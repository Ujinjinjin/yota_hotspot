import os
from tools.tools import *

__all__ = ('Program',)


class Program:
    @staticmethod
    def start():
        if is_configured_for_hotspot():
            print('Your computer configured for hotspot')
            print('Cleaning stuff...')
            # delete_reg_key()
            # clean_hosts()
            print('Done! Now your PC is clean and beautiful')
        else:
            print('Your computer is not configured for hotspot')
            print('Doing some stuff...')
            # create_reg_key()
            # configure_hosts()
            print('Done! Now your PC is ready to receive hotspot and stuff')

        print('Almost there, you have to restart your PC.')
        restart_response = input('Want to do it now? (y/n): ')

        if restart_response == 'y':
            print('Restarting, bye-bye')
            os.system("shutdown -t 0 -r -f")

        input('Press any key to continue...')
