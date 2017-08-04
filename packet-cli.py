#!/usr/bin/env python3

import packet
import os
import argh
import inspect
import pprint
import tabulate
import yaml

DEBUG=False
WIDE=False

TOKEN = os.environ['PACKET_API_TOKEN']

manager = packet.Manager(auth_token=TOKEN)

# if you disagree with displayed attributes of resources, just change this
# dict. You can see relevant source code in
# https://github.com/packethost/packet-python/tree/master/packet

ATTRMAP = {
    packet.Project: ['name', 'id'],
    packet.OperatingSystem: ['name','slug'],
    packet.SSHKey: ['label', 'id', 'key'],
    packet.Plan: ['name','id', 'slug'],
    packet.Device: ['hostname','id', 'operating_system',
           ('facility', lambda d: d.facility['code']),
           ('plan', lambda d: d.plan['slug']),
           'state', 
           'locked',
           ('addresses', lambda r: [r['address'] for r in r.ip_addresses])],
    packet.Facility: ['name','code', 'id', 'features'],
    packet.Volume: ['description','id', 'size', 'billing_cycle', 'attached_to'],
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

def get_dict(obj):
    return {name: getattr(obj, name) for name in dir(obj)
            if not name.startswith('__')} 

def show_res(r):
    if type(r) is list:
        if len(r) == 0:
            print("Empty list")
            return
        if DEBUG:
            print("about to show", r[0])
            pprint.pprint([get_dict(i) for i in r])
        header = colorize(get_headers(type(r[0])))
        tab_list = [attrget(i) for i in r]
        tab_list_color = [colorize(i) for i in tab_list]
        print(tabulate.tabulate(tab_list_color, headers=header))
    elif type(r) in ATTRMAP.keys():
        if DEBUG:
            print("about to show", r)
            pprint.pprint(get_dict(r))
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
        for a in ['p', 'params']:
            if a in kwargs:
                if kwargs[a] is None:
                    kwargs.pop(a)
                else:
                    _params = yaml.load(kwargs[a])
                    kwargs[a] = _params
        #args = list(args)
        #args[3] = int(args[3])
        if DEBUG:
            print("args", args)
            print("kwargs", kwargs)
        orig_fn_output = f(*args, **kwargs)
        if DEBUG:
            print(type(orig_fn_output))
        show_res(orig_fn_output)

    decorated_fun.__name__ = f.__name__
    return decorated_fun


def wipe_devices(project_id):
    ds = manager.list_devices(project_id)
    for d in ds:
        m = "devices/%s" % d.id
        if d.locked:
            manager.call_api(m, "PATCH", {"locked": False})
        manager.call_api(m, "DELETE")

def wipe_volumes(project_id):
    vs = manager.list_volumes(project_id)
    for v in vs:
        v.delete()


if __name__ == "__main__":
    exposed_methods = [deco(m[1]) for m in methods]
    exposed_methods.append(wipe_devices)
    exposed_methods.append(wipe_volumes)
    parser = argh.ArghParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-w', '--wide', action='store_true')
    parser.add_argument('-p', '--params')
    parser.add_commands(exposed_methods)
    try:
        parser.dispatch()
    except packet.baseapi.Error as e:
        print(e)
        print(", ".join(e._cause.response.json()['errors']))



