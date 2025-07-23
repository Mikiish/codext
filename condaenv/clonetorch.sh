#!/bin/bash
set -e
cd ~
git clone https://github.com/pytorch/pytorch.git
cd pytorch
git submodule update --init --recursive

### Find your version using rocm-info
export PYTORCH_ROCM_ARCH=gfx1100
