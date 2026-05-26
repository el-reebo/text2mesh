#!/bin/bash
set -e

sudo apt-get update

sudo apt-get install -y libgl1 libglu1-mesa libxrender1 libxkbcommon-x11-0

conda env create -f text2meshV2.yml

source $(conda info --base)/etc/profile.d/conda.sh
conda activate text2meshV2

pip install kaolin==0.15.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.1.0_cu121.html && \
pip install jupyter-client==7.4.9

pip install git+https://github.com/openai/CLIP.git

python -m ipykernel install --user --name t2m --display-name "Python (t2m)"

echo "Installed text2mesh conda environment & additional dependencies."

