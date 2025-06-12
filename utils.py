from flask import request


def get_ip():
    return request.headers.get("cf-connecting-ip") or request.headers.get(
        "x-real-ip") or request.remote_addr or "Unknown"
