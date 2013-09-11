import os
import time
import pprint
os.environ['JAVA_HOME'] ='/usr/lib/jvm/java-7-oracle' 
from neo4j import GraphDatabase
import requests
created = []
db = GraphDatabase('/var/www/spinner/db1')
print len(db.nodes)
for a in db.nodes:
    if a.has_key('name'): print a['name']
    print len(a.relationships)
    for rel in a.relationships:
        if rel.start.has_key('image'): print rel.start['image']
        print rel.start['name'] + ' ---> ' + rel.end['name']
