import functools


class VibraSignal:
    """
    This class is suposed to work like a pyqtBoundSignal,
    the class created when you use a qt signal.
    The implementation is very simple, and probably need to
    be changed in the future, but for now it helps a lot
    with the decoupling of the software structure.
    """

    def __init__(self) -> None:
        self.callbacks = set()

    def connect(self, function):
        if not callable(function):
            raise TypeError(f'"{function}" is not callable')
        self.callbacks.add(function)

    def disconnect(self, function):
        if function in self.callbacks:
            self.callbacks.remove(function)

    def emit(self, *args, **kwargs):
        for function in self.callbacks:
            if callable(function):
                function(*args, **kwargs)


def signal_emitter(*signal_names: str):
    """
    Decorator to emit signals after a function is called.
    It accepts a list of signal names to be emitted.
    """

    if not signal_names:
        raise ValueError("At least one signal name must be provided")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)

            for name in signal_names:
                if not hasattr(self, name):
                    raise ValueError(f'Signal "{name}" does not exist')

                signal: VibraSignal = getattr(self, name)
                signal.emit()

            return ret

        return wrapper

    return decorator