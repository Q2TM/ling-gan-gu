import os

from waitress import serve

from app import app
import routes
import middlewares

PORT = 3133

if os.getenv("DEV"):
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    print(f"Starting server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
