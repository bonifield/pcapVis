#!/usr/bin/python

#=============
# HTTP-link viewer, inspired by URLQuery.net
# Requires Python 2.6+, GraphViz, and TShark
# v1.2
# 19 May 2017
#=============

import sys, os

inputFile = sys.argv[1]
dotFile = str(inputFile+'-chain.dot')
dotOutputFile = str(inputFile+'-chain-dot.png')
circoOutputFile = str(inputFile+'-chain-circo.png')
neatoOutputFile = str(inputFile+'-chain-circo.png')

# be cheaty and use tshark to do the heavy lifting
command = 'tshark -r %s -T fields -e ip.src -e ip.dst -e http.host -e http.request.method -e http.referer -e ssl.handshake.extensions_server_name -Y "http.request or ssl.handshake.extensions_server_name" -E separator=, | sort | uniq' % (inputFile)
listy = []
dicty = {}

def makeGraph():
	for line in os.popen(command):
		l = line.strip('\n').replace('http://', '').replace('https://','').split(',')
		sip = str(l[0])
		dip = str(l[1])
		hosty = str(l[2])
		method = str(l[3])
		refy = str(l[4])
		sslsrvr = str(l[5])
		k = ''
		v = ''
		if len(hosty) >= 3 and len(refy) >= 3: # if there is a referrer
			r = refy.split('/')[0] # split it before the uri
			if hosty != r: # if the referrer and host are not the same
				listy.append('"%s" -> "%s" [label="%s", color="blue"]' % (r, hosty, method)) # add the referrer-to-host link
				k = hosty
				v = str('IP:  '+dip)
		elif len(hosty) >= 3 and len(refy) == 0:
			listy.append('"%s" -> "%s" [label="%s", color="blue"]' % (sip, hosty, method)) # add the sip-to-host link
			k = hosty
			v = str('IP:  '+dip)
		if len(sslsrvr) >= 3:
			listy.append('"%s" -> "%s" [label="SSL", color="cyan"]' % (sip, sslsrvr)) # add the sip-to-sslsrvr link
			k = sslsrvr
			v = str('IP:  '+dip)

		if len(k) >= 2:
			try:
				if k not in dicty.keys():
					dicty.setdefault(k,[])
					dicty[k].append(v)
				elif k in dicty.keys():
					dicty[k].append(v)
			except:
				pass

	for key,val in dicty.items():
		v = list(set(dicty[key]))
		dicty[key]=v

	with open(dotFile,'w') as d:
		# create the graph formatting, note that rankdir is now "LR" (previously "TB")
		dotty = str('digraph graph_name { \n\ngraph [\nlabel="%s",\nlabelloc="t",\nlabeljust="c",\nbgcolor="white",\nfontcolor="black",\nfontsize=16,\nmargin=0,\nrankdir=LR,\nsplines=spline,\nranksep=1,\nnodesep=1\n]; \n\nnode [\nstyle="solid,filled",\nfontsize=14,\nfontcolor=black,\nfontname="Arial",\nfillcolor=none,\nfixedsize=false\n]; \n\nedge [\nstyle=solid,\nfontsize=12,\nfontcolor=black,\nfontname="Arial",\ncolor=black\n]\n' % (sys.argv[1]))
		d.write(dotty)
		for i in list(set(listy)): # implement the unique lines from the list previously created
			d.write('\n'+i+';')
		d.write('\n\n')
		if dicty:
			for key in dicty.keys():
				d.write(str('"%s" [label = "' % (key)))
				d.write(key)
				for val in dicty[key]:
					d.write(r'\n'+val)
				d.write('"];\n')
			d.write('\n\n}')
	d.close()

	os.popen('dot -Tpng %s -o %s' % (dotFile, dotOutputFile))
#	os.popen('circo -Tpng %s -o %s' % (dotFile, circoOutputFile))
#	os.popen('neato -Goverlap=scale -Tpng %s -o %s' % (dotFile, neatoOutputFile))
	os.remove(dotFile)	

#====================

if __name__ == "__main__":
	makeGraph()
