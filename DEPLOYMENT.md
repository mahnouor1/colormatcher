# 🚀 Deployment Guide for PurpleStore Hijab Color Matcher

## Step 1: Push to GitHub

### Option A: Using GitHub CLI (Recommended)
```bash
# Install GitHub CLI if you haven't already
# brew install gh (on macOS)

# Login to GitHub
gh auth login

# Create repository and push
gh repo create purple-hijab-matcher --public --source=. --remote=origin --push
```

### Option B: Manual GitHub Setup
1. Go to [github.com](https://github.com) and create a new repository named `purple-hijab-matcher`
2. Make it **public** (required for free Streamlit Cloud)
3. Run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/purple-hijab-matcher.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the details:
   - **Repository**: `YOUR_USERNAME/purple-hijab-matcher`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

Your app will be available at: `https://purple-hijab-matcher.streamlit.app`

## Step 3: Embed in Your Website

### For Odoo Website:
1. Go to your Odoo admin panel
2. Navigate to **Website → Edit**
3. Add an **HTML block**
4. Paste this code:

```html
<iframe
  src="https://purple-hijab-matcher.streamlit.app/?embed=true"
  style="width:100%; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
  loading="lazy"
  title="PurpleStore Hijab Color Matcher"
></iframe>
```

### For Any Website:
Add this to your HTML:

```html
<div style="text-align: center; margin: 20px 0;">
  <h2>Find Your Perfect Hijab Color</h2>
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="width:100%; max-width:800px; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
    loading="lazy"
    title="PurpleStore Hijab Color Matcher"
  ></iframe>
</div>
```

## Step 4: Customize the Embed

### Responsive Design:
```html
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
    loading="lazy"
    title="PurpleStore Hijab Color Matcher"
  ></iframe>
</div>
```

### With Custom Styling:
```html
<div class="hijab-matcher-container" style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
  <h3 style="text-align: center; color: #8B5CF6; margin-bottom: 20px;">🧕 Find Your Perfect Hijab Match</h3>
  <iframe
    src="https://purple-hijab-matcher.streamlit.app/?embed=true"
    style="width:100%; height:650px; border:none; border-radius:10px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);"
    loading="lazy"
    title="PurpleStore Hijab Color Matcher"
  ></iframe>
</div>
```

## Troubleshooting

### If the embed doesn't work:
1. Make sure your Streamlit app is deployed and accessible
2. Check that the URL is correct
3. Try adding `?embed=true` to the URL
4. Ensure your website allows iframe embedding

### For HTTPS issues:
- Streamlit Cloud provides HTTPS by default
- Make sure your website also uses HTTPS for security

## Next Steps

1. **Test the embed** on your website
2. **Customize the styling** to match your brand
3. **Add analytics** to track usage
4. **Update the catalog** regularly by pushing changes to GitHub

---

**Your deployed app will automatically update when you push changes to the main branch!**
