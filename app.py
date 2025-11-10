import streamlit as st
from colorthief import ColorThief
import pandas as pd
import tempfile
import os

# Configure the page
st.set_page_config(
    page_title="PurpleStore — Hijab Color Matcher",
    page_icon="🧕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Coolors-inspired minimal design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Modern Header */
    .top-header {
        background: #c59bd1;
        padding: 1.25rem 2.5rem;
        margin: -1.5rem -1.5rem 2rem -1.5rem;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        box-shadow: 0 2px 10px rgba(197, 155, 209, 0.2);
        min-height: 80px;
    }
    
    .header-content {
        text-align: right;
        color: white;
        animation: slideInRight 0.8s ease-out;
    }
    
    .header-brand {
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.01em;
    }
    
    .header-title {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 0.25rem 0;
        animation: fadeIn 1s ease-out 0.2s both;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        animation: fadeIn 1s ease-out 0.4s both;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
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

# Modern Header - Top bar with purple background
st.markdown("""
<div class="top-header">
    <div class="header-content">
        <div class="header-brand">PurpleStore</div>
        <div class="header-title">Hijab Color Matcher</div>
        <div class="header-subtitle">Find the perfect hijab color to match your outfit.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main layout - Coolors style
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hero section - Coolors style layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # Upload section - compact, left-aligned (header is now in top bar)
    st.markdown("""
    <div class="upload-section" style="margin-top: 0;">
        <h3 class="upload-title">📸 Upload Your Outfit Photo</h3>
        <p class="upload-subtitle">Upload a clear photo of your outfit to get personalized hijab color recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo of your outfit",
        key="file_uploader_main"
    )

    with col2:
        if uploaded_file is None:
            # Right side - Color grid mockup (like Coolors)
            st.markdown("""
            <div class="right-content">
                <div class="color-mockup">
                    <div class="section-label">Available Colors</div>
                    <div class="color-grid">
            """, unsafe_allow_html=True)
            
            # Show sample colors from catalog
            sample_colors = catalog.head(10)
            cols = st.columns(5)
            for i, (_, row) in enumerate(sample_colors.iterrows()):
                if i < 5:
                    with cols[i]:
                        st.markdown(f"""
                        <div class="color-swatch" style="background: {row['hex']};"></div>
                        """, unsafe_allow_html=True)
            
            st.markdown("""
                    </div>
                    <div class="section-label" style="margin-top: 1.5rem;">How It Works</div>
                    <p style="color: #666; font-size: 0.9rem; line-height: 1.6; margin-top: 0.5rem;">
                        1. Upload your outfit photo<br>
                        2. We detect the dominant colors<br>
                        3. Get perfect hijab matches<br>
                        4. Shop directly from our store
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
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
