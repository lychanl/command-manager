from runner import ProcessRunner

class RunnersManager():
    next_id = 0

    def __init__(self):
        self.runners = {}
    
    def run(self, command, *args):
        self.runners[self.next_id] = ProcessRunner(command, *args)
        self.next_id += 1
        
        while self.next_id in self.runners:
            self.next_id += 1
    
    def close(self, runner_id):
        runner = self.runners.pop(runner_id)
        runner.close()

    def get_procs_info(self):
        return {
            i: {
                'command': r.command,
                'args': r.args,
                'exit_code': r.get_exit_code(),
                'stdout': r.get_last_lines(),
                'start_time': r.start_time,
                'end_time': r.end_time,
            }
            for i, r in self.runners.items()
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, value=None, traceback=None):
        for runner in self.runners.values():
            runner.close()

