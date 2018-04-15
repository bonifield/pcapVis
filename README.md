# pcapVis
PCAP Force-Directed Graph Generators
- Requires Python 2.6+, GraphViz, and TShark
- Install Requirements: ```sudo apt-get install graphviz tshark -y```
- Usage:  ```script.py yourfile.pcap```

## pcapVis-connections.py
Produces a basic force-directed link graph that also highlights SSH connections
![pcapVis-connections.py](https://github.com/bonifield/pcapVis/blob/master/conn-snippet.PNG)

## pcapVis-httpRequestChain.py
Produces a URLQuery.net-like HTTP/SSL force-directed link graph of web connections
- note that this version only supports http referrers, and not .location redirects, etc (work in progress)
![pcapVis-httpRequestChain.py](https://github.com/bonifield/pcapVis/blob/master/chain-snippet.PNG)

