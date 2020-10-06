import multiprocessing.connection as mpc
import os
import pathlib

from config import ADDRESS
from manager import RunnersManager


if not os.path.exists(ADDRESS):
    dirname = os.path.dirname(ADDRESS)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
else:
    os.remove(ADDRESS)

with mpc.Listener(ADDRESS, family='AF_UNIX') as listener:
    run = True
    with RunnersManager() as manager:
        while run:
            with listener.accept() as conn:
                response = None
                try:
                    inp = conn.recv()
                    if inp[0].upper() == "POLL":
                        res = manager.get_procs_info()
                        response = ("OK", res)
                    elif inp[0].upper() == "RUN":
                        manager.run(*inp[1:])
                        response = ("OK",)
                    elif inp[0].upper() == "CLOSE":
                        manager.close(int(inp[1]))
                        response = ("OK",)
                    elif inp[0].upper() == "STOP":
                        run = False
                        response = ("OK",)
                    else:
                        response = ("BAD COMMAND", inp[0].upper())
                except Exception as e:
                    response = ("BAD REQUEST", type(e))

                conn.send(response)
