from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
import csv

EX = Namespace("http://www.example.org/disease-ontology#")

existing_graph = Graph()
existing_graph.parse("medical.ttl", format="turtle")

new_graph = Graph()
description_graph = Graph()

new_graph.bind("", EX)
new_graph.bind("owl", OWL)
new_graph.bind("rdf", RDF)
new_graph.bind("rdfs", RDFS)


new_graph.add((EX.Ontology, RDF.type, OWL.Ontology))

new_graph.add((EX.Disease, RDF.type, OWL.Class))
new_graph.add((EX.Symptom, RDF.type, OWL.Class))
new_graph.add((EX.Treatment, RDF.type, OWL.Class))
new_graph.add((EX.Patient, RDF.type, OWL.Class))

new_graph.add((EX.hasSymptom, RDF.type, OWL.ObjectProperty))
new_graph.add((EX.hasSymptom, RDFS.domain, EX.Disease))
new_graph.add((EX.hasSymptom, RDFS.range, EX.Symptom))

new_graph.add((EX.hasTreatment, RDF.type, OWL.ObjectProperty))
new_graph.add((EX.hasTreatment, RDFS.domain, EX.Disease))
new_graph.add((EX.hasTreatment, RDFS.range, EX.Treatment))

description_graph.add((EX.hasDescription, RDF.type, OWL.DatatypeProperty))
description_graph.add((EX.hasDescription, RDFS.domain, EX.Disease))
description_graph.add((EX.hasDescription, RDFS.range, RDFS.Literal))

with open("../datasets/Disease_Syntoms.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    symptoms_set = set()

    for row in reader:
        disease = row["Disease"].strip().replace(" ", "_")
        disease_uri = EX[disease]
        new_graph.add((disease_uri, RDF.type, EX.Disease))

        symptoms = [
            row[f"Symptom_{i}"].strip().replace(" ", "_")
            for i in range(1, 18)
            if row[f"Symptom_{i}"]
        ]

        for symptom in symptoms:
            symptom_uri = EX[symptom]
            new_graph.add((symptom_uri, RDF.type, EX.Symptom))
            new_graph.add((disease_uri, EX.hasSymptom, symptom_uri))
            symptoms_set.add(symptom)

with open("../datasets/Disease_Description.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        disease = row["Disease"].strip().replace(" ", "_")
        description = row["Description"].strip()
        disease_uri = EX[disease]
        description_graph.add((disease_uri, EX.hasDescription, Literal(description)))

existing_graph += new_graph

existing_graph.serialize(destination="1-3_ontologia.ttl", format="turtle")

existing_graph += description_graph
existing_graph.serialize(destination="med_doencas.ttl", format="turtle")

with open("../datasets/Disease_Treatment.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    treatments_set = set()
    
    for row in reader:
        disease = row["Disease"].strip().replace(" ", "_")
        disease_uri = EX[disease]
        
        for i in range(1, 5):
            treatment = row[f"Precaution_{i}"].strip()
            if treatment:
                treatment_uri = EX[treatment.replace(" ", "_")]
                
                if treatment not in treatments_set:
                    new_graph.add((treatment_uri, RDF.type, EX.Treatment))
                    treatments_set.add(treatment)
                
                new_graph.add((disease_uri, EX.hasTreatment, treatment_uri))

existing_graph += new_graph
existing_graph.serialize(destination="med_tratamentos.ttl", format="turtle")


