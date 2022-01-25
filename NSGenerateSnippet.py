
import pandas as pd
import json
from rdflib import Graph
import re

df = pd.read_csv("./Namespace/NameSpace.csv", sep=",")
Snipets={}
Snipets['Start-rdf'] = {'prefix': 'Start-rdf',
                        'body': '<?xml version = "1.0" encoding = "UTF-8"?>\n <rdf:RDF xml:base= "$1"\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\nxmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">$0</rdf:RDF>'}
Snipets['add-instance'] = {'prefix': 'add-instance',
                           'body': '<rdf:Description rdf:about="#$1">$0</rdf:Description>'}
for r in range(0,len(df.index)):
    i = df.loc[r]
    name='ns-'+i['ns']
    Snipets[name] = {'prefix': name, 'body': 'xmlns:'+i['link']}
    
 
    if type(i['RdfLink'])==str:
        link = i['RdfLink']
        ns = i['ns']
        g = Graph()
        g.parse(link)
        
        
    
        r1 = g.query(""" 
         PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT  ?C ?L ?D
            WHERE { ?C rdf:type rdfs:Class.
  					optional{?C rdfs:label ?L.}
  					optional{?C rdfs:comment ?D}
  			}""")

        for c in r1:
            a = ns+":"+re.split(r'\/|\#', c[0])[-1]
            name = 'E-'+ns+'-'+re.split(r'\/|\#', c[0])[-1]
            rdftype = '<rdf:type rdf:resource="'+c[0]+'"/>\n'
            Snipets[name] = {'prefix': name, 'body': rdftype, 'description':c[1]+'\n'+c[2]}

        r2 = g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT  ?C ?L ?D
            WHERE {?C rdf:type rdf:Property.
                    optional{?C rdfs:label ?L.}
  					optional{?C rdfs:comment ?D}}""")

        for p in r2:
            a = ns+":"+re.split(r'\/|\#', p[0])[-1]
            name = 'P-'+ns+'-'+re.split(r'\/|\#', p[0])[-1]
            rdftype = '<'+a+'${1| rdf:resource=""/>,></'+a+'>|}\n'
            Snipets[name] = {'prefix': name, 'body': rdftype,'description':p[1]+'\n'+p[2]}


with open('./snippets/snippets.json', 'w') as outfile:
    outfile.write(json.dumps(Snipets))
