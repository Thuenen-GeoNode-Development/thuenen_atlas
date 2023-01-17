#!/bin/bash -e

# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
source ~/.bashrc

# Configure node
nvm install v14.21.2
nvm use v14.21.2
