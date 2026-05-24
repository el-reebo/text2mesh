import subprocess
import sys
import os

def run_main(obj_path="", output_dir="", prompt="", no_prompt=False, lmda=0, image_path="", image_geo=False, style_embed=False, n_iter=750, n_augs=1):
    # Flags
    image_flag = f"--image {image_path}" if image_path else ""
    image_geo_flag = "--image_geo" if image_geo else ""
    style_embed_flag = "--style_embed" if style_embed else ""
    no_prompt_flag = "--no_prompt" if no_prompt else ""

    cmd = [
        sys.executable, "main.py", "--run", "branch",
        "--obj_path", obj_path,
        "--output_dir", output_dir,
        "--prompt", prompt,
        "--lambda_style", str(lmda),
        "--sigma", "12.0",
        "--clamp", "tanh",
        "--n_normaugs", "4",
        "--n_augs", str(n_augs),
        "--normmincrop", "0.1",
        "--normmaxcrop", "0.4",
        "--geoloss",
        "--colordepth", "2",
        "--normdepth", "2",
        "--frontview",
        "--frontview_std", "4",
        "--clipavg", "view",
        "--lr_decay", "0.9",
        "--clamp", "tanh",
        "--normclamp", "tanh",
        "--maxcrop", "1.0",
        "--save_render",
        "--seed", "29",
        "--n_iter", str(n_iter),
        "--learning_rate", "0.0005",
        "--normal_learning_rate", "0.0005",
        "--standardize",
        "--no_pe",
        "--symmetry",
        "--background", "1", "1", "1"
    ]

    if image_flag:
        cmd.extend(["--image", image_path])

    if image_geo_flag:
        cmd.append("--image_geo")

    if style_embed_flag:
        cmd.append("--style_embed")

    if no_prompt_flag:
        cmd.append("--no_prompt")

    return cmd

def build_video(output_dir, n_iter, step=100, fps=2):
    import cv2
    import os

# Create video frames
    frames = []
    for i in range(0, n_iter, step):
        img = cv2.imread(os.path.join(output_dir, f"iter_{i}.jpg"))
        frames.append(img)

    if not frames: # if frames empty
        return None

# Create avi video
    avi_path = os.path.join(output_dir, "video.avi")
    mp4_path = os.path.join(output_dir, "video.mp4")

    height, width = frames[0].shape[:2]
    video = cv2.VideoWriter(
        avi_path,
        cv2.VideoWriter_fourcc(*"XVID"),
        fps,
        (width, height)
    )

    for f in frames:
        video.write(f)
    video.release()

# conver avi to mp4
    subprocess.run([
        "ffmpeg", "-y",
        "-i", avi_path,
        "-pix_fmt", "yuv420p",
        mp4_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # discard logs

    return mp4_path