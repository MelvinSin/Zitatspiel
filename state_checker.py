from functools import wraps
from game_state import GameStateEnum, GameState


def check_state(required_state: GameStateEnum):
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            game_state = GameState()  # Instanziere ein GameState-Objekt
            if game_state.get_state() == required_state:
                return await func(ctx, *args, **kwargs)
            else:
                await ctx.send(f'Befehl ist im aktuellen Zustand "{required_state.value}" nicht erlaubt.')

        return wrapper

    return decorator
