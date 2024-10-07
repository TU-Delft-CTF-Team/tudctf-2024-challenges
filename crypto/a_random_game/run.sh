#!/bin/sh
socat TCP-LISTEN:50021,fork EXEC:'python3 ./challenge.py',stderr,pty,echo=0
