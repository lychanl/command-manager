import ast
import pickle
import posixpath

import paramiko


class Server():
    def __init__(self, hostname = None, username = None, password = None, src_dir = None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.src_dir = src_dir
        self.cli_cmd = f"python3 {posixpath.join(self.src_dir, 'server/src/cli.py')} --pickle"
    
    def poll(self):
        return self._run_cli("poll")

    def close(self, proc_id):
        return self._run_cli("close", str(proc_id))

    def run(self, command_with_args):
        return self._run_cli("run", command_with_args)

    def _run_cli(self, command, args=""):
        with paramiko.SSHClient() as client:
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.hostname, username=self.username, password=self.password)
            stdin, stdout, _ = client.exec_command(self.cli_cmd)
            stdin.write(f'{command}{" " if args else ""}{args}\n')
            stdin.flush()
            result = stdout.read()
            client.close()
        return pickle.loads(ast.literal_eval(result.decode("utf-8")))
    
    def __getstate__(self):
        # don't pickle passwords
        state = self.__dict__.copy()
        del state["password"]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
