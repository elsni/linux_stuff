#!/bin/bash
echo "Get a patched ST terminal emulator"
sudo apt install git build-essential pkg-config  libx11-dev libfontconfig1-dev libxft-dev
cd ../..

git clone https://git.suckless.org/st

cd st
wget https://st.suckless.org/patches/scrollback/st-scrollback-ringbuffer-0.8.5.diff
cp ../linux_stuff/tools/visualbell.diff .

patch -p1 < st-scrollback-ringbuffer-0.8.5.diff
patch -p1 < visualbell.diff

echo "all patches applied correctly?"
echo "if not, match the rejection files and apply manually "
echo "then change to ../../st"
echo "and do a 'sudo make clean install'"
