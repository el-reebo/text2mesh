conda env create -f text2meshV2.yml && \
conda activate text2mesh && \
python -m ipykernel install --user --name text2meshV2 --display-name "Python (text2meshV2)" && \
pip install kaolin==0.15.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.1.0_cu121.html && \
pip install git+https://github.com/openai/CLIP.git && \
pip install "transformers==4.46.3" && \
/venv/text2meshV2/bin/pip install opencv-python==4.8.0.76 && \
sudo apt-get update && \
sudo apt-get install -y libgl1 libglu1-mesa libxrender1 libxkbcommon-x11-0 && \
echo "Installed text2mesh conda environment & additional dependencies."


