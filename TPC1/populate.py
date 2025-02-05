import json
from rdflib import Graph, URIRef, Literal, XSD, RDF

BASE_URI = "http://www.semanticweb.org/jojocoelho/ontologies/2025/tpc1/"

graph = Graph()
graph.parse("tpc1_turtle.ttl", format="ttl")

with open('datasets/emd.json', 'r') as file:
    dataset = json.load(file)

temExame = URIRef(BASE_URI + "temExame")
temModalidade = URIRef(BASE_URI + "temModalidade")

_id = URIRef(BASE_URI + "_id")
primeiroNome = URIRef(BASE_URI + "primeiroNome")
ultimoNome = URIRef(BASE_URI + "ultimoNome")
idade = URIRef(BASE_URI + "idade")
genero = URIRef(BASE_URI + "genero")
morada = URIRef(BASE_URI + "morada")
email = URIRef(BASE_URI + "email")
federado = URIRef(BASE_URI + "federado")
resultado = URIRef(BASE_URI + "resultado")
dataEMD = URIRef(BASE_URI + "dataEMD")
nomeModalidade = URIRef(BASE_URI + "nomeModalidade")
clube = URIRef(BASE_URI + "clube")

def add_pessoa(graph, pessoa_id, primeiro_nome, ultimo_nome, idade_value, genero_value, morada_value, email_value, federado_value, modalidade_uri, exame_uri):
    pessoa_uri = URIRef(BASE_URI + "Pessoa/" + pessoa_id)
    
    graph.add((pessoa_uri, RDF.type, URIRef(BASE_URI + "Pessoa")))
    graph.add((pessoa_uri, _id, Literal(pessoa_id, datatype=XSD.string)))
    graph.add((pessoa_uri, primeiroNome, Literal(primeiro_nome, datatype=XSD.string)))
    graph.add((pessoa_uri, ultimoNome, Literal(ultimo_nome, datatype=XSD.string)))
    graph.add((pessoa_uri, idade, Literal(idade_value, datatype=XSD.int)))
    graph.add((pessoa_uri, genero, Literal(genero_value, datatype=XSD.string)))
    graph.add((pessoa_uri, morada, Literal(morada_value, datatype=XSD.string)))
    graph.add((pessoa_uri, email, Literal(email_value, datatype=XSD.string)))
    graph.add((pessoa_uri, federado, Literal(federado_value, datatype=XSD.boolean)))
    
    graph.add((pessoa_uri, temModalidade, modalidade_uri))
    graph.add((pessoa_uri, temExame, exame_uri))

for entry in dataset:
    modalidade_uri = URIRef(BASE_URI + "Modalidade/" + entry["modalidade"])
    exame_uri = URIRef(BASE_URI + "Exame/" + entry["_id"])

    add_pessoa(graph, str(entry["_id"]), entry["nome"]["primeiro"], entry["nome"]["último"], 
               entry["idade"], entry["género"], entry["morada"], entry["email"], 
               entry["federado"], modalidade_uri, exame_uri)

    graph.add((exame_uri, RDF.type, URIRef(BASE_URI + "Exame")))
    graph.add((exame_uri, _id, Literal(str(entry["_id"]), datatype=XSD.string)))
    graph.add((exame_uri, dataEMD, Literal(entry["dataEMD"], datatype=XSD.string)))
    graph.add((exame_uri, resultado, Literal(entry["resultado"], datatype=XSD.boolean)))

    graph.add((modalidade_uri, RDF.type, URIRef(BASE_URI + "Modalidade")))
    graph.add((modalidade_uri, nomeModalidade, Literal(entry["modalidade"], datatype=XSD.string)))
    graph.add((modalidade_uri, clube, Literal(entry["clube"], datatype=XSD.string)))

graph.serialize(destination="final.ttl", format="turtle")
