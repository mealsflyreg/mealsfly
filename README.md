# MealsFly Website

A Flask-based landing page for MealsFly food delivery app with partner and rider registration forms.

## Features

- Responsive landing page
- Partner restaurant registration
- Rider registration
- Google Sheets integration for form submissions
- Bootstrap UI components

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Open your browser and go to `http://localhost:5000`

## Deployment Options

### Option 1: Deploy to Render (Recommended)

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy to Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub account and select this repository
   - Use these settings:
     - **Name**: `mealsfly-website`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
   - Click "Create Web Service"

3. **Set Environment Variables** (optional):
   - In Render dashboard, go to Environment tab
   - Add `SESSION_SECRET` with a secure random string

### Option 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the Python project
5. Set environment variable: `SESSION_SECRET`
6. Click "Deploy"

### Option 3: Deploy to Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create mealsfly-website`
4. Set environment variable: `heroku config:set SESSION_SECRET=your-secret-key`
5. Deploy: `git push heroku main`

## Environment Variables

Set these environment variables in your deployment platform:

- `SESSION_SECRET`: A secure random string for Flask sessions (required)
- `PORT`: Port number (automatically set by most platforms)

## File Structure

```
├── app.py              # Main Flask application
├── main.py             # Entry point for deployment
├── start.py            # Alternative start script
├── requirements.txt    # Python dependencies
├── Procfile           # Process configuration
├── render.yaml        # Render configuration
├── vercel.json        # Vercel configuration
├── runtime.txt        # Python version specification
├── static/            # CSS, JS, and image files
├── templates/         # HTML templates
├── .env.example       # Environment variables example
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Forms**: Flask-WTF, WTForms
- **Integration**: Google Sheets API
- **Deployment**: Render, Vercel, or Heroku compatible

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## Live Demo

Once deployed, your website will have:
- Landing page at `/`
- Partner registration at `/become-partner`
- Rider registration at `/become-rider`
- Download tracking at `/download`
