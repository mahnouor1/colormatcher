# 🧕 PurpleStore Hijab Color Matcher

A beautiful Streamlit app that helps you find the perfect hijab color to match your outfit! Upload a photo of your outfit and get instant color recommendations from PurpleStore's hijab collection.

## ✨ Features

- **Smart Color Detection**: Uses ColorThief to extract the dominant color from your outfit photos
- **Color Matching Algorithm**: Finds the best matching hijab colors from our curated catalog
- **Beautiful UI**: Clean, modern interface with color swatches and match scores
- **Direct Product Links**: Click through to view and purchase recommended hijabs
- **Multiple Recommendations**: Get top 3 color matches with confidence scores
- **Swipeable Collection**: Browse all 43 hijab colors with navigation arrows
- **Stock Information**: See real-time stock availability for each color

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahnouor1/purplehijab.git
   cd purplehijab
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### Deployment Options

#### Option 1: Streamlit Cloud (Recommended)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `mahnouor1/purplehijab`
5. Set main file: `app.py`
6. Deploy! You'll get a URL like: `https://purplehijab.streamlit.app`

#### Option 2: Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create purplehijab`
4. Deploy: `git push heroku main`

#### Option 3: Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📁 Project Structure

```
purplehijab/
├── app.py                 # Main Streamlit application
├── hijab_catalog.csv      # Hijab color database (43 colors)
├── requirements.txt       # Python dependencies
├── .streamlit/config.toml # Streamlit configuration
├── Procfile              # Heroku deployment config
├── DEPLOYMENT.md         # Deployment guide
├── embed-example.html    # Website integration example
└── README.md             # This file
```

## 🎨 How It Works

1. **Upload**: User uploads a photo of their outfit
2. **Analyze**: ColorThief extracts 5 dominant colors from the image
3. **Match**: Improved algorithm compares colors with hijab catalog
4. **Recommend**: Shows best matches with stock info and product links
5. **Browse**: Users can swipe through all 43 available colors

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Color Analysis**: ColorThief library with improved quality settings
- **Data**: CSV-based hijab catalog with stock information
- **Algorithm**: Weighted Euclidean distance for better color matching
- **UI**: Responsive design with HTML/CSS styling and carousel navigation

## 📝 Tips for Best Results

- Use photos with good lighting
- Crop images to focus on the main fabric
- Solid colors work better than complex patterns
- Higher resolution images give better color detection

## 🔧 Customization

### Adding New Hijab Colors
Edit `hijab_catalog.csv` to add new colors:
```csv
name,hex,stock,url
New Color,#ff5733,50,https://www.purplestore.com.pk/product/new-color-hijab
```

### Modifying the Algorithm
The color matching algorithm is in the `color_distance()` function. You can adjust it to use different color spaces or weighting.

## 🌐 Website Integration

### Embed Code for Your Website
```html
<iframe
  src="https://purplehijab.streamlit.app/?embed=true"
  style="width:100%; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
  loading="lazy"
  title="PurpleStore Hijab Color Matcher"
></iframe>
```

## 📄 License

This project is created for PurpleStore. All rights reserved.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

Made with ❤️ for PurpleStore | Powered by Streamlit & ColorThief
