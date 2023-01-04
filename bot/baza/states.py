from aiogram.dispatcher.filters.state import State, StatesGroup


# apartment callback states
class CallbackOnStart(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()
    Q11 = State()
    Q12 = State()
    Q13 = State()
    Q14 = State()
    Q15 = State()


class RoomCallbackStates(StatesGroup):
    R1 = State()
    R2 = State()
    R3 = State()
    R4 = State()
    R5 = State()
    R6 = State()
    R7 = State()
    R8 = State()
    R9 = State()
    R10 = State()
    R11 = State()
    R12 = State()
    R13 = State()
    R14 = State()
    R15 = State()


class HouseCallbackStates(StatesGroup):
    H1 = State()
    H2 = State()
    H3 = State()
    H4 = State()
    H5 = State()
    H6 = State()
    H7 = State()
    H8 = State()
    H9 = State()
    H10 = State()
    H11 = State()
    H12 = State()
    H13 = State()
    H14 = State()
    H15 = State()
    H16 = State()
    H17 = State()
    H18 = State()
    H19 = State()
    H20 = State()
    H21 = State()
    H22 = State()
    H23 = State()


class TownHouseCallbackStates(StatesGroup):
    T1 = State()
    T2 = State()
    T3 = State()
    T4 = State()
    T5 = State()
    T6 = State()
    T7 = State()
    T8 = State()
    T9 = State()
    T10 = State()
    T11 = State()
    T12 = State()
    T13 = State()
    T14 = State()
    T15 = State()
    T16 = State()
    T17 = State()
    T18 = State()
    T19 = State()
    T20 = State()
    T21 = State()
    T22 = State()
    T23 = State()


class LandCallbackStates(StatesGroup):
    L1 = State()
    L2 = State()
    L3 = State()
    L4 = State()
    L5 = State()
    L6 = State()
    L7 = State()
    L8 = State()
    L9 = State()
    L10 = State()
    L11 = State()
    L12 = State()
    L13 = State()
    L14 = State()
    L15 = State()
    L16 = State()
    L17 = State()
    L18 = State()
    L19 = State()
    L20 = State()
    L21 = State()


class MyObjectsCallbackStates(StatesGroup):
    MO1 = State()


class PriceEditCallbackStates(StatesGroup):
    EP1 = State()
    EP2 = State()
    EP3 = State()
    EP4 = State()


class EditCallbackStates(StatesGroup):
    E1 = State()
    E2 = State()
    E3 = State()


class DeleteCallbackStates(StatesGroup):
    D1 = State()
    D2 = State()
    D3 = State()
    D4 = State()


class Buyer(StatesGroup):
    buyer_name = State()
    buyer_phone_number = State()
    category = State()
    microregion = State()
    city_microregion = State()
    room_quantity = State()
    last_floor = State()
    limit = State()
    source = State()
    initial_payment = State()
    none_initial_payment_microregion = State()
    comment = State()
    base_update = State()
