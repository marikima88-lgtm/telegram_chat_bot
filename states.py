from aiogram.fsm.state import State, StatesGroup


class MainStates(StatesGroup):
    selecting_city = State()
    selecting_branch = State()

    booking_operation = State()
    booking_currency = State()
    booking_amount = State()
    booking_nominals = State()
    booking_name = State()
    booking_phone = State()
    booking_comment = State()
    booking_review = State()

    rate_request_operation = State()
    rate_request_currency = State()
    rate_request_amount = State()
    rate_request_name = State()
    rate_request_phone = State()
    rate_request_preference = State()
    rate_request_nominals = State()
    rate_request_comment = State()
    rate_request_review = State()

    alert_currency = State()
    alert_rate_type = State()
    alert_condition = State()
    alert_target_rate = State()
    alert_confirmation = State()

    callback_name = State()
    callback_phone = State()
    callback_theme = State()
    callback_comment = State()
    callback_review = State()
