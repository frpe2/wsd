from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMINS
from states.cartridge_states import AddCartridge, SearchState, EditState
from services.cartridge_service import *
from keyboards.inline import *
from database.models import Status

router = Router()

def is_admin(uid):
    return uid in ADMINS

# ---------- ДОБАВЛЕНИЕ ----------
@router.message(F.text == "➕ Добавить картридж")
async def add_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await message.answer("Введите модель:")
    await state.set_state(AddCartridge.model)

@router.message(AddCartridge.model)
async def add_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите владельца:")
    await state.set_state(AddCartridge.owner)

@router.message(AddCartridge.owner)
async def add_owner(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_cartridge(data["model"], message.text, str(message.from_user.id))
    await message.answer("Добавлено")
    await state.clear()

# ---------- СПИСОК ----------
@router.message(F.text == "📦 Список картриджей")
async def list_all(message: Message):
    data = await get_all()
    for c in data:
        await message.answer(
            f"{c.id}. {c.model} | {c.owner} | {c.status.value}",
            reply_markup=cartridge_actions_keyboard(c.id)
        )

# ---------- ПОИСК ----------
@router.message(F.text == "🔍 Поиск")
async def search_start(message: Message, state: FSMContext):
    await message.answer("Введите запрос:")
    await state.set_state(SearchState.query)

@router.message(SearchState.query)
async def search_do(message: Message, state: FSMContext):
    results = await search_cartridges(message.text)
    for c in results:
        await message.answer(
            f"{c.id}. {c.model} | {c.owner} | {c.status.value}",
            reply_markup=cartridge_actions_keyboard(c.id)
        )
    await state.clear()

# ---------- ФИЛЬТР ----------
@router.message(F.text == "📊 Фильтр по статусу")
async def filter_menu(message: Message):
    await message.answer("1-склад 2-сервис 3-готов 4-выдан")

@router.message(F.text.in_(["1","2","3","4"]))
async def filter_do(message: Message):
    mapping = {
        "1": Status.IN_STOCK,
        "2": Status.IN_SERVICE,
        "3": Status.READY,
        "4": Status.ASSIGNED
    }
    data = await get_by_status(mapping[message.text])
    for c in data:
        await message.answer(f"{c.model} | {c.owner}")

# ---------- СЕРВИС ----------
@router.message(F.text == "📤 В сервис")
async def to_service(message: Message):
    data = await get_all()
    await message.answer("Выбор:", reply_markup=cartridge_list_keyboard(data,"to_service"))

@router.callback_query(F.data.startswith("to_service"))
async def to_service_do(callback: CallbackQuery):
    cid = int(callback.data.split(":")[1])
    await update_status(cid, Status.IN_SERVICE, str(callback.from_user.id))
    await callback.message.answer("Отправлено")

@router.message(F.text == "📥 Из сервиса")
async def from_service(message: Message):
    data = await get_all()
    await message.answer("Выбор:", reply_markup=cartridge_list_keyboard(data,"from_service"))

@router.callback_query(F.data.startswith("from_service"))
async def from_service_do(callback: CallbackQuery):
    cid = int(callback.data.split(":")[1])
    await update_status(cid, Status.READY, str(callback.from_user.id))
    await callback.message.answer("Готов")

# ---------- УДАЛЕНИЕ ----------
@router.callback_query(F.data.startswith("delete"))
async def delete(callback: CallbackQuery):
    cid = int(callback.data.split(":")[1])
    await delete_cartridge(cid, str(callback.from_user.id))
    await callback.message.answer("Удалено")

# ---------- РЕДАКТИРОВАНИЕ ----------
@router.callback_query(F.data.startswith("edit"))
async def edit_start(callback: CallbackQuery, state: FSMContext):
    cid = int(callback.data.split(":")[1])
    await state.update_data(cid=cid)
    await callback.message.answer("Новая модель:")
    await state.set_state(EditState.model)

@router.message(EditState.model)
async def edit_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Новый владелец:")
    await state.set_state(EditState.owner)

@router.message(EditState.owner)
async def edit_owner(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_cartridge(
        data["cid"],
        data["model"],
        message.text,
        str(message.from_user.id)
    )
    await message.answer("Обновлено")
    await state.clear()

# ---------- ЛОГ ----------
@router.callback_query(F.data.startswith("log"))
async def logs(callback: CallbackQuery):
    cid = int(callback.data.split(":")[1])
    logs = await get_logs(cid)

    text = "\n".join([
        f"{l.timestamp} | {l.action} | {l.user}"
        for l in logs
    ]) or "Пусто"

    await callback.message.answer(text)
