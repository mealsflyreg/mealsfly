import os
from app import app

# This is required for Vercel
def handler(request):
    return app(request.environ, request.start_response)

# This is required for gunicorn to find the app (used by Render)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
