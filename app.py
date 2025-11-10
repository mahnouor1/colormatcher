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

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Theme Color: #c59bd1 */
    .main-header {
        background: linear-gradient(135deg, #c59bd1 0%, #a67bc4 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(197, 155, 209, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #c59bd1;
        text-align: center;
        margin: 2rem 0;
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(197, 155, 209, 0.15);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(197, 155, 209, 0.25);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #c59bd1 0%, #a67bc4 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(197, 155, 209, 0.3);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(197, 155, 209, 0.4);
        background: linear-gradient(135deg, #a67bc4 0%, #c59bd1 100%);
    }
    
    .color-swatch {
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .color-swatch:hover {
        transform: scale(1.05);
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #c59bd1;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #c59bd1 0%, #a67bc4 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 6px rgba(197, 155, 209, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(197, 155, 209, 0.4);
        background: linear-gradient(135deg, #a67bc4 0%, #c59bd1 100%);
    }
    
    .section-title {
        color: #c59bd1;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>🧕 PurpleStore</h1>
    <p>Hijab Color Matcher</p>
    <p style="font-size: 0.95rem; margin-top: 0.5rem;">Find the perfect hijab color to match your outfit</p>
</div>
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
    # Convert RGB to more perceptually uniform space
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    
    # Weighted Euclidean distance (red is less important for clothing)
    r_mean = (r1 + r2) / 2
    delta_r = r1 - r2
    delta_g = g1 - g2
    delta_b = b1 - b2
    
    # Weighted distance formula (more emphasis on green and blue)
    distance = (2 + r_mean/256) * delta_r**2 + 4 * delta_g**2 + (2 + (255-r_mean)/256) * delta_b**2
    return distance**0.5

def get_color_palette(colors, title):
    """Display a color palette"""
    st.markdown(f"**{title}**")
    cols = st.columns(len(colors))
    for i, (name, hex_color) in enumerate(colors):
        with cols[i]:
            text_color = "white" if hex_color in ["#000000", "#800020", "#1e3a8a", "#800000"] else "black"
            st.markdown(f"<div style='width:100%;height:60px;background:{hex_color};border:1px solid #ccc;border-radius:5px;display:flex;align-items:center;justify-content:center;color:{text_color};font-weight:bold;'>{name}</div>", unsafe_allow_html=True)
            st.caption(hex_color)

# Upload section with professional styling
st.markdown("""
<div class="upload-section">
    <h3 style="color: #c59bd1; margin-bottom: 1rem;">📸 Upload Your Outfit Photo</h3>
    <p style="color: #666; margin-bottom: 1rem;">Upload a clear photo of your outfit to get personalized hijab color recommendations</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=['png', 'jpg', 'jpeg'],
    help="Upload a clear photo of your outfit. For best results, crop to show mainly the fabric.",
    key="file_uploader"
)

# Display uploaded image immediately if available
if uploaded_file is not None:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3 style="color: #c59bd1; margin-bottom: 1rem;">📷 Your Uploaded Image</h3>
    </div>
    """, unsafe_allow_html=True)
    # Responsive image display with card styling
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 1rem;">
        """, unsafe_allow_html=True)
        st.image(uploaded_file, caption="Uploaded outfit photo", width=400, use_container_width=False)
        st.markdown("</div>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    if uploaded_file is not None:
        st.markdown("""
        <div class="card">
            <h3 style="color: #c59bd1; margin-bottom: 1rem;">🔍 Color Analysis</h3>
            <p style="color: #666;">Your image is being analyzed above! We're detecting the dominant colors from your outfit to find the perfect hijab matches.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
            <h3 style="color: #c59bd1; margin-bottom: 1rem;">🎯 How It Works</h3>
            <ol style="color: #666; line-height: 2;">
                <li><strong>Upload</strong> a photo of your outfit</li>
                <li><strong>Analyze</strong> - we'll detect the dominant colors</li>
                <li><strong>Match</strong> - find perfect hijab colors</li>
                <li><strong>Shop</strong> - click to view products</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 class="section-title">🎨 Available Hijab Colors</h3>
        <p style="color: #666; font-size: 0.95rem;">Browse through our complete collection of beautiful hijab colors</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a carousel for all colors
    if 'color_page' not in st.session_state:
        st.session_state.color_page = 0
    
    colors_per_page = 6
    total_pages = (len(catalog) + colors_per_page - 1) // colors_per_page
    
    # Get colors for current page
    start_idx = st.session_state.color_page * colors_per_page
    end_idx = min(start_idx + colors_per_page, len(catalog))
    page_colors = [(row['name'], row['hex'], row['stock']) for _, row in catalog.iloc[start_idx:end_idx].iterrows()]
    
    # Display colors in a responsive grid
    if len(page_colors) <= 3:
        cols = st.columns(len(page_colors))
    else:
        cols = st.columns(3)
    
    for i, (name, hex_color, stock) in enumerate(page_colors):
        with cols[i % 3]:
            text_color = "white" if hex_color in ["#000000", "#800020", "#1e3a8a", "#800000", "#301934", "#006a4e", "#654321"] else "black"
            stock_status = "✅" if stock > 0 else "❌"
            st.markdown(f"""
            <div class="card" style='text-align:center; padding: 1rem;'>
                <div class="color-swatch" style='width:100%;height:50px;background:{hex_color};border-radius:8px;margin:0.5rem 0;border:2px solid #e9ecef;'></div>
                <h6 style='margin:0.5rem 0;color:#333;font-size:0.95rem;font-weight:600;'>{name}</h6>
                <p style='margin:0.25rem 0;font-size:0.8rem;color:#666;'><code>{hex_color}</code></p>
                <p style='margin:0.25rem 0;font-size:0.85rem;color:#666;'>{stock_status} <strong>{stock}</strong> available</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Professional navigation controls
    st.markdown("---")
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_left:
        if st.button("⬅️ Previous", disabled=(st.session_state.color_page == 0), key="prev_page", use_container_width=True):
            st.session_state.color_page -= 1
            st.rerun()
    
    with col_center:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <p style="color: #c59bd1; font-size: 1.1rem; font-weight: 600; margin: 0;">Page {st.session_state.color_page + 1} of {total_pages}</p>
        </div>
        """, unsafe_allow_html=True)
        # Quick page selector
        selected_page = st.selectbox(
            "Jump to page:", 
            range(total_pages), 
            index=st.session_state.color_page,
            key="page_selector",
            label_visibility="visible"
        )
        if selected_page != st.session_state.color_page:
            st.session_state.color_page = selected_page
            st.rerun()
    
    with col_right:
        if st.button("Next ➡️", disabled=(st.session_state.color_page >= total_pages - 1), key="next_page", use_container_width=True):
            st.session_state.color_page += 1
            st.rerun()
    
    # Show total colors count
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1rem; padding: 0.75rem; background: #f8f9fa; border-radius: 8px;">
        <p style="color: #666; margin: 0; font-size: 0.9rem;"><strong>{len(catalog)}</strong> beautiful colors available in our collection</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Extract dominant color with better quality
        color_thief = ColorThief(tmp_file_path)
        dominant_color = color_thief.get_color(quality=10)  # Higher quality for better accuracy
        dominant_hex = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
        
        # Also get a palette of colors for better matching
        palette = color_thief.get_palette(color_count=5, quality=10)
        
        # Find best matches using improved algorithm
        catalog['rgb'] = catalog['hex'].apply(hex_to_rgb)
        
        # Calculate distances for all colors in palette
        distances = []
        for color in palette:
            catalog['temp_distance'] = catalog['rgb'].apply(lambda r: color_distance(r, color))
            distances.append(catalog['temp_distance'])
        
        # Use the minimum distance from any color in the palette
        catalog['distance'] = pd.concat(distances, axis=1).min(axis=1)
        
        # Filter out out-of-stock items and sort by distance
        in_stock = catalog[catalog['stock'] > 0].copy()
        if len(in_stock) > 0:
            best_matches = in_stock.sort_values('distance').head(3)
        else:
            # If nothing in stock, show all items
            best_matches = catalog.sort_values('distance').head(3)
        
        # Display results with professional styling
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h2 class="section-title">🎯 Color Analysis Results</h2>
            <p style="color: #666; font-size: 1rem; margin-bottom: 1.5rem;">Based on your outfit, here are our top recommendations:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional recommendation cards with interactive buttons
        for i, (_, match) in enumerate(best_matches.iterrows()):
            medal = ["🥇", "🥈", "🥉"][i]
            stock_emoji = "✅" if match['stock'] > 0 else "❌"
            stock_status = "In Stock" if match['stock'] > 0 else "Out of Stock"
            
            st.markdown(f"""
            <div class="recommendation-card">
                <div style="display: flex; align-items: center; gap: 1.5rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{medal}</div>
                        <div class="color-swatch" style="width:80px;height:80px;background:{match['hex']};border:3px solid #c59bd1;border-radius:12px;box-shadow: 0 4px 8px rgba(0,0,0,0.15);"></div>
                    </div>
                    <div style="flex: 1;">
                        <h3 style="color: #c59bd1; margin: 0 0 0.5rem 0; font-size: 1.3rem;">{match['name']}</h3>
                        <p style="color: #666; margin: 0.25rem 0; font-size: 0.95rem;"><strong>Color:</strong> <code style="background: #f0f0f0; padding: 0.2rem 0.5rem; border-radius: 4px;">{match['hex']}</code></p>
                        <p style="color: #666; margin: 0.25rem 0; font-size: 0.95rem;"><strong>Stock:</strong> {stock_emoji} {stock_status} ({match['stock']} available)</p>
                    </div>
                    <div style="text-align: center;">
            """, unsafe_allow_html=True)
            
            # Interactive button
            if st.button(f"🛒 Shop Now", key=f"shop_btn_{i}", use_container_width=True):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={match["url"]}">', unsafe_allow_html=True)
                st.success(f"Opening {match['name']}...")
            
            st.markdown("""
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Show detected color palette with professional styling
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 class="section-title">🎨 Detected Colors from Your Outfit</h3>
            <p style="color: #666; font-size: 0.95rem; margin-bottom: 1rem;">These are the dominant colors we found in your outfit:</p>
        </div>
        """, unsafe_allow_html=True)
        palette_cols = st.columns(5)
        for i, color in enumerate(palette):
            with palette_cols[i]:
                hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                st.markdown(f"""
                <div class="card" style="text-align: center; padding: 1rem;">
                    <div class="color-swatch" style='width:100%;height:60px;background:{hex_color};border:2px solid #c59bd1;border-radius:8px;margin-bottom:0.5rem;'></div>
                    <p style="font-size:0.8rem;color:#666;margin:0;"><code>{hex_color}</code></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please make sure you've uploaded a valid image file (PNG, JPG, or JPEG).")

else:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-left: 4px solid #c59bd1;">
        <p style="color: #666; margin: 0; font-size: 1rem;">👆 <strong>Upload a clear photo of your outfit</strong> to get personalized hijab color recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional tips section
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 class="section-title">💡 Tips for Best Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="color: #c59bd1; margin-bottom: 0.75rem;">📸 Photo Tips</h4>
            <ul style="color: #666; line-height: 2; margin: 0;">
                <li>Good lighting (natural light)</li>
                <li>Focus on fabric</li>
                <li>Clear, solid colors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="color: #c59bd1; margin-bottom: 0.75rem;">🎯 Best Results</h4>
            <ul style="color: #666; line-height: 2; margin: 0;">
                <li>High resolution images</li>
                <li>Single dominant color</li>
                <li>Avoid busy patterns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Professional Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#666;font-size:0.9rem;padding:1.5rem;background:linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);border-radius:12px;margin-top:2rem;'>
    <p style='margin:0.5rem 0;color:#c59bd1;font-weight:600;'>Made with ❤️ for PurpleStore</p>
    <p style='margin:0.25rem 0;color:#999;font-size:0.85rem;'>Powered by Streamlit & ColorThief</p>
    <p style='margin:0.5rem 0 0 0;color:#999;font-size:0.8rem;'>© 2025 PurpleStore. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)