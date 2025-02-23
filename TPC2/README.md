# Queries SPARQL sobre a Ontologia da História de Portugal

## 2025/02/23

### 1. Quantos triplos existem na Ontologia?

```sparql
SELECT (COUNT(*) AS ?count) WHERE {
  ?s ?p ?o .
}
```

### 2. Que classes estão definidas?

```sparql
SELECT DISTINCT ?class WHERE {
  ?class a owl:Class .
}
```

### 3. Que propriedades tem a classe "Rei"?

```sparql
SELECT DISTINCT ?property WHERE {
  ?s a :Rei .
  ?s ?property ?o .
}
```

### 4.Quantos reis aparecem na ontologia?

```sparql
SELECT (COUNT(*) as ?count) WHERE {
  ?s a :Rei .
}
```

### 5. Calcula uma tabela com o seu nome, data de nascimento e cognome.

```sparql
SELECT ?nome ?data ?cognome WHERE {
  ?s a :Rei .
  ?s :nome ?nome .
  ?s :nascimento ?data .
  ?s :cognomes ?cognome .
}
```

### 6. Acrescenta à tabela anterior a dinastia em que cada rei reinou.

```sparql
SELECT ?nome ?data ?cognome ?dinastia WHERE {
  ?s a :Rei .
  ?s :nome ?nome .
  ?s :nascimento ?data .
  ?s :cognomes ?cognome .
  ?r :temMonarca ?s .
  ?r :dinastia ?dinastia .
}
```

### 7. Qual a distribuição de reis pelas 4 dinastias?

```sparql
SELECT ?dinastia (COUNT (DISTINCT ?monarca) as ?d) WHERE {
  ?r :dinastia ?dinastia .
  ?r :temMonarca ?monarca .
  ?monarca a :Rei .
} GROUP BY ?dinastia ORDER BY ?dinastia
```

### 8. Lista os descobrimentos (sua descrição) por ordem cronológica.

```sparql
SELECT ?descobrimento ?descricao WHERE {
  ?descobrimento a :Descobrimento .
  ?descobrimento :data ?data .
  ?descobrimento :notas ?descricao .
} ORDER BY ?data
```

### 9. Lista as várias conquistas, nome e data, com o nome do rei que reinava no momento.

```sparql
SELECT ?nome ?data ?nomeMonarca WHERE {
  ?conquista a :Conquista .
  ?conquista :nome ?nome .
  ?conquista :data ?data .
  ?conquista :temReinado ?reinado .
  ?reinado :temMonarca ?monarca .
  ?monarca :nome ?nomeMonarca .
} ORDER BY ?data
```

### 10. Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.

```sparql
SELECT ?nome ?nascimento (COUNT(DISTINCT ?mandato) as ?numMandatos) WHERE {
  ?presidente a :Presidente .
  ?presidente :nome ?nome .
  ?presidente :nascimento ?nascimento .
  ?presidente :mandato ?mandato .
} GROUP BY ?presidente ?nome ?nascimento
```
### 11. Quantos mandatos teve o presidente Sidónio Pais? Em que datas iniciaram e terminaram esses mandatos?

```sparql
SELECT (COUNT(DISTINCT ?mandato) as ?numMandatos) ?dataInicio ?dataFim WHERE {
  ?presidente a :Presidente .
  ?presidente :nome "Sidónio Bernardino Cardoso da Silva Pais" .
  ?presidente :mandato ?mandato .
  ?mandato :comeco ?dataInicio .
  ?mandato :fim ?dataFim .
} GROUP BY ?presidente ?dataInicio ?dataFim
```

### 12. Quais os nomes dos partidos politicos presentes na ontologia?

```sparql
SELECT ?nome WHERE {
  ?partido a :Partido .
  ?partido :nome ?nome .
}
```

### 13. Qual a distribuição dos militantes por cada partido politico?

```sparql
SELECT ?partido (COUNT(DISTINCT ?militante) as ?numMilitantes) WHERE {
  ?partido a :Partido .
  ?partido :temMilitante ?militante .
} GROUP BY ?partido
```

### 14. Qual o partido com maior número de presidentes militantes?

```sparql
SELECT ?partido ?nome (COUNT(DISTINCT ?militante) as ?numMilitantes) WHERE {
  ?partido a :Partido .
  ?partido :nome ?nome .
  ?partido :temMilitante ?militante .
  ?militante a :Presidente .
} GROUP BY ?partido ?nome ORDER BY DESC(?numMilitantes) LIMIT 1
```