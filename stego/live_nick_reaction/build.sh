#!/bin/sh

OUTER_ZIP_PASSWORD="I_D0NT_W4NT_Y0UR_D4MN_L3M0N5"
INNER_ZIP_PASSWORD="d0ntM4k3L3m0n4d3"

(cd PiSSTVpp; make; cp pisstvpp ..)
./pisstvpp -r 23000 -p m1 flag.png && mv flag.png.wav Martin_1.wav
zip --password $INNER_ZIP_PASSWORD final.zip doge.gif note.txt Martin_1.wav

python3 embed_lsb.py
zip --password $OUTER_ZIP_PASSWORD archive.zip warning.txt lyrics.txt ew.png yo.png final.zip

ffmpeg -i More\ Layers\ in\ Sight\ jazz.mp3 -acodec pcm_s16le -ar 44100 -af "channelsplit=channel_layout=stereo:channels=FL" sound.wav
python3 embed_spectrogram.py
zip outer.zip song.wav archive.zip
cat orig.png outer.zip > live_nick_reaction.png