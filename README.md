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

## Deployment on Vercel (from GitHub)

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/mealsfly-website.git
   git push -u origin main
   ```

### Step 2: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Click "Deploy"

### Step 3: Configure Environment Variables
In your Vercel project dashboard, go to Settings > Environment Variables and add:
- `SESSION_SECRET`: A secure random string (generate one at https://djecrety.ir/)

### Automatic Deployments
Once connected, Vercel will automatically deploy:
- Every push to the `main` branch
- Pull requests (as preview deployments)

## Environment Variables for Production

When deploying to Vercel, set these environment variables in your Vercel dashboard:

- `SESSION_SECRET`: A secure random string for session encryption

## File Structure

```
├── app.py                 # Main Flask application
├── main.py               # Entry point for Vercel
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── runtime.txt          # Python version specification
├── static/              # CSS, JS, and image files
├── templates/           # HTML templates
├── .env.example         # Environment variables example
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Forms**: Flask-WTF, WTForms
- **Integration**: Google Sheets API
- **Deployment**: Vercel + GitHub
- **CI/CD**: Automatic deployments on push

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## Security Notes

- Google Sheets credentials are currently hardcoded in `app.py`
- For production, consider moving sensitive credentials to environment variables
- The `.env.example` file shows how to structure environment variables
