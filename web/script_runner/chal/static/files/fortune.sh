#!/bin/sh
/usr/games/fortune | /usr/games/cowsay -f $(ls /usr/share/cowsay/cows/ | shuf -n1)
