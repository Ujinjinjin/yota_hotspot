from abc import ABC, abstractmethod

from winregistry import WinRegistry as Reg

__all__ = ('BaseConfigurator', 'WindowsConfigurator',)


class BaseConfigurator(ABC):
    @property
    @abstractmethod
    def is_configured_for_hotspot(self):
        pass

    @abstractmethod
    def _is_configured_for_hotspot(self) -> bool:
        pass

    @abstractmethod
    def create_reg_key(self):
        pass

    @abstractmethod
    def delete_reg_key(self):
        pass

    @staticmethod
    @abstractmethod
    def configure_hosts():
        pass

    @staticmethod
    @abstractmethod
    def clean_hosts():
        pass


class WindowsConfigurator(BaseConfigurator):
    KEY_PATH: str = r'HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters'
    KEY_NAME: str = 'DefaultTTL'
    KEY_VALUE: int = 65
    KEY_TYPE: str = 'REG_DWORD'

    def __init__(self):
        self._reg: Reg = Reg()

    @property
    def is_configured_for_hotspot(self):
        return self._is_configured_for_hotspot()

    def _is_configured_for_hotspot(self) -> bool:
        registry = self._reg.read_key(self.KEY_PATH)

        for item in registry['values']:
            if item['value'] == self.KEY_NAME and item['data'] == self.KEY_VALUE:
                return True
        return False

    def create_reg_key(self):
        self._reg.write_value(self.KEY_PATH, self.KEY_NAME, self.KEY_VALUE, self.KEY_TYPE)

    def delete_reg_key(self):
        self._reg.delete_value(self.KEY_PATH, self.KEY_NAME)

    @staticmethod
    def configure_hosts():
        with open('hosts_filled', 'r', encoding='utf8') as hosts_file:
            new_hosts: str = hosts_file.read()

        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w', encoding='utf8') as hosts_file:
            hosts_file.write(new_hosts)

    @staticmethod
    def clean_hosts():
        with open('hosts_empty', 'r', encoding='utf8') as hosts_file:
            new_hosts: str = hosts_file.read()

        with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w', encoding='utf8') as hosts_file:
            hosts_file.write(new_hosts)
