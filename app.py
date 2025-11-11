import streamlit as st
from colorthief import ColorThief
import pandas as pd
import tempfile
import os
import base64

# Configure the page
st.set_page_config(
    page_title="PurpleStore — Hijab Color Matcher",
    page_icon="🧕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Landing Page Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Poppins:wght@400;600;700;800&family=Caveat:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Light beige background */
    .stApp {
        background: #F5F1E8 !important;
    }
    
    /* Remove default Streamlit padding/margins */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Remove gaps in columns */
    [data-testid="column"] {
        padding: 0 !important;
    }
    
    /* Decorative elements */
    .landing-page {
        position: relative;
        padding: 0;
        margin: 0;
        overflow: hidden;
    }
    
    .landing-page::before {
        content: '';
        position: absolute;
        top: 10%;
        right: 5%;
        width: 150px;
        height: 150px;
        background: rgba(201, 168, 217, 0.2);
        border-radius: 50%;
        z-index: 0;
    }
    
    .landing-page::after {
        content: '';
        position: absolute;
        bottom: 15%;
        left: 8%;
        width: 100px;
        height: 100px;
        background: rgba(201, 168, 217, 0.15);
        border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
        z-index: 0;
    }
    
    /* Left Section Styles */
    .landing-left {
        position: relative;
        z-index: 1;
        padding: 0;
        margin-top: 1rem;
    }
    
    .brand-box {
        display: inline-block;
        background: #E8D5F2;
        padding: 0.4rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .brand-text {
        font-size: 1.5rem;
        font-weight: 800;
        color: #000;
        letter-spacing: 0.05em;
        margin: 0;
    }
    
    .tagline-container {
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .tagline-text {
        font-size: 1.8rem;
        font-weight: 700;
        color: #000;
        margin: 0;
    }
    
    .tagline-highlight {
        display: inline-block;
        background: #E8D5F2;
        padding: 0.3rem 1rem;
        border-radius: 12px;
        margin: 0.2rem 0;
    }
    
    .upload-btn {
        background: linear-gradient(135deg, #C9A8D9 0%, #A87DC0 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 125, 192, 0.3);
        margin-top: 0.5rem;
    }
    
    .upload-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 125, 192, 0.4);
    }
    
    /* Style Streamlit button to match upload-btn design */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(135deg, #C9A8D9 0%, #A87DC0 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 30px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        box-shadow: 0 4px 15px rgba(168, 125, 192, 0.3) !important;
        transition: all 0.3s ease !important;
        width: auto !important;
    }
    
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 125, 192, 0.4) !important;
    }
    
    /* Right Section Styles */
    .landing-right {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0;
        margin-top: 1rem;
    }
    
    .available-colors-text {
        font-family: 'Caveat', cursive;
        font-size: 1.5rem;
        font-weight: 600;
        color: #000;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .dotted-arrow {
        position: absolute;
        width: 120px;
        height: 80px;
        z-index: 1;
        margin-top: -20px;
        margin-left: 150px;
    }
    
    .dotted-arrow svg {
        width: 100%;
        height: 100%;
    }
    
    .phone-mockup {
        width: 240px;
        height: 480px;
        background: #000;
        border-radius: 30px;
        padding: 15px 12px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 2;
        margin-top: 0.5rem;
    }
    
    .phone-screen {
        width: 100%;
        height: 100%;
        background: #fff;
        border-radius: 25px;
        padding: 20px 15px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        overflow: hidden;
    }
    
    .hijab-display {
        flex: 1;
        display: flex;
        gap: 10px;
        align-items: stretch;
    }
    
    .hijab-item {
        flex: 1;
        position: relative;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .hijab-color {
        width: 100%;
        height: 100%;
    }
    
    .hijab-label {
        position: absolute;
        left: 5px;
        top: 50%;
        transform: translateY(-50%) rotate(-90deg);
        transform-origin: center;
        color: #000;
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    /* PurpleStore Header - Exact Match from Image */
    .top-grey-bar {
        background: #363636;
        height: 30px;
        width: 100%;
        margin: -1.5rem -1.5rem 0 -1.5rem;
        display: flex;
        align-items: center;
        padding: 0 2rem;
    }
    
    .main-header {
        background: #F8F5F9;
        padding: 1rem 2rem;
        margin: 0 -1.5rem 0 -1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-center {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .icon-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #E8E8E8;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        position: relative;
    }
    
    .icon-circle svg {
        width: 20px;
        height: 20px;
    }
    
    .badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #A87DC0;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .logo-image {
        max-height: 60px;
        height: auto;
        width: auto;
    }
    
    .contact-btn {
        background: #A87DC0;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .contact-btn:hover {
        background: #9568b0;
        transform: translateY(-1px);
    }
    
    .nav-bar {
        background: #C9A8D9;
        padding: 0.75rem 2rem;
        margin: 0 -1.5rem 0 -1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .nav-title {
        color: white;
        text-decoration: none;
        font-weight: 500;
        font-size: 1.1rem;
        text-align: center;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .hero-section {
        display: flex;
        gap: 4rem;
        align-items: flex-start;
        padding: 2rem 0;
    }
    
    .left-content {
        flex: 0 0 500px;
        max-width: 500px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: #000;
        margin: 0 0 1.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #666;
        line-height: 1.6;
        margin: 0 0 2.5rem 0;
    }
    
    .upload-section {
        margin-top: 2rem;
    }
    
    .upload-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #c59bd1;
        margin: 0 0 0.5rem 0;
    }
    
    .upload-subtitle {
        font-size: 0.95rem;
        color: #666;
        margin: 0 0 1.5rem 0;
        line-height: 1.5;
    }
    
    .right-content {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .color-mockup {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        max-width: 500px;
    }
    
    .color-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .color-swatch {
        aspect-ratio: 1;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .color-swatch:hover {
        transform: scale(1.05);
    }
    
    .result-container {
        display: flex;
        gap: 2rem;
        margin-top: 2rem;
        align-items: flex-start;
    }
    
    .result-left {
        flex: 0 0 280px;
    }
    
    .result-right {
        flex: 1;
        min-width: 0;
    }
    
    @media (max-width: 768px) {
        .hero-section {
            flex-direction: column;
            gap: 2rem;
        }
        
        .left-content {
            flex: 1;
            max-width: 100%;
        }
        
        .result-container {
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .result-left {
            flex: 1;
            width: 100%;
        }
    }
    
    .detected-palette {
        display: flex;
        gap: 0.75rem;
        margin: 1.5rem 0;
    }
    
    .palette-color {
        flex: 1;
        height: 80px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .recommendation-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .recommendation-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .recommendation-color {
        width: 100%;
        height: 60px;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }
    
    .shop-button {
        background: #c59bd1;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(197, 155, 209, 0.3);
        width: 100%;
        margin-top: 0.5rem;
    }
    
    .shop-button:hover {
        background: #b089c1;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(197, 155, 209, 0.4);
    }
    
    .stButton > button {
        background: #c59bd1;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(197, 155, 209, 0.3);
    }
    
    .stButton > button:hover {
        background: #b089c1;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(197, 155, 209, 0.4);
    }
    
    .image-preview {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        max-width: 100%;
    }
    
    .section-label {
        font-size: 0.85rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load hijab catalog
@st.cache_data
def load_catalog():
    return pd.read_csv("hijab_catalog.csv")

catalog = load_catalog()

# Helper functions
def hex_to_rgb(hexstr):
    """Convert hex color to RGB tuple"""
    h = hexstr.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    """Calculate improved color distance using weighted RGB and perceptual differences"""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    
    r_mean = (r1 + r2) / 2
    delta_r = r1 - r2
    delta_g = g1 - g2
    delta_b = b1 - b2
    
    distance = (2 + r_mean/256) * delta_r**2 + 4 * delta_g**2 + (2 + (255-r_mean)/256) * delta_b**2
    return distance**0.5

# PurpleStore Header - Exact Match from Image
# Check for logo file first - improved detection
logo_paths = [
    "PS LOGO.png", "PS LOGO.jpg", "PS LOGO.jpeg",
    "ps logo.png", "ps logo.jpg", "ps logo.jpeg",
    "PS_LOGO.png", "PS_LOGO.jpg", "PS_LOGO.jpeg",
    "logo.png", "logo.jpg", "logo.jpeg",
    "purplestore-logo.png", "purplestore-logo.jpg",
    "assets/logo.png", "assets/PS LOGO.png",
    "logo.svg"
]

logo_path = None
current_dir = os.getcwd()

# Check each path
for path in logo_paths:
    full_path = os.path.join(current_dir, path)
    if os.path.exists(full_path):
        logo_path = full_path
        break
    # Also check relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, path)
    if os.path.exists(script_path):
        logo_path = script_path
        break

# Build complete header HTML as single string
logo_html = ""
if logo_path:
    try:
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            logo_ext = logo_path.split('.')[-1].lower()
            if logo_ext == 'jpg':
                logo_ext = 'jpeg'
            logo_html = f'<img src="data:image/{logo_ext};base64,{logo_data}" class="logo-image" alt="PurpleStore Logo" style="max-height: 50px; width: auto; height: auto; display: block; margin: 0 auto; object-fit: contain;">'
    except Exception as e:
        # Fallback to relative path
        try:
            rel_path = os.path.relpath(logo_path, current_dir)
            logo_html = f'<img src="{rel_path}" class="logo-image" alt="PurpleStore Logo" style="max-height: 50px; width: auto; height: auto; display: block; margin: 0 auto; object-fit: contain;">'
        except:
            logo_html = '<div style="color: #A87DC0; font-weight: 700; font-size: 2.5rem; text-align: center; width: 100%;">Purple Store</div>'
else:
    logo_html = '<div style="color: #A87DC0; font-weight: 700; font-size: 2.5rem; text-align: center; width: 100%;">Purple Store</div>'

# Complete header HTML - build as single string
header_html = '<div class="main-header">'
header_html += '<div class="header-left"><div class="icon-circle"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg></div></div>'
header_html += '<div class="header-center">' + logo_html + '</div>'
header_html += '<div class="header-right">'
header_html += '<div class="icon-circle"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg><div class="badge">1</div></div>'
header_html += '<div class="icon-circle"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg><div class="badge">0</div></div>'
header_html += '<div class="icon-circle"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 12px; height: 12px; margin-left: -5px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg></div>'
header_html += '<button class="contact-btn">Contact Us</button>'
header_html += '</div></div>'

st.markdown(header_html, unsafe_allow_html=True)

# Navigation bar
st.markdown("""
<div class="nav-bar">
    <div class="nav-title">Hijab color matcher</div>
</div>
""", unsafe_allow_html=True)

# Main Landing Page Layout
st.markdown('<div class="landing-page">', unsafe_allow_html=True)

# Initialize session state for upload trigger
if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Check if file is uploaded - if not, show landing page
uploaded_file = st.session_state.uploaded_file

if uploaded_file is None:
    # Landing Page - Two Column Layout
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        # Left Section
        st.markdown("""
        <div class="landing-left">
            <div class="brand-box">
                <p class="brand-text">PURPLE STORE</p>
            </div>
            <div class="tagline-container">
                <p class="tagline-text">
                    find the <span class="tagline-highlight">perfect hijab color to match</span> your outfit!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload Button - triggers file uploader
        if st.button("UPLOAD A PHOTO", key="upload_trigger", use_container_width=False):
            st.session_state.show_uploader = True
            st.rerun()
        
        # Show uploader if triggered
        if st.session_state.show_uploader:
            uploaded_file = st.file_uploader(
                "Upload a photo", 
                type=['png', 'jpg', 'jpeg'],
                help="Upload a clear photo of your outfit",
                key="file_uploader_main"
            )
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.session_state.show_uploader = False
                st.rerun()
    
    with col2:
        # Right Section - Available Colors and Phone Mockup
        st.markdown("""
        <div class="landing-right">
            <div style="position: relative; display: inline-block;">
                <p class="available-colors-text">Available Colors</p>
                <div class="dotted-arrow">
                    <svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
                        <path d="M 10 40 Q 50 20, 90 30 T 110 40" 
                              stroke="#C9A8D9" 
                              stroke-width="2" 
                              fill="none" 
                              stroke-dasharray="5,5" 
                              stroke-linecap="round"/>
                        <polygon points="105,35 110,40 105,45" 
                                 fill="#C9A8D9"/>
                    </svg>
                </div>
            </div>
            <div class="phone-mockup">
                <div class="phone-screen">
                    <div class="hijab-display">
                        <div class="hijab-item">
                            <div class="hijab-color" style="background: #800020;"></div>
                            <div class="hijab-label">Maroon</div>
                        </div>
                        <div class="hijab-item">
                            <div class="hijab-color" style="background: #E6B8B7;"></div>
                            <div class="hijab-label">Dusky Pink</div>
                        </div>
                        <div class="hijab-item">
                            <div class="hijab-color" style="background: #228B22;"></div>
                            <div class="hijab-label">Forest Green</div>
                        </div>
                        <div class="hijab-item">
                            <div class="hijab-color" style="background: #BDB76B;"></div>
                            <div class="hijab-label">Khaki</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # File uploaded - show results
    uploaded_file = st.session_state.uploaded_file
    if uploaded_file is not None:
            # When photo is uploaded - show results on right side
            try:
                # Save uploaded file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name
                
                # Extract colors
                color_thief = ColorThief(tmp_file_path)
                dominant_color = color_thief.get_color(quality=10)
                dominant_hex = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
                palette = color_thief.get_palette(color_count=5, quality=10)
                
                # Find best matches
                catalog['rgb'] = catalog['hex'].apply(hex_to_rgb)
                distances = []
                for color in palette:
                    catalog['temp_distance'] = catalog['rgb'].apply(lambda r: color_distance(r, color))
                    distances.append(catalog['temp_distance'])
                
                catalog['distance'] = pd.concat(distances, axis=1).min(axis=1)
                in_stock = catalog[catalog['stock'] > 0].copy()
                if len(in_stock) > 0:
                    best_matches = in_stock.sort_values('distance').head(3)
                else:
                    best_matches = catalog.sort_values('distance').head(3)
                
                # Right side layout: Small image + colors + matches side by side
                st.markdown("""
                <div style="display: flex; gap: 1.5rem; align-items: flex-start; margin-top: 1rem;">
                """, unsafe_allow_html=True)
                
                # Left part: Small uploaded image (250-300px)
                st.markdown("""
                <div style="flex-shrink: 0;">
                """, unsafe_allow_html=True)
                st.image(uploaded_file, width=280, caption="")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Right part: Colors and matches
                st.markdown("""
                <div style="flex: 1; min-width: 0;">
                """, unsafe_allow_html=True)
                
                # Detected Colors section
                st.markdown("""
                <h3 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem; color: #c59bd1;">Detected Colors</h3>
                <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem;">
                """, unsafe_allow_html=True)
                
                # Show detected palette
                for i, color in enumerate(palette):
                    hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                    st.markdown(f"""
                    <div style="flex: 1; height: 50px; background: {hex_color}; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);"></div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Best Matches section
                st.markdown("""
                <h3 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem; color: #c59bd1;">Best Matches</h3>
                """, unsafe_allow_html=True)
                
                # Show top 3 recommendations in compact vertical list
                for i, (_, match) in enumerate(best_matches.iterrows()):
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 0.5rem;">
                        <div style="width: 50px; height: 50px; background: {match['hex']}; border-radius: 6px; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>
                        <div style="flex: 1;">
                            <p style="font-weight: 600; margin: 0; color: #000; font-size: 0.95rem;">{match['name']}</p>
                            <p style="color: #666; font-size: 0.85rem; margin: 0.25rem 0 0 0;">Stock: {match['stock']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Shop Now button
                best_match = best_matches.iloc[0]
                st.markdown("""
                <div style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
                if st.button("🛒 Shop Now", key="shop_main", use_container_width=True):
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={best_match["url"]}">', unsafe_allow_html=True)
                    st.success(f"Opening {best_match['name']}...")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Clean up
                os.unlink(tmp_file_path)
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Please make sure you've uploaded a valid image file (PNG, JPG, or JPEG).")

st.markdown('</div>', unsafe_allow_html=True)

# Minimal footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #999; font-size: 0.85rem; margin-top: 4rem;">
    Made with ❤️ for PurpleStore | Powered by Streamlit & ColorThief
</div>
""", unsafe_allow_html=True)
