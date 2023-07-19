from datetime import datetime

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    """Базовая схема объекта пожертвования."""
    comment: str = Field(..., title='Комментарий')
    full_amount: int = Field(..., title='Сумма пожертвования')

    class Config:
        title = 'Базовая схема пожертвования'


class DonationCreate(BaseModel):
    """Схема пожертвования для создания."""

    class Config:
        extra = Extra.forbid
        title = 'Схема пожертвования для создания'


class DonationDB(DonationBase):
    """Схема пожертвования для получения из базы обычным пользователем."""
    id: int = Field(..., title='ID пожертвования')
    create_date: datetime = Field(..., title='Время внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'


class DonationDBSuper(DonationDB):
    """Схема пожертвования для получения из базы суперпользователем."""
    user_id: int = Field(..., title='ID пользователя')
    invested_amount: int = Field(0, title='Сколько вложено')
    fully_invested: bool = Field(False, title='Вложена полная сумма')
    close_date: datetime = Field(..., title='Дата вложения')

    class Config:
        title = 'Схема пожертвования для получения (advanced)'
