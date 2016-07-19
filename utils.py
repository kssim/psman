import signal
import sys

class _Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('Singleton', (object,), {})): pass


class Logger(Singleton):

    verbose_mode = False

    def psman_log(self, *args):
        if self.verbose_mode == False:
            return

        print ('%s' % args)

    def set_verbose_mode(self, mode):
        self.verbose_mode = True if mode == True else False




class Signal(Singleton):

    def sigint_handler(self, signal, frame):
        Logger().psman_log('You pressed \'Ctrl+C\'')
        print ('Psman is terminated.')
        sys.exit(0)

    def set_signal(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
