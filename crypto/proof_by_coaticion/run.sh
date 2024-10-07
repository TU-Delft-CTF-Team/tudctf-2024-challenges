#!/bin/sh
socat TCP-LISTEN:50037,fork EXEC:'python3 ./source.py',stderr,pty,echo=0
