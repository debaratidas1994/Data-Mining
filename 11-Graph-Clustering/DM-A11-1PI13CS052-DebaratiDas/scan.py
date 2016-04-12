#import statements here
import networkx as nx
import math
import pylab as plt
#this calculates the similarity based on the formula of sigma
def similarity(G,v,u):
    v_set = set(G.neighbors(v))
    u_set = set(G.neighbors(u))
    inter = v_set.intersection(u_set)
    if inter == 0:
        return 0
    #need to account for vertex itself, add 2(1 for each vertex)
    sim = (len(inter) + 2)/(math.sqrt((len(v_set) + 1 )*(len(u_set) + 1)))
    return sim

#this gets the neighborhood of v following the epsilon
def neighborhood(G,v,eps):
    eps_neighbors =[]
    v_list = G.neighbors(v)
    for u in v_list:
        #print(similarity(G,u,v),u,v)
        if(similarity(G,u,v)) > eps:
            eps_neighbors.append(u)
    return eps_neighbors

#is this vertex present in the clique    
def hasLabel(cliques,vertex):
    for k,v in cliques.items():
        if vertex in v:
            return True
    return False

#if u is member
def isNonMember(li,u):
    if u in li:
        return True
    return False

#checks if neighbors of the given vertex u are in the same cluster
def sameClusters(G,clusters,u):
    n = G.neighbors(u)
    #b is belong 
    b = []
    i = 0
    
    while i < len(n):
        for k,v in clusters.items():
            if n[i] in v:
                if k in b:
                    continue
                else:
                    b.append(k)
        i = i + 1
    if len(b) > 1:
        return False
    return True
                
    
    
def scan(G,eps=0.7, mu=2):
    c = 0
    clusters = dict()
    nomembers = []
    for n,nbrs in G.adjacency_iter():
        if hasLabel(clusters,n):
            continue
        else:
        	#get neighborhood and check if vertex is core
            N = neighborhood(G,n,eps)
            if len(N) > mu : #if it passes the epsilon threshold
                #Generate a new cluster-id c
                c = c + 1
                Q = neighborhood(G,n,eps)
                clusters[c] = []
                # append the core vertex itself
                clusters[c].append(n)
                while len(Q) != 0:
                    w = Q.pop(0)
                    R = neighborhood(G,w,eps)
                    # include current vertex itself
                    R.append(w)
                    for s in R:
                        if not(hasLabel(clusters,s)) or isNonMember(nomembers,s):
                            clusters[c].append(s)
                        if not(hasLabel(clusters,s)):
                            Q.append(s)
            else:
                nomembers.append(n)
    outliers = []
    hubs = []
    for v in nomembers:
        if not sameClusters(G,clusters,v):
            hubs.append(v)
        else:
            outliers.append(v)
        

    return clusters,hubs,outliers

                        
                        
def main():
	#build the graph from an edgelist input called " input.edgelist "
    G=nx.Graph()
    fh=open("input.edgelist", 'rb')
    G=nx.read_edgelist(fh)
    fh.close()
    nx.draw(G,with_labels=True)
    
    #display the graph to verify
    plt.show()
    
    #call the SCAN algorithm to return the required values 
    (clusters,hubs,outliers) = scan(G)

    #print out the outputs of the program
    print('Clusters - Set :')
    print 
    for k,v in clusters.items():
        print(k,set(v))
	
    print 
    print('Hubs - Set',set(hubs))
    print 
    ClusterSet=set()
    for i in clusters:
    	for j in clusters[i]:
    		ClusterSet.add(j)
    Nodeset=set(G.nodes())
    OutlierSet=Nodeset-ClusterSet-set(hubs)
    print("Outliers - Set ",OutlierSet)
    print
    
main()




