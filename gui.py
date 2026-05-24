import streamlit as st
import os

# Argument variables
obj_path = "data/source_meshes/vase.obj"  
n_iter = 800  
n_augs = 0
prompt = ""
image_path = ""
lmda = 1
style_embed = False
image_geo = True
output_dir = "./Results2/test3_imageonly"
no_prompt = False

st.markdown("""
    <style>
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

left, right = st.columns([1, 3], gap="large")

with left:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)

    # Text prompt and toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left">📝 Text Prompt</div>
    """, unsafe_allow_html=True)
    text_toggle = st.toggle(" ", key="text_toggle", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # text input area
    if text_toggle:
        text_prompt = st.text_area(
            "Describe the model and how you would like it to look",
            key="text_prompt_area",
            height=150,
            width=300
        )

    st.write("")  # spacing

    # Image prompt and toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left">📷 Image</div>
    """, unsafe_allow_html=True)
    image_toggle = st.toggle(" ", key="image_toggle", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # image upload box
    if image_toggle:
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Extract Image Style toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left"  style="font-weight: 400; font-size: 0.95rem;">🎨 Extract Image Style</div>
    """, unsafe_allow_html=True)
    extract_style_toggle = st.toggle(" ", key="extract_style_toggle", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # Image Affects Geo toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left"  style="font-weight: 400; font-size: 0.95rem;">🌍 Image Affects Geo</div>
    """, unsafe_allow_html=True)
    affects_geo_toggle = st.toggle(" ", key="affects_geo_toggle", label_visibility="collapsed")
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
        " ",
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


    if st.button("✨ Generate Model"):
        if text_toggle:
            text_prompt = st.session_state.text_prompt_area
            st.write(f"Text prompt saved: {text_prompt}")
            st.session_state.text_prompt_value = ""
        else:
            no_prompt = True

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
        st.write(f"Style Embed: {style_embed}")

        if affects_geo_toggle:
            image_geo = True
        else:
            image_geo = False
        st.write(f"Image Geo: {image_geo}")

        lmda = st.session_state.blend_slider
        st.write(f"Lambda value: {lmda}")

        n_iter = st.session_state.num_iterations
        st.write(f"n_iterations: {n_iter}")

        n_augs = st.session_state.num_augmentations
        st.write(f"n_augmentations: {n_augs}")
