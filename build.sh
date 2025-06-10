#!/bin/bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

source $HOME/.local/bin/activate

make install
make migrate
make collectstatic