from datetime import date, datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SprintStatus(StrEnum):
    PLANNED = 'planned'
    ACTIVE = 'active'
    COMPLETED = 'completed'

class CreateSprint(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=5, max_length=225, description='name of sprint')
    project_id: UUID = Field(..., description='unique id of project')
    goal: str = Field(..., min_length=1, description='goal of the sprint')
    start_date: date = Field(..., description='start date of sprint')
    end_date: date = Field(..., description='end date of sprint')
    status: SprintStatus = Field(..., description='status of sprint')

    @model_validator(mode='after')
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self


class UpdateSprint(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Optional[str] = Field(None, min_length=5, max_length=225, description='name of sprint')
    goal: Optional[str] = Field(None, min_length=1, description='goal of the sprint')
    start_date: Optional[date] = Field(None, description='start date of sprint')
    end_date: Optional[date] = Field(None, description='end date of sprint')
    status: Optional[SprintStatus] = Field(None, description='status of sprint')

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.end_date <= self.start_date:
                raise ValueError('end_date must be after start_date')
        return self


class CreateSprintItems(BaseModel):
    sprint_id: UUID = Field(..., description='unique id of sprint')
    task_id: UUID = Field(..., description='unique id of task')


class UpdateSprintItems(BaseModel):
    sprint_id: Optional[UUID] = Field(None, description='unique id of sprint')
    task_id: Optional[UUID] = Field(None, description='unique id of task')


class SprintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    goal: str
    start_date: date
    end_date: date
    status: SprintStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class SprintItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sprint_id: UUID
    task_id: UUID
    added_at: datetime


class MessageResponse(BaseModel):
    message: str

