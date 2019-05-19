import os
import platform
from .utils.utils import *
from .configurator.configurator import *
from .enums import *
from typing import Dict, Type

__all__ = ('Program',)


class Program:
    """Main program, that should be started"""

    def __init__(self, main_file: str):
        self.main_file: str = main_file
        self.utils: BaseUtils = self._get_utils()
        self.configurator: BaseConfigurator = self._get_configurator()
        self.OS: OperationSystem = self._detect_system()

    def start(self):
        """Start program as admin"""
        if self.utils.is_admin():
            self._start()
        else:
            self.utils.run_as_admin()

    def _start(self):
        """Main logic"""
        if self.configurator.is_configured_for_hotspot():
            print('Your computer configured for hotspot')
            print('Cleaning stuff...')
            self.configurator.delete_reg_key()
            self.configurator.clean_hosts()
            print('Done! Now your PC is clean and beautiful')
        else:
            print('Your computer is not configured for hotspot')
            print('Doing some stuff...')
            self.configurator.create_reg_key()
            self.configurator.configure_hosts()
            print('Done! Now your PC is ready to receive hotspot and stuff')

        print('Almost there, you have to restart your PC.')
        restart_response = input('Want to do it now? (y/n): ')

        if restart_response == 'y':
            print('Restarting, bye-bye')
            self.utils.restart_system()

        input('Press any key to continue...')

    @staticmethod
    def _detect_system() -> OperationSystem:
        return OperationSystem(platform.system())

    def _get_utils(self) -> BaseUtils:
        """Get utils class depending on what system it's running"""
        cleaners_by_system: Dict[OperationSystem, Type[BaseUtils]] = {
            OperationSystem.LINUX: LinuxUtils,
            OperationSystem.WINDOWS: WindowsUtils
        }
        if self.OS in cleaners_by_system.keys():
            return cleaners_by_system[self.OS](self.main_file)
        else:
            raise OSError(f'Your OS utils currently not supported. '
                          f'We have utils for following systems: {", ".join(cleaners_by_system.keys())}')

    def _get_configurator(self) -> BaseConfigurator:
        """Do similar stuff as in _get_utils"""
        configurator_by_system: Dict[OperationSystem, Type[BaseConfigurator]] = {
            OperationSystem.WINDOWS: WindowsConfigurator
        }

        if self.OS in configurator_by_system.keys():
            return configurator_by_system[self.OS]()
        else:
            raise OSError(f'Your OS configurator currently not supported. '
                          f'We have configurators for following systems: {", ".join(configurator_by_system.keys())}')
