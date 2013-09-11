from gexf import *
import os
import time
import pprint
import random
os.environ['JAVA_HOME'] ='/usr/lib/jvm/java-7-oracle' 
from neo4j import GraphDatabase
import requests
gexf = Gexf("Sean Voss","Crunchbase") 
graph=gexf.addGraph("directed","static","a graph")
created = []
i = 0
db = GraphDatabase('/var/www/spinner/db1')
print len(db.nodes)

for a in db.nodes:

    if a.has_key('name'):
        node = graph.addNode(a.id,a['name'].encode('ascii', 'ignore')) 
        node.setColor(unicode(random.randrange(1,255)),unicode(random.randrange(1,255)),unicode(random.randrange(1,255)))



        #node.addAttribute('size',len(a.relationships))
       
for a in db.nodes:
    if a.has_key('name'):
        #graph.addNode(a.id,a['name']) 

        #gexf_sm  = Gexf("Sean Voss","Crunchbase") 
        #graph_sm = gexf_sm.addGraph("directed","static","a graph")
        #node2 = graph_sm.addNode(a.id,a['name'].encode('ascii', 'ignore')) 
        #node2.setColor(unicode(random.randrange(1,255)),unicode(random.randrange(1,255)),unicode(random.randrange(1,255)))

        for rel in a.relationships:
            if rel.start.has_key('image'): print rel.start['image']
            print rel.start['name'] + ' ---> ' + rel.end['name']
            print dict(rel.end)
            #rel2 = graph_sm.addNode(unicode(rel.start.id),rel.start['name'].encode('ascii', 'ignore')) 
            #rel2.setColor(unicode(random.randrange(1,255)),unicode(random.randrange(1,255)),unicode(random.randrange(1,255)))
            #rel3 = graph_sm.addNode(rel.end.id,rel.end['name'].encode('ascii', 'ignore')) 
            #rel3.setColor(unicode(random.randrange(1,255)),unicode(random.randrange(1,255)),unicode(random.randrange(1,255)))


            edge = graph.addEdge(i,rel.start.id,rel.end.id)
            #edge2 = graph_sm.addEdge(i,a.id,rel.end.id)
            #edge.setColor(random.randrange(1,255),random.randrange(1,255),random.randrange(1,255))
            i += 1
        #output_file=open("graphs/%s.gexf" % a['name'],"w") 
        #gexf.write(output_file)

output_file=open("hellworld.gexf","w") 
gexf.write(output_file)



