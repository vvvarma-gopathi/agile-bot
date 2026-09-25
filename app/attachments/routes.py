from fastapi import APIRouter, Depends, status
from uuid import UUID

from attachments.schemas import CommentResponse, CreateComment, MessageResponse, UpdateAttachment, UpdateComment,AttachmentResponse,CreateAttachment
from attachments.services import create_comment, delete_attachment, delete_comment, get_attachments_by_comment_id, get_comments_by_task_id, update_attachment, update_comment,create_attachment
from auth.dependencies import get_current_user
from core.database import get_db


attachment_router = APIRouter(prefix='/comments', tags=['Comment Routes'])


@attachment_router.post('', response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
	comment_details: CreateComment,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await create_comment(comment_details, payload, db)


@attachment_router.get('/task/{task_id}', response_model=list[CommentResponse], status_code=status.HTTP_200_OK)
async def get_comments_for_task(
	task_id: UUID,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await get_comments_by_task_id(task_id, payload, db)


@attachment_router.put('/{comment_id}', response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def update_comment_by_id(
	comment_id: UUID,
	comment_details: UpdateComment,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await update_comment(comment_id, comment_details, payload, db)


@attachment_router.delete('/{comment_id}', response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_comment_by_id(
	comment_id: UUID,
	payload=Depends(get_current_user),
	db=Depends(get_db),
):
	return await delete_comment(comment_id, payload, db)

@attachment_router.post('/create/attachment',response_model=AttachmentResponse,status_code=status.HTTP_201_CREATED)
async def add_attachment(attachment_details:CreateAttachment,payload=Depends(get_current_user),db=Depends(get_db)):
	return await create_attachment(attachment_details,payload,db)

@attachment_router.get('/{comment_id}/attachments',response_model=list[AttachmentResponse],status_code=status.HTTP_200_OK)
async def get_attachments_for_comment(comment_id: UUID,payload=Depends(get_current_user),db=Depends(get_db)):
	return await get_attachments_by_comment_id(comment_id,payload,db)

@attachment_router.put('/attachments/{attachment_id}',response_model=AttachmentResponse,status_code=status.HTTP_200_OK)
async def update_attachment_by_id(attachment_id: UUID,attachment_details:UpdateAttachment,payload=Depends(get_current_user),db=Depends(get_db)):
	return await update_attachment(attachment_id,attachment_details,payload,db)

@attachment_router.delete('/attachments/{attachment_id}',response_model=MessageResponse,status_code=status.HTTP_200_OK)
async def delete_attachment_by_id(attachment_id: UUID,payload=Depends(get_current_user),db=Depends(get_db)):
	return await delete_attachment(attachment_id,payload,db)

