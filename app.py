import streamlit as st
from colorthief import ColorThief
import pandas as pd
import tempfile
import os

# Configure the page
st.set_page_config(
    page_title="PurpleStore — Hijab Color Matcher",
    page_icon="🧕",
    layout="wide"
)

# Title and description
st.title("🧕 PurpleStore — Hijab Color Matcher")
st.markdown("Upload an outfit photo and we'll suggest the best hijab color from our catalog.")
st.markdown("---")

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
    """Calculate Euclidean distance between two RGB colors"""
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def get_color_palette(colors, title):
    """Display a color palette"""
    st.markdown(f"**{title}**")
    cols = st.columns(len(colors))
    for i, (name, hex_color) in enumerate(colors):
        with cols[i]:
            text_color = "white" if hex_color in ["#000000", "#800020", "#1e3a8a", "#800000"] else "black"
            st.markdown(f"<div style='width:100%;height:60px;background:{hex_color};border:1px solid #ccc;border-radius:5px;display:flex;align-items:center;justify-content:center;color:{text_color};font-weight:bold;'>{name}</div>", unsafe_allow_html=True)
            st.caption(hex_color)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Upload Your Outfit Photo")
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo of your outfit. For best results, crop to show mainly the fabric."
    )

with col2:
    st.markdown("### 🎨 Available Hijab Colors")
    # Show top 5 colors from catalog
    top_colors = [(row['name'], row['hex']) for _, row in catalog.head(5).iterrows()]
    get_color_palette(top_colors, "Our Collection")

if uploaded_file is not None:
    # Display the uploaded image
    st.markdown("---")
    st.markdown("### 📷 Your Uploaded Image")
    st.image(uploaded_file, caption="Uploaded outfit photo", use_column_width=True)
    
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Extract dominant color
        color_thief = ColorThief(tmp_file_path)
        dominant_color = color_thief.get_color(quality=1)  # (R, G, B)
        dominant_hex = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
        
        # Display detected color
        st.markdown("### 🔍 Color Analysis")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("**Detected Dominant Color:**")
            st.markdown(f"`{dominant_hex}`")
            st.markdown(f"<div style='width:120px;height:80px;background:{dominant_hex};border:2px solid #333;border-radius:10px;'></div>", unsafe_allow_html=True)
        
        # Find best matches
        catalog['rgb'] = catalog['hex'].apply(hex_to_rgb)
        catalog['distance'] = catalog['rgb'].apply(lambda r: color_distance(r, dominant_color))
        best_matches = catalog.sort_values('distance').head(3)
        
        with col2:
            st.markdown("**🥇 Best Match**")
            best_match = best_matches.iloc[0]
            st.markdown(f"**[{best_match['name']}]({best_match['url']})**")
            st.markdown(f"`{best_match['hex']}`")
            st.markdown(f"<div style='width:120px;height:80px;background:{best_match['hex']};border:2px solid #333;border-radius:10px;'></div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("**🥈 Second Choice**")
            second_match = best_matches.iloc[1]
            st.markdown(f"**[{second_match['name']}]({second_match['url']})**")
            st.markdown(f"`{second_match['hex']}`")
            st.markdown(f"<div style='width:120px;height:80px;background:{second_match['hex']};border:2px solid #333;border-radius:10px;'></div>", unsafe_allow_html=True)
        
        # Show all matches with scores
        st.markdown("### 📊 All Color Matches")
        st.markdown("Here are all available hijab colors ranked by how well they match your outfit:")
        
        # Create a dataframe for display
        display_df = best_matches[['name', 'hex', 'url']].copy()
        display_df['Match Score'] = (1 - (best_matches['distance'] / max(best_matches['distance']))) * 100
        display_df['Match Score'] = display_df['Match Score'].round(1)
        
        # Display as cards
        cols = st.columns(3)
        for i, (_, row) in enumerate(display_df.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='border:1px solid #ddd;border-radius:10px;padding:15px;margin:10px 0;background:#f9f9f9;'>
                    <h4 style='margin:0;color:#333;'>{row['name']}</h4>
                    <div style='width:100%;height:50px;background:{row['hex']};border-radius:5px;margin:10px 0;'></div>
                    <p style='margin:5px 0;font-size:12px;color:#666;'>{row['hex']}</p>
                    <p style='margin:5px 0;font-size:12px;color:#666;'>Match: {row['Match Score']}%</p>
                    <a href='{row['url']}' target='_blank' style='color:#8B5CF6;text-decoration:none;font-size:12px;'>View Product →</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please make sure you've uploaded a valid image file (PNG, JPG, or JPEG).")

else:
    st.info("👆 Upload a clear photo of your outfit to get hijab color recommendations!")
    
    # Show some tips
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - **Good lighting**: Take photos in natural light when possible
        - **Focus on fabric**: Crop the image to show mainly the clothing fabric
        - **Clear colors**: Avoid photos with multiple dominant colors
        - **High resolution**: Higher quality images give better color detection
        - **Solid colors work best**: Patterns with many colors may not give optimal results
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#666;font-size:12px;'>
    Made with ❤️ for PurpleStore | Powered by Streamlit & ColorThief
</div>
""", unsafe_allow_html=True)