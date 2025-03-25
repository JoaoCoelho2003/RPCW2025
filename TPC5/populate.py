import json

with open("moviesFinal.json", "r", encoding="utf-8") as file:
    data = json.load(file)

rdf_output = ""

for id, name in data["allPeople"].items():
    rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{id}
:{id} rdf:type owl:NamedIndividual ,
						:Pessoa ;
			   :nome "{name}" .
"""

for id in data["allCountries"]:
    rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{id}
:{id} rdf:type owl:NamedIndividual ,
						 :Pais .
"""

for id in data["allLanguages"]:
    rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{id}
:{id} rdf:type owl:NamedIndividual ,
				  :Lingua .
"""

for id in data["allGenres"]:
    rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{id}
:{id} rdf:type owl:NamedIndividual ,
				   :Genero .
"""

for movie in data["movies"]:
    id = movie["id"]
    genres = ",".join([f":{t}" for t in movie["genres"]])
    originalLanguage = movie["originalLanguage"]
    og = ""

    if originalLanguage:
        og = f":temLingua :{originalLanguage};"

    rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{id}
:{id} rdf:type owl:NamedIndividual ,
				   :Filme ;
		  :temArgumento :Argumento_{id} ;
		  :temGenero {genres} ;
		  {og}
		  :temPaisOrigem :{movie["originalCountry"]} ;
		  :data "{int(movie["releaseYear"])}" ;  # Aqui garantimos que a data seja um inteiro
		  :duracao {movie["duration"]} .
"""

    for person in movie["peopleInvolved"]:
        person_id = person["nconst"]
        rdf_output += f"""
###  http://www.semanticweb.org/jojocoelho/ontologies/2025/cinema/{person_id}
:{person_id} rdf:type owl:NamedIndividual ,
                          :Pessoa ;
               :nome "{person["name"]}" ;
               :funcao "{person["job"]}" ;
               :categoria "{person["category"]}" .
"""

with open("final.ttl", "w", encoding="utf-8") as ttl_file:
    ttl_file.write(rdf_output)

print("O ficheiro final.ttl foi gerado com sucesso!")
