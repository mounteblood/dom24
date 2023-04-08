from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
    buying = State()
    selling = State()
    editing = State()
    property_group_saving = State()
    property_group_naming = State()
