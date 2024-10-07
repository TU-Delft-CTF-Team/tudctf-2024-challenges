#!/bin/sh

gcc printing.c -o printing -fstack-protector -Wl,-z,relro,-z,now
