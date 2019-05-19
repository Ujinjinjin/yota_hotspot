from enum import Enum

__all__ = ('OperationSystem',)


class OperationSystem(str, Enum):
    WINDOWS: str = 'Windows'
    LINUX: str = 'Linux'
    OTHER: str = 'Other'

    @classmethod
    def _missing_(cls, value):
        return cls.OTHER
