#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Updating package lists ---"
sudo apt-get update

echo "--- Installing required system libraries ---"
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libpango-1.0-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    libevent-2.1-7 \
    libwebpmux3 \
    libwebpdemux2 \
    libwebp7 \
    libminizip1 \
    libxslt1.1 \
    libtiff6
pip install PySide6

echo "--- Creating symbolic links for library version compatibility ---"

# Create symlink for libwebp (libwebp.so.6 -> libwebp.so.7)
if [ ! -L /usr/lib/aarch64-linux-gnu/libwebp.so.6 ]; then
    sudo ln -s /usr/lib/aarch64-linux-gnu/libwebp.so.7 /usr/lib/aarch64-linux-gnu/libwebp.so.6
    echo "Created symlink for libwebp."
else
    echo "Symlink for libwebp already exists."
fi

# Create symlink for libtiff (libtiff.so.5 -> libtiff.so.6)
if [ ! -L /usr/lib/aarch64-linux-gnu/libtiff.so.5 ]; then
    sudo ln -s /usr/lib/aarch64-linux-gnu/libtiff.so.6 /usr/lib/aarch64-linux-gnu/libtiff.so.5
    echo "Created symlink for libtiff."
else
    echo "Symlink for libtiff already exists."
fi

echo "--- Environment setup complete! ---"
