from app import app

# This is required for Vercel
def handler(request):
    return app(request.environ, request.start_response)

# This is required for gunicorn to find the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
