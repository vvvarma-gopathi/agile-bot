from uuid import UUID
from fastapi import HTTPException, status
from attachments.models import Comments,Attachments
from attachments.schemas import CreateComment, MessageResponse, UpdateAttachment, UpdateComment,CommentResponse,AttachmentResponse
from auth.dependencies import validate_user
from auth.models import Users


def _get_comment(comment_id: UUID, db):
	comment = db.query(Comments).filter(Comments.id == comment_id).first()
	if not comment:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No comment exists with id={comment_id}',
		)
	return comment


def _require_comment_owner(comment, payload):
	validate_user(payload)
	if comment.user_id != UUID(str(payload['id'])):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='Only the comment owner can modify this comment',
		)


def _get_attachment(attachment_id: UUID, db):
	attachment = db.query(Attachments).filter(Attachments.id == attachment_id).first()
	if not attachment:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No attachment exists with id={attachment_id}',
		)
	return attachment


def _require_attachment_owner(attachment, payload):
	validate_user(payload)
	if attachment.uploaded_by != UUID(str(payload['id'])):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='Only the attachment owner can modify this attachment',
		)


async def create_comment(comment_details: CreateComment, payload, db):
	validate_user(payload)
	comment = Comments(
		**comment_details.model_dump(),
		user_id=UUID(str(payload['id'])),
	)
	db.add(comment)
	db.commit()
	db.refresh(comment)
	return MessageResponse(message='Comment added successfully..')


async def get_comments_by_task_id(task_id: UUID, payload, db):
	validate_user(payload)
	result=[]
	comments=db.query(Comments).filter(Comments.task_id == task_id, Comments.is_delete.is_(False)).order_by(Comments.created_at).all()
	for comment in comments:
		user=db.query(Users).filter(Users.id==comment.user_id).first()
		result.append(CommentResponse(id=comment.id,user_id=comment.user_id,
							task_id=comment.task_id,project_id=comment.project_id,parent_comment_id=comment.parent_comment_id,
							content=comment.content,is_delete=comment.is_delete,created_at=comment.created_at,updated_at=comment.updated_at,user_name=user.user_name))
	return result

async def update_comment(comment_id: UUID, comment_details: UpdateComment, payload, db):
	comment = _get_comment(comment_id, db)
	_require_comment_owner(comment, payload)
	update_data = comment_details.model_dump(exclude_unset=True, exclude_none=True)
	if not update_data:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='At least one comment field must be provided',
		)
	for field, value in update_data.items():
		setattr(comment, field, value)
	db.commit()
	db.refresh(comment)
	return comment


async def delete_comment(comment_id: UUID, payload, db):
	comment = _get_comment(comment_id, db)
	_require_comment_owner(comment, payload)
	db.delete(comment)
	db.commit()
	return MessageResponse(message=f'Comment deleted successfully...')

async def create_attachment(attachment_details,payload,db):
	validate_user(payload)
	comment=db.query(Comments).filter(Comments.id==attachment_details.comment_id).first()
	if not comment or comment.is_delete:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='no comment found')
	_require_comment_owner(comment,payload)
	attachment_record=Attachments(
		**attachment_details.model_dump(exclude={'uploaded_by'}),
		uploaded_by=UUID(str(payload['id'])),
	)
	db.add(attachment_record)
	db.commit()
	db.refresh(attachment_record)
	return MessageResponse(message='Attachment created successfully..')


async def update_attachment(attachment_id: UUID, attachment_details: UpdateAttachment, payload, db):
	attachment = _get_attachment(attachment_id, db)
	_require_attachment_owner(attachment, payload)
	update_data = attachment_details.model_dump(exclude_unset=True, exclude_none=True)
	if not update_data:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail='At least one attachment field must be provided',
		)
	for field, value in update_data.items():
		setattr(attachment, field, value)
	db.commit()
	db.refresh(attachment)
	return attachment


async def delete_attachment(attachment_id: UUID, payload, db):
	attachment = _get_attachment(attachment_id, db)
	_require_attachment_owner(attachment, payload)
	db.delete(attachment)
	db.commit()
	return MessageResponse(message=f'Attachment deleted successfully with id {attachment_id}')


async def get_attachments_by_comment_id(comment_id: UUID, payload, db):
	validate_user(payload)
	result=[]
	comment = db.query(Comments).filter(Comments.id == comment_id, Comments.is_delete.is_(False)).first()
	if not comment:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f'No comment exists with id={comment_id}',
		)
	attachments=db.query(Attachments).filter(Attachments.comment_id == comment_id).order_by(Attachments.created_at).all()
	for attachment in attachments:
		user=db.query(Users).filter(Users.id==attachment.uploaded_by).first()
		result.append(AttachmentResponse(file_name=attachment.file_name,
		                                 file_url=attachment.file_url,file_type=attachment.file_type,
										 uploaded_by=user.user_name,created_at=attachment.created_at))
	return result
	
	