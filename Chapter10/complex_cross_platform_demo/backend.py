import subprocess


def get_process_getter_class(os_name):
    backends = {
        'Linux': LinuxProcessGetter,
        'Darwin': MacBsdProcessGetter,
        'Windows': WindowsProcessGetter,
        'freebsd7': MacBsdProcessGetter
    }
    try:
        return backends[os_name]
    except KeyError:
        raise NotImplementedError("No backend for OS")


class GenericProcessGetter:

    cmd = []

    def get_process_list(self):
        if self.cmd:
            return subprocess.check_output(self.cmd)
        else:
            raise NotImplementedError


class LinuxProcessGetter(GenericProcessGetter):
    cmd = ['ps', '-e', '--format', 'comm', '--no-heading']


class MacBsdProcessGetter(GenericProcessGetter):
    cmd = ['ps', '-e', '-o', "comm=''", '-c']


class WindowsProcessGetter(GenericProcessGetter):
    cmd = ['tasklist', '/nh', '/fo', 'CSV']
