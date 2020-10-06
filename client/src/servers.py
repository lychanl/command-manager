import pickle

from server import Server


class Servers:
    def __init__(self):
        self.servers = {}
        self.last_filename = None

    def add_server(self, hostname, username, password, src_dir):
        self.servers[hostname] = Server(hostname, username, password, src_dir)
    
    def load(self, filename):
        with open(filename, 'wb') as f:
            self.servers.update(pickle.load(f))
        self.last_filename = filename

    def store(self, filename):
        with open(filename, 'rb') as f:
            pickle.dump(self.servers, f)
        self.last_filename = filename

    def check_passwords(self):
        return {h: s.password == None for h, s in self.servers.items()}
    
    def poll(self):
        return {h: s.poll() for h, s in self.servers.items()}