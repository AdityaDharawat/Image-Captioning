import streamlit as st
from PIL import Image
import os
import base64
import time
from generate_caption import generate_caption  # Your caption generation function

# Set page config
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# Lottie animation loader
def load_lottie_animation(path):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return base64.b64encode(f.read().encode()).decode()
        return None
    except Exception:
        return None

# App header
st.markdown("""
<div class="header">
    <h1 class="gradient-text">🧠 AI Image Caption Generator</h1>
    <p class="subheader">Transform your images into descriptive captions with our advanced deep learning model</p>
</div>
""", unsafe_allow_html=True)

# Lottie animation
lottie_b64 = load_lottie_animation("assets/animation.json")
if lottie_b64:
    st.markdown(f"""
    <div class="lottie-container">
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player 
            src="data:application/json;base64,{lottie_b64}"
            background="transparent" 
            speed="1" 
            style="width: 200px; height: 200px;" 
            loop 
            autoplay>
        </lottie-player>
    </div>
    """, unsafe_allow_html=True)

# Main content
with st.container():
    # Upload section
    with st.expander("📤 Upload Image", expanded=True):
        st.markdown("""
        <div class="upload-instructions">
            <p>Upload an image (JPG, PNG, JPEG) and our AI will generate a descriptive caption.</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            " ",
            type=["jpg", "jpeg", "png"],
            key="file_uploader",
            label_visibility="collapsed"
        )
    
    # Image processing
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.markdown("""
            <div class="image-container animate__animated animate__fadeIn">
            """, unsafe_allow_html=True)
            
            st.image(
                image,
                use_column_width=True,
                caption="Your uploaded image",
                output_format="auto"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(
                    "✨ Generate Caption",
                    key="generate_btn",
                    help="Click to generate a caption for your image"
                ):
                    with st.spinner(""):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for percent_complete in range(0, 101, 20):
                            status_text.markdown(f"""
                            <div class="progress-text">
                                <p>Analyzing image... {percent_complete}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                            progress_bar.progress(percent_complete)
                            time.sleep(0.1)
                        
                        temp_image_path = "temp_image.jpg"
                        image.save(temp_image_path)
                        caption = generate_caption(temp_image_path, beam_index=5)
                        
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.markdown("""
                        <div class="results-container animate__animated animate__fadeInUp">
                            <h3 class="results-title">📝 Generated Caption</h3>
                            <div class="caption-box">
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f'<p class="caption-text">{caption}</p>', unsafe_allow_html=True)
                        
                        st.markdown("""
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                if st.button(
                    "🔄 Try Another Image",
                    key="reset_btn",
                    help="Upload a different image"
                ):
                    st.experimental_rerun()
                    
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p>Powered by Deep Learning & Streamlit</p>
</div>
""", unsafe_allow_html=True)