from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    """Базовое схема объекта проекта."""
    name: Optional[str] = Field(
        None,
        title='Название',
        min_length=1,
        max_length=100,
    )
    description: Optional[str] = Field(None, title='Описание')
    full_amount: Optional[PositiveInt] = Field(None, title='Требуемая сумма')

    class Config:
        title = 'Базовая схема проекта'


class CharityProjectCreate(CharityProjectBase):
    """Схема проекта для создания."""
    name: str = Field(
        ...,
        title='Название',
        min_length=1,
        max_length=100,
    )
    description: str = Field(..., title='Описание')
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')

    class Config:
        title = 'Схема проекта для создания'
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта для получения."""
    id: int = Field(..., title='Порядковый номер')
    invested_amount: int = Field(0, title='Сколько пожертвовано')
    fully_invested: bool = Field(False, title='Собрана нужная сумма')
    create_date: datetime = Field(..., title='Дата открытия проекта')
    close_date: Optional[datetime] = Field(None, title='Дата закрытия проекта')

    class Config:
        title = 'Схема проекта для получения'
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Схема проекта для обновления."""

    class Config:
        title = 'Схема проекта для обновления'
        orm_mode = True

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value: str):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value




    # @validator('close_date')
    # def check_close_date_is_none(cls, value: datetime):
    #     pass
    #     if value:
    #         raise ValueError('Нельзя редактировать закрытый проект!')
    #     return value
    #
    # @validator('full_amount')
    # def check_full_amount_greater_than_invested(cls, value: int):
    #     pass



