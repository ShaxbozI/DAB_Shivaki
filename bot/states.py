from aiogram.fsm.state import State, StatesGroup



class FAQ(StatesGroup):
    murojaat = State() 



class MAI(StatesGroup):
    name = State()
    file = State() 



class BroadcastStates(StatesGroup):
    waiting_for_message = State()
 


class PhotoAddorUpdate(StatesGroup):
    waiting_for_category = State()
    waiting_for_item_selection = State()
    waiting_for_photo = State()



class BookAddorUpdate(StatesGroup):
    waiting_for_category = State()
    waiting_for_item_selection = State()
    waiting_for_book = State()
