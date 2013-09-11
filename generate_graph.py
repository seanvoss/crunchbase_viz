import os
import time
import pprint
os.environ['JAVA_HOME'] ='/usr/lib/jvm/java-7-oracle' 
from neo4j import GraphDatabase
import requests
db = GraphDatabase('/var/www/spinner/db_x4')
created = []
nodes = {}

def main():
    r = requests.get('http://api.crunchbase.com/v/1/person/Ron+Conway.js?api_key=b3jdpvrs6r2vbjn8rg5sbz8p');
    print r.status_code
    pprint.pprint(r.json['first_name'])
    # All write operations happen in a transaction
    for a in db.nodes: 
        if a.has_key('name'): 
            nodes[a['name']] = a.id

    with db.transaction:
      name = "%s %s" % (r.json['first_name'], r.json['last_name'] )  
      if nodes.has_key(name):
        node = db.node[nodes[name]]
      else:
        node = db.node(name = "%s %s" % (r.json['first_name'], r.json['last_name'] ))  

      if r.json.has_key('image'):
         sizes = r.json['image']['available_sizes']
         node['image'] = sizes[len(sizes) - 1 ][1]
 

      for attribute in r.json:

        if type(r.json[attribute]) == unicode and  r.json[attribute]:
          node[attribute] = r.json[attribute]

    for relationship in r.json['relationships']:
        with db.transaction:
            print relationship['firm']
            rel = db.node(name=relationship['firm']['name'])
            node.relationships.create(relationship['title'],rel, type_of_relationship = relationship['firm']['type_of_entity'])
            created.append("%s-%s-%s" % ( relationship['title'], node['name'], rel['name'])) 
            r = requests.get('http://api.crunchbase.com/v/1/%s/%s.js?api_key=b3jdpvrs6r2vbjn8rg5sbz8p' %  ( relationship['firm']['type_of_entity'], relationship['firm']['name']  ) );
        i = 0
        make_relationship(r,node,i)
     
    for key, value in node.items():
        print key, value

def make_relationship(r,node,i,clearer=[]):
    i = i + 1
    for a in db.nodes: 
        if a.has_key('name'): 
            nodes[a['name']] = a.id

    if not r.json or r.json.has_key('error') or not r.json['relationships']: return 
    for relationship in r.json['relationships']:

        with db.transaction:
            typeOf = ""
            if  'firm' in relationship: 
                typeOf = 'firm'
                url_stub = 'company'
            if  'person' in relationship: 
                typeOf = 'person'
                url_stub = 'person'

            if typeOf == 'person': relationship[typeOf]['name'] = "%s %s" % (relationship[typeOf]['first_name'], relationship[typeOf]['last_name'] ) 
            if "%s-%s-%s" % ( relationship['title'], relationship[typeOf]['name'], node['name'] ) in created: continue

            name=relationship[typeOf]['name']
            if nodes.has_key(name):
                rel = db.node[nodes[name]] 
            else:
                rel = db.node(name=relationship[typeOf]['name'])


            print relationship[typeOf]
            if relationship.has_key(typeOf) and relationship[typeOf].has_key('image') and relationship[typeOf]['image'] and relationship[typeOf]['image'].has_key('available_sizes') :
                sizes = relationship[typeOf]['image']['available_sizes']
                rel['image'] = sizes[len(sizes) - 1 ][1]
            



            if "%s-%s-%s" % ( relationship['title'], node['name'], rel['name']) in clearer: return
            clearer.append("%s-%s-%s" % ( relationship['title'], node['name'], rel['name'])) 

                
            print relationship[typeOf]['name']
            node.relationships.create(relationship['title'],rel)

            print "%s-%s-%s" % ( relationship['title'], node['name'], rel['name'])
            created.append("%s-%s-%s" % ( relationship['title'], node['name'], rel['name'])) 
            node = rel
            url = 'http://api.crunchbase.com/v/1/%s/%s.js?api_key=b3jdpvrs6r2vbjn8rg5sbz8p' %  ( url_stub, relationship[typeOf]['name'] ) 
            print url
            r = requests.get(url)
            if (i % 5 == 0 ):
                time.sleep(1)
            print len(db.relationships)
        make_relationship(r,node,i)
     

main()
# Read operations can happen anywhere
 
# Always shut down your database when your application exits
db.shutdown()
