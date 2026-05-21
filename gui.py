import streamlit as st

st.markdown("""
    <style>
        .left-col {
            width: 100px !important;
            min-width: 100px !important;
            max-width: 280px !important;
            padding-right: 20px;
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
    </style>
""", unsafe_allow_html=True)

left, right = st.columns([1, 3], gap="large")

with left:
    st.markdown('<div class="left-col">', unsafe_allow_html=True)

    # Text prompt and toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left">📝 Text Prompt</div>
        </div>
    """, unsafe_allow_html=True)
    text_toggle = st.toggle(" ", key="text_toggle")

    st.write("")  # spacing

    # Image prompt and toggle
    st.markdown("""
        <div class="title-row">
            <div class="title-left">📷 Image</div>
        </div>
    """, unsafe_allow_html=True)
    image_toggle = st.toggle(" ", key="image_toggle")

    # image upload box
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    st.markdown('</div>', unsafe_allow_html=True)
