"""Flask to create website application
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    x = 11
    return f"Hello Tariq {x}!"