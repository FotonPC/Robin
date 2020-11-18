# Robin Error System
class RoExitError(Exception):
    def __init__(self, *argv):
        # print('END RUN CODE')
        pass


class Ro_Error:
    def __init__(self, line, text, string, p=0):
        self.line = line
        self.info = text
        self.string = string
        self.out(p)
        raise RoExitError('')

    def out(self, p):
        print(self.stroka(), str(self.line) + ':', "\n " + self.string, "\n" + self.pos(p), '\n', self.name() + ':',
              self.info)

    def name(self):
        return 'BasicError'

    def pos(self, p):
        return ' ' * (p + 1) + "^"

    def stroka(self):
        return ' In string'


class Ro_NameError(Ro_Error):
    def name(self):
        return 'NameError'


class Ro_SintaxError(Ro_Error):
    def name(self):
        return 'SintaxError'


class Ro_ValueError(Ro_Error):
    def name(self):
        return 'ValueError'


class Ro_TypeError(Ro_Error):
    def name(self):
        return 'TypeError'


class Ro_MemoryError(Ro_Error):
    def name(self):
        return 'MemoryError'


class Ro_RobinError(Ro_Error):
    def name(self):
        return 'PobinError'


class Ro_SystemError(Ro_Error):
    def name(self):
        return 'SystemError'


class Ro_SimpleError(Ro_Error):
    def name(self):
        return 'SimpleError'


class Ro_TabError(Ro_Error):
    def name(self):
        return 'TabError'
