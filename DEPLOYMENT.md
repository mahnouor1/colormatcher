# 🚀 Deployment Guide - PurpleStore Hijab Color Matcher

## Option 1: Streamlit Cloud (Recommended)

### Step 1: Push to GitHub
```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/purple-hijab-matcher.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/purple-hijab-matcher`
5. Set main file path: `app.py`
6. Click "Deploy"

Your app will be available at: `https://purple-hijab-matcher.streamlit.app`

## Option 2: Other Hosting Platforms

### Heroku
```bash
# Install Heroku CLI, then:
heroku create purple-hijab-matcher
git push heroku main
```

### Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## Website Integration

### For Odoo Website
Add this HTML block to your Odoo website:

```html
<iframe
  src="https://purple-hijab-matcher.streamlit.app/?embed=true"
  style="width:100%; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
  loading="lazy"
  title="PurpleStore Hijab Color Matcher"
></iframe>
```

### For WordPress
Use the HTML block and paste the same iframe code.

### For Custom Websites
Add this to your HTML:

```html
<div style="max-width: 100%; margin: 20px auto;">
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="width:100%; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
    loading="lazy"
    title="PurpleStore Hijab Color Matcher"
  ></iframe>
</div>
```

### Responsive Embed (Mobile-Friendly)
```html
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
    loading="lazy"
    title="PurpleStore Hijab Color Matcher"
  ></iframe>
</div>
```

## Customization Options

### Different Heights
- **Compact**: `height: 500px`
- **Standard**: `height: 650px` (recommended)
- **Full**: `height: 800px`

### Styling Options
```html
<!-- With custom border -->
<iframe
  src="https://purple-hijab-matcher.streamlit.app/?embed=true"
  style="width:100%; height:650px; border: 2px solid #8B5CF6; border-radius:15px;"
  loading="lazy"
></iframe>

<!-- With background -->
<div style="background: linear-gradient(135deg, #8B5CF6, #A855F7); padding: 20px; border-radius: 15px;">
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="width:100%; height:650px; border:none; border-radius:10px;"
    loading="lazy"
  ></iframe>
</div>
```

## Testing Your Integration

1. **Test the deployed app**: Visit your Streamlit Cloud URL
2. **Test the embed**: Add the iframe to your website
3. **Test on mobile**: Ensure it's responsive
4. **Test functionality**: Upload an image and verify color matching works

## Troubleshooting

### Common Issues:
- **App not loading**: Check if the Streamlit Cloud URL is correct
- **Embed not working**: Ensure your website allows iframes
- **Mobile issues**: Use the responsive embed code
- **Slow loading**: Add `loading="lazy"` attribute

### Support:
- Streamlit Cloud: [docs.streamlit.io](https://docs.streamlit.io)
- GitHub Issues: Create an issue in your repository