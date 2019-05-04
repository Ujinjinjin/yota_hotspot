import ctypes
from winregistry import WinRegistry as Reg

__all__ = ('is_admin', 'create_reg_key', 'is_configured_for_hotspot', 'delete_reg_key', 'clean_hosts',
           'configure_hosts')

key_path: str = r'HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters'
key_name: str = r'DefaultTTL2'
key_value: int = 65
key_type: str = 'REG_DWORD'
_reg: Reg = Reg()


# noinspection PyBroadException
def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def is_configured_for_hotspot() -> bool:
    registry = _reg.read_key(key_path)

    for item in registry['values']:
        if item['value'] == key_name and item['data'] == key_value:
            return True
    return False


def create_reg_key():
    _reg.write_value(key_path, key_name, key_value, key_type)


def delete_reg_key():
    _reg.delete_value(key_path, key_name)


def configure_hosts():
    with open('hosts_filled', 'r', encoding='utf8') as hosts_file:
        new_hosts: str = hosts_file.read()

    with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w', encoding='utf8') as hosts_file:
        hosts_file.write(new_hosts)


def clean_hosts():
    with open('hosts_empty', 'r', encoding='utf8') as hosts_file:
        new_hosts: str = hosts_file.read()

    with open('C:\\Windows\\System32\\drivers\\etc\\hosts', 'w', encoding='utf8') as hosts_file:
        hosts_file.write(new_hosts)
