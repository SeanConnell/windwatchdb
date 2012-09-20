#!/bin/bash
#Do this as root and pick size, that example is 8M
sudo mkfs -q /dev/ram1 8192
sudo mkdir -p /ramcache
sudo mount /dev/ram1 /ramcache
sudo chown -R sean /ramcache
