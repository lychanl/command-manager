import multiprocessing.connection as mpc
import pickle
import sys
import shlex

from config import ADDRESS


interactive = "--pickle" not in sys.argv

if interactive:
    print('[CCCC  OOOO  MM  MM  MM  MM   AA   N  N]')
    print('[C     O  O  M MM M  M MM M  A  A  NN N]')
    print('[C     O  O  M MM M  M MM M  AAAA  N NN]')
    print('[CCCC  OOOO  M    M  M    M  A  A  N  N]')
    print()
    print("Welcome to comman cli")

run = True
while run:
    try:
        with mpc.Client(ADDRESS, family='AF_UNIX') as client:
            inp = shlex.split(input())
            client.send(inp)
            response = client.recv()
            if interactive:
                print(*response, sep=' ')
            else:
                print(pickle.dumps(response))
            run = inp[0].upper() not in ('EXIT', 'STOP')
            
    except Exception as e:
        if interactive:
            print('AN ERROR OCCURED: ' + type(e))
        else:
            print(pickle.dumps(e))

    run = run and interactive

