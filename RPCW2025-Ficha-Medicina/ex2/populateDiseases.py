import csv

with open('diseases.ttl', 'w') as ttl_file:
	ttl_file.write('@prefix : <http://www.example.org/disease-ontology#> .\n')
	ttl_file.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
	ttl_file.write('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n')
	ttl_file.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
	ttl_file.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')

	with open('../datasets/Disease_Syntoms.csv', 'r') as csv_file:
		reader = csv.DictReader(csv_file)
		disease_symptoms = {}
		disease_treatments = {}
		symptoms_set = set()
		treatments_set = set()

		for row in reader:
			disease = row['Disease'].strip().replace(' ', '_')
			symptoms = [row[f'Symptom_{i}'].strip().replace(' ', '_') for i in range(1, 18) if row[f'Symptom_{i}']]
			treatments = [row[f'Treatment_{i}'].strip().replace(' ', '_') for i in range(1, 6) if row.get(f'Treatment_{i}')]

			if disease not in disease_symptoms:
				disease_symptoms[disease] = set()
			disease_symptoms[disease].update(symptoms)

			if disease not in disease_treatments:
				disease_treatments[disease] = set()
			disease_treatments[disease].update(treatments)

			symptoms_set.update(symptoms)
			treatments_set.update(treatments)

		for disease, symptoms in disease_symptoms.items():
			ttl_file.write(f':{disease} a :Disease ;\n')
			ttl_file.write(f'\t:hasSymptom {", ".join(f":{symptom}" for symptom in symptoms)} ;\n')
			if disease in disease_treatments:
				ttl_file.write(f'\t:hasTreatment {", ".join(f":{treatment}" for treatment in disease_treatments[disease])} .\n\n')
			else:
				ttl_file.write('.\n\n')

		for symptom in symptoms_set:
			ttl_file.write(f':{symptom} a :Symptom .\n')

		ttl_file.write('\n')

		for treatment in treatments_set:
			ttl_file.write(f':{treatment} a :Treatment .\n')