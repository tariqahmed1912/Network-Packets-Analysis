"""Capture tcpdump packets over a network.
"""

import pandas as pd
import sys
import os
import json

def get_traffic():
    # tcpdump packets stores in Desktop/Extra Project/dump.txt
    tcp, udp, arp, icmp = [],[],[],[]
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    with open(f"{path}/dump.txt", 'r') as f:
        data = f.read()
    data = data.strip()
    data = data.replace("\n","@")
    data = data.split("@")
    for line in data:
        if 'UDP' in line:
            udp.append(line.split())
        elif 'ARP' in line:
            arp.append(line.split())
        elif 'ICMP' in line or 'ICMP6' in line:
            icmp.append(line.split())
        else:
            tcp.append(line.split())

    df_arp = pd.DataFrame(arp)
    df_tcp = pd.DataFrame(tcp)[[0,1,2,4]]
    df_udp = pd.DataFrame(udp)[[0,2,4,5]]
    df_icmp = pd.DataFrame(icmp)[[0,2,4,5]]

    df_tcp.columns = ['timestamp', 'protocol', 'src', 'dest']
    df_udp.columns = ['timestamp', 'src', 'dest', 'protocol']
    df_icmp.columns = ['timestamp', 'src', 'dest', 'protocol']
    
    df_arp[1] = df_arp[1].str.replace(',','')
    df_icmp['protocol'] = df_icmp['protocol'].str.replace(',', '')
    df_udp['protocol'] = df_udp['protocol'].str.replace(',', '')
    df = [df_tcp, df_udp, df_arp, df_icmp]
    for i in range(len(df)):
        df[i] = df[i].to_json(orient='records')
        df[i] = json.loads(df[i])

    # df_tcp = df_tcp.to_json(orient='records')
    # df_tcp = json.loads(df_tcp)
    df_udp = df_udp.to_json(orient='records')
    df_udp = json.loads(df_udp)
    df_arp = df_arp.to_json(orient='records')
    df_arp = json.loads(df_arp)
    df_icmp = df_icmp.to_json(orient='records')
    df_icmp = json.loads(df_icmp)

    return df_tcp, df_udp, df_arp, df_icmp
    

