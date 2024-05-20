#!/bin/bash

set -e

conda create --name canvas-scripts python=3.11 --yes
conda activate canvas-scripts
pip install -r requirements.txt

read -p "Setup complete. Press any key to continue..."
