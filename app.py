from flask import Flask

app = Flask(__name__, static_folder="../dist", static_url_path="/")
