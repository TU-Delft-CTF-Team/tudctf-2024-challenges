#!/bin/sh
socat TCP-LISTEN:50011,fork EXEC:'python3 ./good_luck_and_who_knows.py',stderr,pty,echo=0
