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
