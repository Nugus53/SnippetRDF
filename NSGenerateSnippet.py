
import pandas as pd
import json
from rdflib import Graph
import re

df = pd.read_csv("./Namespace/NameSpace.csv", sep=",")
Snipets={}

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
            SELECT DISTINCT  ?C 
            WHERE { ?C rdf:type rdfs:Class.}""")

        for c in r1:
            a = ns+":"+re.split(r'\/', c[0])[-1]
            name = 'E-'+ns+'-'+re.split(r'\/', c[0])[-1]
            rdftype = '<rdf:type rdf:resource="'+c[0]+'"/>\n'
            Snipets[name] = {'prefix': name, 'body': rdftype}

        r2 = g.query("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT  ?C 
            WHERE {?C rdf:type rdf:Property.}""")

        for p in r2:
            a = ns+":"+re.split(r'\/', p[0])[-1]
            name = 'P-'+ns+'-'+re.split(r'\/', p[0])[-1]
            rdftype = '<'+a+'/>\n'
            Snipets[name] = {'prefix': name, 'body': rdftype}


with open('./snippets/snippets.json', 'W') as outfile:
    outfile.write(json.dumps(Snipets))
