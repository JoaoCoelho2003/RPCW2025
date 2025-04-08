from rdflib import OWL, RDF, Graph, Namespace, URIRef

n = Namespace("http://www.example.org/disease-ontology#")

g = Graph()
g.parse("med_doentes.ttl")

query = """
CONSTRUCT {
	?patient :hasDisease ?disease .
}
WHERE {
	?patient :hasSymptomP ?symptom1, ?symptom2, ?symptom3 .
	?disease :hasSymptomD ?symptom1, ?symptom2, ?symptom3 .
	FILTER(?symptom1 != ?symptom2 && ?symptom1 != ?symptom3 && ?symptom2 != ?symptom3)
}
"""

new_triples = g.query(query)

for triple in new_triples:
    g.add(triple)

g.serialize(destination="med_doentes_diagnosticados.ttl", format="turtle")
