import streamlit as st
import os
import re
import subprocess
from commands import run_main, build_video

# Argument variables
obj_path = "data/source_meshes/vase.obj"  
n_iter = 800  
n_augs = 1
prompt = ""
image_path = ""
lmda = 1
style_embed = False
image_geo = True
output_dir = ""
no_prompt = False

# Set source mesh location
obj_files = [
    f for f in os.listdir("data/source_meshes")
    if os.path.isfile(os.path.join("data/source_meshes", f))
]

# -- Helpers --
def get_next_output_dir(base="GUIResults"):
    os.makedirs(base, exist_ok=True) # make directory if not existing

    existing = [
        d for d in os.listdir(base)
        if os.path.isdir(os.path.join(base, d)) and re.match(r"render\d+", d)
    ]

    if not existing:
        n = 1 # Create new folder if "base" is empty
    else:
        # Find folder with greatest n value in "render{n}"
        nums = [int(re.findall(r"\d+", d)[0]) for d in existing]
        n = max(nums) + 1

    output_dir = os.path.join(base, f"render{n}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# -- Structure Helpers --
def toggle_row(icon, label, key):
    row = st.container()
    with row:
        st.markdown(f"""
            <div class="title-row" style="display:flex; justify-content:space-between; align-items:center;">
                <div class="title-left">{icon} {label}</div>
            </div>
        """, unsafe_allow_html=True)
        return st.toggle("", key=key, label_visibility="collapsed")

st.markdown("""
    <style>
        [data-testid="stMainBlockContainer"]:first-child {
            max-width: 100% !important;
        }

        [data-testid="stColumn"]:first-child {
            flex: 0 0 350px !important;
            min-width: 250px !important;
            max-width: 350px !important;
        }

        .left-col {
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            padding-right: 20px;
            flex: non !important;
        }
        .title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        .title-left {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .css-1d391kg, [data-testid="column"] {
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            flex: none !important;
        }
    </style>
""", unsafe_allow_html=True)

left, right = st.columns([1, 3], gap="small")

with left:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)

    # Choose model
    row = st.container()
    with row:
        st.markdown(f"""
            <div class="title-row" style="display:flex; justify-content:space-between; align-items:center;">
                <div class="title-left">☀️ Choose Mesh</div>
            </div>
        """, unsafe_allow_html=True)
    
    selected_obj = st.selectbox(
        "Select Object",
        obj_files,
        key="obj_selector"
    )

    # Upload mesh button
    upload_mesh = st.file_uploader(
        "Upload Mesh (.obj)",
        type=["obj"],
        key="mesh_uploader"
    )
    # Upload mesh on input
    if upload_mesh is not None:
        mesh_path = os.path.join("data/source_meshes", upload_mesh.name)

        with open(mesh_path, "wb") as f:
            f.write(upload_mesh.getbuffer())

        st.success(f"Uploaded {upload_mesh.name} successfully!")

        # Add object name to drop down
        obj_files.append(upload_mesh.name)

    # Text prompt and toggle
    text_toggle = toggle_row("📝", "Text Prompt", "text_toggle")

    # text input area
    if text_toggle:
        text_prompt = st.text_area(
            "",
            label_visibility="collapsed",
            placeholder="Describe the model and how you would like it to look",
            key="text_prompt_area",
            height=150,
            width="stretch",
        )

    st.write("")  # spacing

    # Image prompt and toggle
    image_toggle = toggle_row("📷", "Image", "image_toggle")

    # image upload box
    if image_toggle:
        uploaded_image = st.file_uploader(
            "Upload an image", 
            type=["png", "jpg", "jpeg"]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Extract Image Style toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left"  style="font-weight: 400; font-size: 0.95rem;">🎨 Extract Image Style</div>
    """, unsafe_allow_html=True)
    extract_style_toggle = st.toggle("", key="extract_style_toggle", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # Image Affects Geo toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left"  style="font-weight: 400; font-size: 0.95rem;">🌍 Image Affects Geo</div>
    """, unsafe_allow_html=True)
    affects_geo_toggle = st.toggle("", key="affects_geo_toggle", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)    


    # Blend lambda slider
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.9rem;">📝</span>
            <span style="font-weight: 500; font-size: 0.95rem;">Blend</span>
            <span style="font-size: 0.9rem;">📷</span>
        </div>
    """, unsafe_allow_html=True)

    blend_value = st.slider(
        "Blend",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        label_visibility="collapsed",
        key="blend_slider"
    )


    # Advanced settings
    st.markdown("""
        <div class="title-row" style="margin-top: 10px;">
            <div class="title-left" style="font-weight: 400; font-size: 0.95rem;">
                ⚙️ Advanced Settings
            </div>
    """, unsafe_allow_html=True)

    advanced_toggle = st.toggle(
        "",
        key="advanced_toggle",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # advanced settings options
    if advanced_toggle:
        number_iterations = st.number_input(
            "Number of Iterations",
            min_value=1,
            max_value=10000,
            value=1000,
            step=1,
            key="num_iterations"
        )

        number_augmentations = st.number_input(
            "Number of Augmentations",
            min_value=0,
            max_value=100,
            value=1,
            step=1,
            key="num_augmentations"
        )

# Generate Button
    if st.button("✨ Generate Model"):
        # Set obj mesh path
        obj_path = os.path.join("data/source_meshes", st.session_state.obj_selector)
        # st.write(f"Object selected: {obj_path}")

        # Set output path
        output_dir = get_next_output_dir()

        # Set prompt
        if text_toggle:
            text_prompt = st.session_state.text_prompt_area
            # st.write(f"Text prompt saved: {text_prompt}")
            st.session_state.text_prompt_value = ""
        else:
            no_prompt = True

        # Set image path
        if image_toggle and uploaded_image is not None:
            # Ensure directory exists
            os.makedirs("input_image", exist_ok=True)

            # relative path
            image_path = os.path.join("input_image", uploaded_image.name)

            # save file
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

            st.success(f"Image saved to: {image_path}")
        elif image_toggle:
            image_path = None

        if extract_style_toggle:
            style_embed = True
        else:
            style_embed = False
        # st.write(f"Style Embed: {style_embed}")

        if affects_geo_toggle:
            image_geo = True
        else:
            image_geo = False

        # st.write(f"Image Geo: {image_geo}")

        lmda = st.session_state.blend_slider
        # st.write(f"Lambda value: {lmda}")

        n_iter = st.session_state.num_iterations
        # st.write(f"n_iterations: {n_iter}")

        n_augs = st.session_state.num_augmentations
        # st.write(f"n_augmentations: {n_augs}")

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.write("Starting model...")      

        # Run main.py
        cmd = run_main(
            obj_path=obj_path,
            output_dir=output_dir,
            prompt=text_prompt,
            no_prompt=no_prompt,
            lmda=lmda,
            image_path=image_path,
            image_geo=image_geo,
            style_embed=style_embed,
            n_iter=n_iter,
            n_augs=n_augs
        )

        # Catch cmd errors
        if cmd is None:
            st.error("run_main returned None - cannot run subprocess")
            st.stop()
        
        if not isinstance(cmd, list):
            st.error(f"Ensure cmd is a list, got type: {type(cmd)}")
            st.stop()

        process = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )

        # Update progress bar based on lines output
        progress = 0
        for line in process.stdout:
            if "it/s" in line or "%" in line:
                continue # skip tqdm output lines

            progress = min(progress + 1, 100)
            progress_bar.progress(progress)
            status_text.write(line)

        stderr = process.stderr.read()

        progress_bar.progress(100)

        process.wait()

        mp4_path = build_video(output_dir, n_iter)


        # --- Right Side Column ---
        with right:
            # Video Player
            st.subheader("Model Preview")
            if mp4_path and os.path.exists(mp4_path):
                with open(mp4_path, "rb") as f:
                    st.video(f.read())
            else:
                st.info("Model will be displayed here once generated")
            
            # error output
            if stderr:
                st.error(stderr)

