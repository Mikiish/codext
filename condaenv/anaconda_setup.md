## Installing Anaconda3

```bash
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh
```

Visit https://www.anaconda.com/docs/getting-started/anaconda/install#macos-linux-installation:manual-shell-initialization for more information on how to setup conda env.

## Installing PyTorch with pip.

Once conda env is installed, open a conda environnement using condatorch.sh script then install pytorch with the following command :
```bash
sudo apt update
pip3 install wheel setuptools
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.4/
```

Create and activate conda environnement with the following command :
```bash
conda init --all
conda create -y -n condatorch torch
conda activate condatorch
```

Run the following command to activate conda automatically.
```bash
conda config --set auto_activate_base True
```

Once nightly ROCm6.4 PyTorch is installed, you can install MIOpen for additionnal machine learning primitives :
First download the script, then run it with the provided arguments. You can check your GFX architecture on the link below. Note that LLVM target depends on your hardware specifications.
[https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-gpus]
Run the following command to see your uarch : `rocminfo | grep gfx`

```bash
wget https://raw.githubusercontent.com/wiki/ROCm/pytorch/files/install_kdb_files_for_pytorch_wheels.sh
```
Run the scripts : 
```bash
export GFX_ARCH=gfx942
export ROCM_VERSION=6.4.1
./install_kdb_files_for_pytorch_wheels.sh
```

## Using the PyTorch ROCm base Docker image.

Start a docker container :
```bash
docker pull rocm/pytorch:latest-base
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --device=/dev/kfd --device=/dev/dri --group-add video --ipc=host --shm-size 8G rocm/pytorch:latest-base
```
Then run the following script inside the docker container.
```bash
cd ~
git clone https://github.com/pytorch/pytorch.git
cd pytorch
git submodule update --init --recursive
export PYTORCH_ROCM_ARCH=gfx942
.ci/pytorch/build.sh
```

Then run the command `echo $?`

---

From a new terminal you can use the following command to check if PyTorch is working.
`python3 -c 'import torch; print(torch.cuda.is_available())'`

Check all info on official doc : [https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-wheels-package]

