# 🧕 PurpleStore Hijab Color Matcher

A beautiful Streamlit app that helps you find the perfect hijab color to match your outfit! Upload a photo of your outfit and get instant color recommendations from PurpleStore's hijab collection.

## ✨ Features

- **Smart Color Detection**: Uses ColorThief to extract the dominant color from your outfit photos
- **Color Matching Algorithm**: Finds the best matching hijab colors from our curated catalog
- **Beautiful UI**: Clean, modern interface with color swatches and match scores
- **Direct Product Links**: Click through to view and purchase recommended hijabs
- **Multiple Recommendations**: Get top 3 color matches with confidence scores

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd purple-hijab-matcher
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
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and set `app.py` as the main file
6. Deploy! You'll get a URL like: `https://purple-hijab-matcher.streamlit.app`

#### Option 2: Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create purple-hijab-matcher`
4. Deploy: `git push heroku main`

#### Option 3: Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📁 Project Structure

```
purple-hijab-matcher/
├── app.py                 # Main Streamlit application
├── hijab_catalog.csv      # Hijab color database
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
└── README.md             # This file
```

## 🎨 How It Works

1. **Upload**: User uploads a photo of their outfit
2. **Analyze**: ColorThief extracts the dominant color from the image
3. **Match**: Algorithm compares the detected color with hijab catalog colors
4. **Recommend**: Shows best matches with visual color swatches and product links

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Color Analysis**: ColorThief library
- **Data**: CSV-based hijab catalog
- **Algorithm**: Euclidean distance for color matching
- **UI**: Responsive design with HTML/CSS styling

## 📝 Tips for Best Results

- Use photos with good lighting
- Crop images to focus on the main fabric
- Solid colors work better than complex patterns
- Higher resolution images give better color detection

## 🔧 Customization

### Adding New Hijab Colors
Edit `hijab_catalog.csv` to add new colors:
```csv
name,hex,url
New Color,#ff5733,https://purplestore.com.pk/product/new-color-hijab
```

### Modifying the Algorithm
The color matching algorithm is in the `color_distance()` function. You can adjust it to use different color spaces or weighting.

## 📄 License

This project is created for PurpleStore. All rights reserved.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

Made with ❤️ for PurpleStore | Powered by Streamlit & ColorThief
