#!/bin/bash
set -e

source ~/anaconda3/bin/activate
pip3 install -qq --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.4/

conda config --set auto_activate_base True
conda create -y -n condatorch
conda activate condatorch

