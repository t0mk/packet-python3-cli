# packet-python3-cli

Simple cli for packet cloud done with Argh from packet-python. It's just exposing the methods of the manager class from https://github.com/packethost/packet-python/blob/master/packet/Manager.py to command line arguments.

## Usage

```
$ packet-cli list-projects                                    
Ansible and Packet 89b497ee-5afc-420a-8fb5-364634634634

$ packet-cli list-devices 89b497ee-5afc-420a-8fb5-36463463463
anstest2 4bae1675-9fc6-4d64-bf81-fbf506a08cb1 ubuntu_16_04_image Ubuntu 16.04 LTS ubuntu 16.04 active ['147.75.101.83', '2604:1380:2001:1d00::1', '10.80.93.129']A

$ packet-cli create-device 89b497ee-5afc-420a-8fb5-36463463463 anstest3 baremetal_0 ams1 ubuntu_16_04_image
anstest3 db9f035b-cab5-420d-bb68-c5e17d23f507 ubuntu_16_04_image Ubuntu 16.04 LTS ubuntu 16.04 queued []


```
