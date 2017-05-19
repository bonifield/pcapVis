#!/usr/bin/python

#====================
# PCAP Force-Directed Graph Maker v1.4
# 19 May 2017
# Requires Python 2.6+, TShark, and GraphViz
# v1.3 - fixed dictionary/node label logic
# v1.4 - all keys now have unique value lists
# TODO - add user input options
# TODO - color legend
#====================

import sys, os

#====================

inputFile = sys.argv[1]
dotFile = str(inputFile+'-conns.dot')
dotOutputFile = str(inputFile+'-conns-dot.png')
circoOutputFile = str(inputFile+'-conns-circo.png')
neatoOutputFile = str(inputFile+'-conns-neato.png')
listy = [] # connection line list
dicty = {} # node label dictionary
command = 'tshark -r %s -T fields -e ip.proto -e ip.src -e ip.dst -e http.host -e http.request.method -e http.response.code -e http.response.phrase -e ssl.handshake.extensions_server_name -e ssh.protocol -E separator=, -Y "tcp or udp or sctp" | sort | uniq' % (inputFile)

#====================

def makeGraph():
	print('Generating graph.  This may take a few seconds...')
	for line in os.popen(command):
		l = line.split(',')
		k = ''
		v = ''
		proto = int(l[0])
		sip = str(l[1])
		dip = str(l[2])
		hosty = str(l[3])
		reqy = str(l[4])
		code = str(l[5])
		phrase = str(l[6])
		respy = str(l[5]+' '+l[6])
		sslsrvr = str(l[7])
		sshy = str(l[8].replace('\\x0d\\x0a','').replace(' ','_'))
		if proto == 6:
			if len(hosty) >= 3:
				listy.append('"%s" -> "%s" [label="%s", color="blue"]' % (sip, dip, reqy))
				k = dip # add the relevant IP as a key to the dictionary
				v = str('(HTTP) '+hosty) # create a value to be appended to the key
			elif len(respy) >= 3:
				listy.append('"%s" -> "%s" [label="%s", color="blue"]' % (sip, dip, respy))
			elif len(sslsrvr) >= 3:
				listy.append('"%s" -> "%s" [label="SSL", color="cyan"]' % (sip, dip))
				k = dip
				v = str('(SSL) '+sslsrvr)
			elif len(sshy) >= 3:
				listy.append('"%s" -> "%s" [label="SSH", color="red", penwidth=3, arrowsize=2]' % (sip, dip))
				k = sip
				v = str('(SSH) '+sshy)
		elif proto == 17:
			listy.append('"%s" -> "%s" [label="UDP", color="orange"]' % (sip, dip))
		elif proto == 132:
			listy.append('"%s" -> "%s" [label="SCTP", color="black"]' % (sip, dip))

		if len(k) >= 2: # if there is a key/value pair to be added to the label dictionary
			try:
				if k not in dicty.keys(): # if the key does not exist
					dicty.setdefault(k,[]) # initialize the key
					dicty[k].append(v) # append value to the key
				elif k in dicty.keys(): # if the key already exists
					dicty[k].append(v) # append the value
			except:
				pass

	# ensure all key values are unique item lists
	for key,val in dicty.items():
		v = list(set(dicty[key])) # create a list from a set (from a list of values)
		dicty[key]=v # reset the key's values to the unique list

	# create the dot file and enter the data to form the graph
	with open(dotFile,'w') as d:
		# create the graph formatting
		dotty = str('digraph graph_name { \n\ngraph [\nlabel="%s",\nlabelloc="t",\nlabeljust="c",\nbgcolor="white",\nfontcolor="black",\nfontsize=16,\nmargin=0,\nrankdir=LR,\nsplines=spline,\nranksep=1,\nnodesep=1\n]; \n\nnode [\nstyle="solid,filled",\nfontsize=14,\nfontcolor=black,\nfontname="Arial",\nfillcolor=none,\nfixedsize=false\n]; \n\nedge [\nstyle=solid,\nfontsize=12,\nfontcolor=black,\nfontname="Arial",\ncolor=black\n]\n' % (sys.argv[1]))
		d.write(dotty)
		for i in list(set(listy)): # implement the unique lines from the list previously created (for the scapy version)
			d.write('\n'+i+';')
		d.write('\n\n')
		if dicty:
			for key in dicty.keys(): # for each key (which is an IP to be labeled)
				d.write(str('"%s" [ label = "' % (key))) # open the label bracket for that IP
				d.write('IP:  '+key)
				for val in dicty[key]: # iterate over the values for the key (the labels to be added to the node)
					d.write(r'\n'+val) # write the label
				d.write('"];\n') # close the bracket for the key (IP)
			d.write('\n\n}') # close the dot file formatting requirements
	d.close()

	# use the dot file to create the graph
	os.popen('dot -Tpng %s -o %s' % (dotFile, dotOutputFile))
#	os.popen('circo -Tpng %s -o %s' % (dotFile, circoOutputFile))
#	os.popen('neato -Goverlap=scale -Tpng %s -o %s' % (dotFile, neatoOutputFile))
	os.remove(dotFile) # remove dot file

#====================

if __name__ == "__main__":
	makeGraph()
