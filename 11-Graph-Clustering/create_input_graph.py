import networkx as nx 
import pylab as plt

G=nx.Graph()
fh=open("input.edgelist", 'rb')
G=nx.read_edgelist(fh)
fh.close()
nx.draw(G,with_labels=True)
plt.show()