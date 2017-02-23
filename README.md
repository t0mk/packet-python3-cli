# packet-python3-cli

Simple cli for packet cloud done with Argh from packet-python. It's just exposing the methods of the manager class from https://github.com/packethost/packet-python/blob/master/packet/Manager.py to command line arguments.

## Installation

You will need pip3 packages:

```
$ pip3 install packet-python argh tabulate
```

## Usage demo

[![asciicast](https://asciinema.org/a/0hrjxjw72tl77mi4i8dhk1f1p.png)](https://asciinema.org/a/0hrjxjw72tl77mi4i8dhk1f1p)

## Example Usage

You will need your API token exported in env var PACKET\_API\_TOKEN

```
$ packet-cli help
$ packet-cli list-projects

# list devices in a project
$ packet-cli list-devices 89b497ee-5afc-420a-8fb5-56984898f444

# list available plan, facilities and operating systems
$ packet-cli list-plans
$ packet-cli list-facilities
$ packet-cli list-operating-systems

# create device in a project, there's name, plan, faciltiy and OS
$ packet-cli create-device 89b497ee-5afc-420a-8fb5-56984898f444 anstest88 baremetal_0 ams1 ubuntu_16_04_image

# power off device:
$ packet-cli -p "{type: power_off }" call-api /devices/95108175-2b85-48e1-bf3f-81a4a4b21131/actions POST

# remove device
$ packet-cli call-api /devices/6865479e-14d2-492d-ae61-e63dff813229 DELETE

# lock device
$ packet-cli --params "{locked : true }" call-api devices/d39ecd03-d5df-4252-8bc6-f558d53a86bf PATCH

# create new SSH key
$ packet-cli create-ssh-key newkeylabel "`cat keys/key.pub`"
```

