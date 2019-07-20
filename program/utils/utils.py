import ctypes
import os
import sys
from abc import ABC, abstractmethod

__all__ = ('BaseUtils', 'WindowsUtils', 'LinuxUtils',)


class BaseUtils(ABC):
    """Base abstract utils class"""

    def __init__(self, main_file: str):
        self.main_file = main_file

    @abstractmethod
    def is_admin(self) -> bool:
        """Check is script running with admin privileges"""
        pass

    @abstractmethod
    def run_as_admin(self) -> None:
        """Run script with admin privileges"""
        pass

    @abstractmethod
    def restart_system(self) -> None:
        """Restart system"""
        pass


class WindowsUtils(BaseUtils):
    """Windows OS utils"""

    def restart_system(self) -> None:
        os.system("shutdown -t 0 -r -f")

    # noinspection PyBroadException
    def is_admin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def run_as_admin(self):
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, self.main_file, None, 1)


class LinuxUtils(BaseUtils):
    """Linux OS utils"""

    def restart_system(self) -> None:
        pass

    def is_admin(self) -> bool:
        return os.geteuid() == 0

    def run_as_admin(self):
        os.execvp('sudo', ['sudo'] + ['python'] + sys.argv)
