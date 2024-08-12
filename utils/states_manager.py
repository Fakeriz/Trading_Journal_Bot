from enum import Enum, auto


class TradeStates(Enum):
    INIT = auto()
    DATE = auto()
    DATE_VALIDATION = auto()
    TIME = auto()
    TICKER = auto()
    WIN_LOSS = auto()
    SIDE = auto()
    RR = auto()
    PNL = auto()
    STRATEGY = auto()
    PHOTO = auto()
    SAVE = auto()
    CHECK_TRADES = auto()
    CHECK_DATE_RANGE = auto()
    CHECK_ID = auto()
    CHECK_TICKER = auto()
    CHECK_SIDE = auto()
    CHECK_STATUS = auto()


class ExportStates(Enum):
    EXPORT_TICKER = auto()
    EXPORT_PERIOD = auto()
    CUSTOM_DATE_RANGE = auto()
    CUSTOM_TICKER = auto()


class CheckTradesStates(Enum):
    CHECK_TRADES  = auto()
    CHECK_DATE_RANGE = auto()
    CHECK_ID = auto()
    CHECK_TICKER = auto()
    CHECK_SIDE = auto()
    CHECK_STATUS = auto()


class UpdateTradesState(Enum):
    TRADE_ID = auto()
    UPDATE_CHOICE = auto()
    UPDATE_TICKER = auto()
    UPDATE_STATUS = auto()
    UPDATE_SIDE = auto()
    UPDATE_STRATEGY = auto()
