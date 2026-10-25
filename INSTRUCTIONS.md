# Text2Mesh — Setup Guide

---

## Requirements

### Hardware
- NVIDIA CUDA-capable GPU with a minimum of **8 GB VRAM**
- CUDA 11 compatible drivers

> **50-series GPUs (RTX 5000 series) are not currently supported.** Dependency compatibility issues prevent the environment from running correctly on these cards. Use a 40-series or earlier GPU.

### Software
- Linux 
- Anaconda or Miniconda
- Git

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/text2mesh.git
cd text2mesh
```

**2. Run the setup script**

```bash
bash setup-text2mesh.sh
```

---

## Running the GUI

The GUI provides a simple web interface for running stylisations without writing any code.

**1.** In your terminal, go to the Ports tab (next to the Terminal tab)

**2.** Add port `8501`

**3.** Start the Streamlit server:

```bash
streamlit run gui.py --server.address 0.0.0.0 --server.port 8501
```

**4.** Open `http://localhost:8501` in your browser

---

## Running via Jupyter Notebook

The notebook interface gives more fine-grained control over all parameters.

**1.** Open `colab_demo.ipynb`

**2.** Set the kernel to **Python (t2m)**

**3.** Run the first cell to verify the environment is working correctly

**4.** Scroll to the **"Main Argument Inputs"** section and fill in your desired values:
- `obj_path` — path to your input `.obj` mesh
- `prompt` — text description of the target style (e.g. `"a chair made of wood"`)
- `output_dir` — where results will be saved
- Any additional optional parameters

**5.** Run that cell to save the variables

**6.** Run the **"Run Main"** cell to begin stylisation — this may take several minutes depending on iteration count and hardware

**7.** Once complete, run the two cells under **"Showcase Results"** in order to visualise the output renders and stylised mesh

---

## Output

Results are saved to your specified `output_dir` and include:
- Stylised `.obj` file with vertex colours and displacements
- Rendered views at checkpoints during training
- A loss curve plot
- A text file recording the prompt used
- A text filed recording the caption generated if using **style-embed**

---
