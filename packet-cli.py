#!/usr/bin/env python3

import packet
import os
import argh
import inspect
import pprint
import tabulate

DEBUG=False
WIDE=False

TOKEN = os.environ['PACKET_TOKEN']

manager = packet.Manager(auth_token=TOKEN)

ATTRMAP = {
    packet.Project: ['name', 'id'],
    packet.OperatingSystem: ['name', 'id'],
    packet.SSHKey: ['label', 'id', 'key'],
    packet.Plan: ['name','id', 'slug'],
    packet.Device: ['hostname','id', 'operating_system', 'state', ('addresses',
                     lambda r: [r['address'] for r in r.ip_addresses])],
    #packet.Facilty: ['name','code', 'id', 'features'],
    }

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

def get_headers(cl):
    if DEBUG:
        print("getting headers of", cl)
    ret = []
    for i in ATTRMAP[cl]:
        if type(i) is str:
            ret.append(i)
        elif type(i) is tuple:
            ret.append(i[0])
    return ret

def cut(s):
    if not WIDE:
        return s[:36]
    else:
        return s

def colorize(l):
    return [f(cut(str(i))) for f,i in zip(color_loop(), l)]

def attrget(res):
    if DEBUG:
        print('attrget of',type(res), res)
    ret = []
    for i in ATTRMAP[type(res)]:
        if type(i) is tuple:
            # i[1] should be a function extracting some info from the resource
            _item = i[1](res)
        else:
            _item = getattr(res, i)
        ret.append(_item)
    return ret


def show_res(r):
    if DEBUG:
        print("about to show", r)
    if type(r) is list:
        if len(r) == 0:
            print("Empty list")
            return
        header = colorize(get_headers(type(r[0])))
        tab_list = [attrget(i) for i in r]
        tab_list_color = [colorize(i) for i in tab_list]
        print(tabulate.tabulate(tab_list_color, headers=header))
    elif type(r) in ATTRMAP.keys():
        header = colorize(get_headers(type(r)))
        tab_list_color = [colorize(attrget(r))]
        print(tabulate.tabulate(tab_list_color, headers=header))
    else:
        pprint.pprint(r)


def deco(f):
    def decorated_fun(*args,**kwargs):
        for a in ['d', 'debug']:
            if a in kwargs:
                global DEBUG
                DEBUG=kwargs.pop(a)
        for a in ['w', 'wide']:
            if a in kwargs:
                global WIDE
                WIDE=kwargs.pop(a)
        out = f(*args, **kwargs)
        if DEBUG:
            print(type(out))
        show_res(out)
         
    decorated_fun.__name__ = f.__name__
    return decorated_fun


if __name__ == "__main__":
    exposed_methods = [deco(m[1]) for m in methods]
    parser = argh.ArghParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-w', '--wide', action='store_true')
    parser.add_commands(exposed_methods)
    parser.dispatch()


