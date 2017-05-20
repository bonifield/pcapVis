# pcapVis
PCAP Force-Directed Graph Generators
- Requires Python 2.6+, GraphViz, and TShark
- Install Requirements: <b>sudo apt-get install graphviz tshark -y</b>
- Usage:  <b><i>script.py yourfile.pcap</i></b>
- Useful aliases for directories with multiple PCAPs:
  * alias pchain='for i in \`ls | grep pcap | grep -v zip\`; do pcapVis-httpRequestChain.py $i; done'
  * alias pconns='for i in \`ls | grep pcap | grep -v zip\`; do pcapVis-connections.py $i; done'

<b>pcapVis-connections.py</b>
Produces a basic force-directed link graph that also highlights SSH connections
![pcapVis-connections.py](https://github.com/bonifield/pcapVis/blob/master/conn-snippet.PNG)

<b>pcapVis-httpRequestChain.py</b>
Produces a URLQuery.net-like HTTP/SSL force-directed link graph of web connections
- note that this version only supports http referrers, and not .location redirects, etc (work in progress)
![pcapVis-httpRequestChain.py](https://github.com/bonifield/pcapVis/blob/master/chain-snippet.PNG)

