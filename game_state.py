from enum import Enum, auto


class GameStateEnum(Enum):
    NOT_INITIALISED = auto()
    SETUP = auto()
    STARTED = auto()
    WAIT_FOR_DM = auto()
    DM_DONE = auto()


class GameState:
    _instance = None
    current_state = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_state = GameStateEnum.NOT_INITIALISED
        return cls._instance

    def set_state(self, new_state):
        self.current_state = new_state

    def get_state(self):
        return self.current_state
