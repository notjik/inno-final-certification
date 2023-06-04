from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMBuy(StatesGroup):
    game_id = State()
    delivery = State()
