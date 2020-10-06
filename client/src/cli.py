import getpass
import os
import shlex


class CLI:

    commands_list = []
    commands_args = {}
    commands_descr = {}
    commands_funs = {}

    def __init__(self, servers):
        self.servers = servers
        
        self.add_command("help", (), "Display help message", self.help)

        self.add_command("ls", (), "List servers", self.ls)
        self.add_command("add", ("hostname", "username", "source_dir"), "Add server", self.add)
        self.add_command("checkpass", (), "Check if servers have ssh passwords set", self.checkpass)
        self.add_command("setpass", ("hostname"), "Set server ssh password", self.setpass)

        self.add_command("poll", (), "Poll servers", self.poll)
        self.add_command("run", ("hostname", "command_with_args"), "Run command on server", self.run)
        self.add_command("close", ("hostname", "id"), "Close command on server", self.close)

        self.add_command("load", ("filename"), "Load server list", self.load)
        self.add_command("store", ("filename"), "Store server list", self.store)

        self.add_command("exit", (), "Exit program", self.exit)

    def run_cli(self):
        run = True
        while run:
            inp = shlex.split(input())
            if not inp:
                continue
            else:
                self.run_command(*inp)

    def add_command(self, command, args, descr, fun):
        self.commands_list.append(command)
        self.commands_args[command] = args
        self.commands_descr[command] = descr
        self.commands_funs[command] = fun

    def run_command(self, command, *args):
        if command not in self.commands_list:
            print(f"Invalid command: {command}")
            return True
        if len(args) < len(self.commands_args[command]):
            print(f"Invalid number of args. {len(args)} given, {len(self.commands_args[command])}")
            return True

        return self.commands_funs[command](*args)

    def exit(self, *args):
        return False
    
    def yesno(self, question):
        while True:
            print(f"{question} [Y]es or [N]o")
            inp = input()
            if inp.upper()[0] == "Y":
                return True
            elif inp.upper()[0] == "N":
                return False

    def help(self, *args):
        print("Available commands:")
        for command in self.commands_list:
            print(command)
            print(f"\t{self.commands_descr[command]}")
            print(f"\tArgs:")
            for arg in self.commands_args[command]:
                print(f"\t\t{arg}")
            print()
        return True
    
    def ask_password(self):
        return getpass.getpass("Give password:")

    def add(self, hostname, username, source_dir):
        return self.ask_password()
    
    def ls(self):
        print(self.servers.servers.keys(), sep=os.linesep)

    def poll(self):
        results = self.servers.poll()
        # TODO display
        print(results)

    def run(self, hostname, command_with_args):
        self.servers.server[hostname].run(command_with_args)

    def close(self, hostname, id):
        self.servers.server[hostname].close()

    def setpass(self, hostname):
        password = self.ask_password()
        self.servers.server[hostname].password = password

    def store(self, filename):
        self.servers.store(filename)

    def load(self, filename):
        self.servers.load(filename)

    def checkpass(self):
        sp = self.servers.check_passwwords()
        for s, p in sp.items():
            print(s, "Yes" if p else "No", sep="\t")
