#!/bin/sh
socat TCP-LISTEN:50011,fork EXEC:'python3 ./printer.py',stderr,pty,echo=0
