"""Flask to create website application
"""

from flask import Flask, request, redirect, render_template, url_for
import pandas as pd
import plotly
import re
from capture import get_traffic, NetworkPackets

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == "POST":
        for protocol in ['tcp','udp','icmp','arp']:
            if protocol in request.form:
                break
        packets = NetworkPackets()
        if "tcp" in request.form:
            data = packets.gettcp()
        elif "udp" in request.form:
            data = packets.getudp()
        elif "icmp" in request.form:
            data = packets.geticmp()
        else:
            data = packets.getarp()
        print(data)
        graph_data = retrieveFrequencyCount(data)
        print(graph_data)
        return render_template('graph.html', graph_data=graph_data)
    else:
        tcp, udp, arp, icmp = get_traffic()
        context = {'tcp':tcp, 'udp':udp, 'arp':arp, 'icmp':icmp}
        return render_template('main.html', context=context)


def retrieveFrequencyCount(df):
    """Take dataframe as input and retrieve required frequency and count details.

    Args:
        df (DataFrame): Network packets as a dataframe
    """
    re_pattern = re.compile("(\d+\.\d+\.\d+\.\d+)[\.|\:].*")
    for col in ['src','dest']:
        df[col] = df[col].str.replace(re_pattern, r'\1')
    #df['src'] = df['src'].str.replace(re_pattern, '\1')
    src_ip_list = df.src.value_counts().index.to_list()
    src_ip_count = df.src.value_counts().to_list()
    dest_ip_list = df.dest.value_counts().index.to_list()
    dest_ip_count = df.dest.value_counts().to_list()
    
    graph_data = {
        'src_ip':src_ip_list,
        'src_count':src_ip_count,
        'dest_ip':dest_ip_list,
        'dest_count':dest_ip_count
    }
    
    return graph_data
