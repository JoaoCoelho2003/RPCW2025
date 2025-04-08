from rdflib import OWL, RDF, Graph, Namespace

n = Namespace("http://www.example.org/disease-ontology#")

g = Graph()
g.parse("med_doentes.ttl")

print("Quantas doenças estão presentes na ontologia?")

q = """
SELECT (COUNT(?d) AS ?number)
WHERE {
	?d a :Disease .
}
"""

for r in g.query(q):
    print(f"Number of diseases: {r[0]}")

print("\nQue doenças estão associadas ao sintoma yellowish_skin?")

q = """
SELECT ?d {
	?d a :Disease .
	?d :hasSymptomD :yellowish_skin .
}
"""

for r in g.query(q):
    print(f"Disease: {r[0].split('#')[1]}")

print("\nQue doenças estão associadas ao tratamento exercise?")

q = """
SELECT ?d {
	?d a :Disease .
	?d :hasTreatment :exercise .
}
"""

for r in g.query(q):
    print(f"Disease: {r[0].split('#')[1]}")

print("\nProduz uma lista ordenada alfabeticamente com o nome dos doentes.")

q = """
SELECT ?p
WHERE {
	?p a :Patient .
	?p :hasName ?name .
}
ORDER BY ?name
"""

for r in g.query(q):
    print(f"Patient: {r[0].split('#')[1]}")
