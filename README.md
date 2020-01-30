# pcapVis
PCAP Force-Directed Graph Generators
- Requires Python 2.6+, GraphViz, and TShark
- Install Requirements: ```sudo apt-get install graphviz tshark -y```
- Usage:  ```script.py yourfile.pcap```

## Updates
- 29 Jan 2020
	- added quick-and dirty tls flag, to convert the ssl.* fields to tls.*
 
## TO DO
- use argparse and subprocess
- major code refactoring
- check if successful before displaying "made xyz" message
- better output filename

## pcapVis-connections.py
Produces a basic force-directed link graph that also highlights SSH connections
![pcapVis-connections.py](https://github.com/bonifield/pcapVis/blob/master/conn-snippet.PNG)

## pcapVis-httpRequestChain.py
Produces a URLQuery.net-like HTTP/SSL force-directed link graph of web connections
- note that this version only supports http referrers, and not .location redirects, etc (work in progress)
![pcapVis-httpRequestChain.py](https://github.com/bonifield/pcapVis/blob/master/chain-snippet.PNG)

