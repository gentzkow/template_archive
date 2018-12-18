import contextlib
import sys

@contextlib.contextmanager
def nostderrout():
    savestderr = sys.stderr
    savestdout = sys.stdout
    class Devnull(object):
        def write(self, _): pass
    sys.stderr = Devnull()    
    sys.stdout = Devnull()
    yield
    sys.stderr = savestderr
    sys.stdout = savestdout