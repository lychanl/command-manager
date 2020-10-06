import atexit
import datetime
import subprocess
import threading

from config import LINES


class ProcessRunner:
    def __init__(self, command, *args):
        self.command = command
        self.args = args
        self.last_lines = []
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.proc = subprocess.Popen([command, *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        self.output_reader_thread = threading.Thread(target=self.__output_reader)
        self.output_reader_thread.start()

        atexit.register(self.__exit__)

    def __output_reader(self):
        for line in iter(self.proc.stdout.readline, b''):
            self.last_lines = (self.last_lines + [(line).decode("utf-8").rstrip()])[-LINES:]
        self.end_time = datetime.datetime.now()
    
    def get_exit_code(self):
        return self.proc.poll()
    
    def close(self):
        self.__exit__()
    
    def get_last_lines(self):
        return list(self.last_lines)

    def __exit__(self, exc_type=None, value=None, traceback=None):
        if self.proc.poll() == None:
            self.proc.kill()
            
        self.output_reader_thread.join()
        self.proc.__exit__(exc_type, value, traceback)
