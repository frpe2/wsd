from aiogram.fsm.state import State, StatesGroup

class AddCartridge(StatesGroup):
    model = State()
    owner = State()

class SearchState(StatesGroup):
    query = State()

class EditState(StatesGroup):
    model = State()
    owner = State()