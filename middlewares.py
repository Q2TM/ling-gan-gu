from datetime import datetime

from flask import request, Response

from app import app
from utils import get_ip


@app.after_request
def log_response(response: Response):
    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {get_ip()} -> {request.method} {request.path} {response.status_code}")
    return response
