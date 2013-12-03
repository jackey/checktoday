# -*- coding: utf-8 -*-
__all__ = ['getTerminalSize', 'notify', 'convertSize']


def notify(msg):
    import pynotify
    if not pynotify.init('icon-summary-body'):
        return
    n = pynotify.Notification('Administrator', 'Error: %s ' % msg,
                              'dialog-warning')
    n.set_urgency(pynotify.URGENCY_CRITICAL)
    n.show()

def info(msg):
    import pynotify
    if not pynotify.init('icon-summary-body'):
        return
    n = pynotify.Notification('Administrator', 'Info: %s ' % msg,
                              'dialog-info')
    n.set_urgency(pynotify.URGENCY_NORMAL)
    n.show()


def convertSize(size):
    import math
    size_name = (
        'KB',
        'MB',
        'GB',
        'TB',
        'PB',
        'EB',
        'ZB',
        'YB',
        )
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    if s > 0:
        return '%s %s' % (s, size_name[i])
    else:
        return '0B'


def getTerminalSize():
    import platform
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _getTerminalSize_windows()
        if tuple_xy is None:
            tuple_xy = _getTerminalSize_tput()

          # needed for window's python in cygwin's xterm!

    if current_os == 'Linux' or current_os == 'Darwin' \
        or current_os.startswith('CYGWIN'):
        tuple_xy = _getTerminalSize_linux()
    if tuple_xy is None:
        print 'default'
        tuple_xy = (80, 25)  # default value
    return tuple_xy


def _getTerminalSize_windows():
    res = None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct

        (
            bufx,
            bufy,
            curx,
            cury,
            wattr,
            left,
            top,
            right,
            bottom,
            maxx,
            maxy,
            ) = struct.unpack('hhhhHhhhhhh', csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return (sizex, sizey)
    else:
        return None


def _getTerminalSize_tput():

    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window

    try:
        import subprocess
        proc = subprocess.Popen(['tput', 'cols'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        output = proc.communicate(input=None)
        cols = int(output[0])
        proc = subprocess.Popen(['tput', 'lines'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        output = proc.communicate(input=None)
        rows = int(output[0])
        return (cols, rows)
    except:
        return None


def _getTerminalSize_linux():

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            import os
            cr = struct.unpack('hh', fcntl.ioctl(fd,
                               termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return (int(cr[1]), int(cr[0]))



            