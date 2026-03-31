from aiogram import Router
from aiogram.types import Message
from config import ADMINS
from keyboards.main_menu import get_menu

router = Router()

@router.message()
async def start(message: Message):
    is_admin = message.from_user.id in ADMINS
    await message.answer(
        "Добро пожаловать в систему учета картриджей",
        reply_markup=get_menu(is_admin)
    )