# packet-python3-cli

Simple cli for packet cloud done with Argh from packet-python. It's just exposing the methods of the manager class from https://github.com/packethost/packet-python/blob/master/packet/Manager.py to command line arguments.

## Installation

You will need pip3 packages:

```
$ pip3 install packet-python argh tabulate
```

## Example Usage

You will need your API token exported in env var PACKET\_TOKEN

```
$ packet-cli help
$ packet-cli list-projects
$ packet-cli list-devices 89b497ee-5afc-420a-8fb5-56984898f444
$ packet-cli list-plans
$ packet-cli list-facilities
$ packet-cli create-device 89b497ee-5afc-420a-8fb5-56984898f444 anstest88 baremetal_0 ams1 ubuntu_16_04_image
$ packet-cli call-api /devices/6865479e-14d2-492d-ae61-e63dff813229 DELETE packet-cli list-facilities
```

