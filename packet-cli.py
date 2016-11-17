#!/usr/bin/env python3

import packet
import os
import argh
import inspect
import pprint

TOKEN = os.environ['PACKET_TOKEN']

manager = packet.Manager(auth_token=TOKEN)

class C:
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'

def R(msg):
    return C.red + msg + C.end

def G(msg):
    return C.green + msg + C.end

def B(msg):
    return C.blue + msg + C.end

methods = [m for m in inspect.getmembers(manager, predicate=inspect.ismethod)
           if not m[0].startswith("__")]

def color_loop():
    while True:
        yield R
        yield G
        yield B


def colprint(*args):
    l = [f(str(i)) for f,i in zip(color_loop(), args)]
    print(*l)


def show_res(r):
    just_name_and_id = [packet.Project, packet.OperatingSystem]
    if type(r) in just_name_and_id:
        colprint(r.name, r.id)
    elif type(r) is packet.SSHKey:
        colprint(r.label, r.id, r.key)
    elif type(r) is packet.Facility:
        colprint(r.name, r.code, r.id, r.features)
    elif type(r) is packet.Plan:
        colprint(r.name, r.id, r.slug)
    elif type(r) is packet.Device:
        colprint(r.hostname, r.id, r.operating_system, r.state,
                 [i['address'] for i in r.ip_addresses])
    else:
        pprint.pprint(r)



def deco(f):
    def temp_fun(*args,**kwargs):
        out = f(*args, **kwargs)
        #print(type(out))
        if type(out) is list:
            for i in out:
                show_res(i)
        else:
            show_res(out)
         
    temp_fun.__name__ = f.__name__
    return temp_fun

exposed_methods = [deco(m[1]) for m in methods]

parser = argh.ArghParser()

if __name__ == "__main__":
    parser.add_commands(exposed_methods)
    parser.dispatch()


