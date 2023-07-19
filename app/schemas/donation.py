from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема объекта пожертвования."""
    comment: Optional[str] = Field(None, title='Комментарий')
    full_amount: PositiveInt = Field(..., title='Сумма пожертвования')

    class Config:
        title = 'Базовая схема пожертвования'


class DonationCreate(DonationBase):
    """Схема пожертвования для создания."""

    class Config:
        extra = Extra.forbid
        title = 'Схема пожертвования для создания'


class DonationDB(DonationBase):
    """Схема пожертвования для получения из базы обычным пользователем."""
    id: int = Field(..., title='ID пожертвования')
    create_date: datetime = Field(..., title='Дата внесения пожертвования')

    class Config:
        title = 'Схема пожертвования для получения'
        orm_mode = True


class DonationDBSuper(DonationDB):
    """Схема пожертвования для получения из базы суперпользователем."""
    user_id: Optional[int] = Field(None, title='ID пользователя')
    invested_amount: int = Field(0, title='Сколько вложено')
    fully_invested: bool = Field(False, title='Вложена полная сумма')
    close_date: Optional[datetime] = Field(None, title='Дата вложения')

    class Config:
        title = 'Схема пожертвования для получения (advanced)'
        orm_mode = True
