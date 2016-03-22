from random import random
from PIL import Image, ImageDraw
import sys

if len(sys.argv) < 2:
    print "Usage: python dbscan.py <path_to_wallpaper>"
    exit()

def getPts(px, (w, h)):
	#this prints out the points in the form (x,y):0
    return { (x, y): px[x,y] for x in range(w) for y in range(h) }

def dist(pts, a, b): # px : pixel map , a :current point tuple , b:passed point tuple
    # print pts[b]
    s = ((px[a] - px[b]) ** 2) * colorCoef
    s += sum([(a[i] - b[i]) ** 2 for i in range(2)]) * distCoef
    return s

def eNeighborhood(pts, (x, y), e):
	#this function will take in all the points, current point, e
	#if the radius criteria is satisfied it will append to n ( so it can be allowed in neighborhood!)
    n = []
    minx, miny = (max(0, x - e), max(0, y - e))
    #size(0) : gives width while size(1): height
    maxx, maxy = (min(size[0], x + e), min(size[1], y + e))
    e = (e ** 2);
    for j in xrange(miny, maxy):
        for i in xrange(minx, maxx):
            if (i, j) not in pts:
                continue
            #get the distance function of current point to all other points in neighbourhood
            d = dist(pts, (x, y), (i, j))
            if d < e:
                n.append((i, j))
    return n

def getCluster(pts, curr, neighbors, e, clustersz):
    cluster = [curr] # this has the current core node in a list
    while len(neighbors):
        pt = neighbors.pop()
        if pt in pts: # remove the point from all the points as its now in a cluster
            ptneighbors = eNeighborhood(pts, pt, e) # check if the neighbours should be in a cluster for this point
            del pts[pt]
            if ptneighbors >= clustersz:
                neighbors += ptneighbors
            cluster.append(pt) # add the neighbour to the cluster
    return cluster

#this function does the main DBSCAN algo
def dbscan(pts, e, clustersz):
    clusters = [] # list of lists 
    while len(pts):
    	#we should get (,):0
        key, value = pts.popitem()
        #check if it is in the neighbourhood list n
        n = eNeighborhood(pts, key, e)
        #now check if minPoint criteria is satisfied !
        if len(n) >= clustersz:
        	#add the cluster to the clusters list 
            clusters.append(getCluster(pts, key, n, e, clustersz))
    return clusters

def display(width,height,pts,clusters):
	print("Number of points in the image originally : ",width*height)
	print("Number of clusters found : ",len(clusters))
	print("Number of noise points that remain : ",len(pts))
	print("__________________________________________________________________________")
	print()
	print("              Cluster Table ")
	print("__________________________________________________________________________")
	
	

	template="{0:10}|{1:20}|{2:25}"
	print(template.format("Cluster","Cluster Size","Avg Cluster Color"))
	print()
	i=0
	for c in clusters:
		avg = 0
		for pt in c:
			avg += px[pt]
		avg /= len(c)
		print(template.format(str(i),str(len(c)),str(avg)))
		#print(str(i)+""+str(len(c))+"\t\t"+str(avg)+"\n")
		i+=1

#opens image from commandline
img = Image.open(sys.argv[1])
#will resize the image to 200X200
# img = img.resize((200, 200), Image.ANTIALIAS)

img.show()
img.save("orig.png")
# stores the image
width,height=img.size
size=(width,height)
out = Image.new("RGB", size)
outpx = out.load()
#this prcesses the image
px = img.load()
#gets points from Image
pts = getPts(px, size)

#set the coefficients
colorCoef = 1.0
distCoef = 1.00
#get the clusters with three arguments : pts : points e:neighborhood-radius clustersz:1 , number of points in a cluster
clusters = dbscan(pts, 4, 22)

display(width,height,pts,clusters)

for c in clusters:
    
    avg = 0
    for pt in c:
        avg += px[pt]
    avg /= len(c)
    for pt in c:
        outpx[pt] =(avg,avg,avg)

#img.show()
#img.save("convert.png")
out.convert('RGB')
out.show()
out.save("rendered.png")
