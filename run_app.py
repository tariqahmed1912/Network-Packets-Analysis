"""Flask to create website application
"""

from flask import Flask, render_template
from capture import get_traffic

app = Flask(__name__)

@app.route('/')
def hello():
    tcp, udp, arp, icmp = get_traffic()
    context = {'tcp':tcp, 'udp':udp, 'arp':arp, 'icmp':icmp}
    return render_template('main.html', context=context)