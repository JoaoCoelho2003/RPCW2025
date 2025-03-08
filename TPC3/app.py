from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import CORS
import random
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

def get_rei_questions():
    sparql = SPARQLWrapper("http://localhost:7200/repositories/HistoriaPortugal")
    sparql.setReturnFormat(JSON)

    # 1. Consulta sobre a quantidade de reis
    sparql.setQuery("""
    PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    
    SELECT (COUNT(*) as ?count) WHERE {
      ?s a historia:Rei .
    }
    """)
    result_reis = sparql.query().convert()
    num_reis = result_reis['results']['bindings'][0]['count']['value']

    # 2. Consulta sobre as dinastias
    sparql.setQuery("""
    PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    
    SELECT DISTINCT ?dinastia WHERE {
      ?r historia:dinastia ?dinastia .
    }
    """)
    result_dinastias = sparql.query().convert()
    dinastias = [r['dinastia']['value'].split('#')[-1] for r in result_dinastias['results']['bindings']]

    # 3. Consulta sobre os descobrimentos
    sparql.setQuery("""
    PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    
    SELECT ?descobrimento ?descricao WHERE {
      ?descobrimento a historia:Descobrimento .
      ?descobrimento historia:data ?data .
      ?descobrimento historia:notas ?descricao .
    } ORDER BY ?data
    """)
    result_descobrimentos = sparql.query().convert()
    descobrimentos = [(r['descobrimento']['value'].split('#')[-1], r['descricao']['value']) for r in result_descobrimentos['results']['bindings']]

    # 4. Consulta sobre conquistas e o nome do monarca
    sparql.setQuery("""
    PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    
    SELECT ?nome ?data ?nomeMonarca WHERE {
      ?conquista a historia:Conquista .
      ?conquista historia:nome ?nome .
      ?conquista historia:data ?data .
      ?conquista historia:temReinado ?reinado .
      ?reinado historia:temMonarca ?monarca .
      ?monarca historia:nome ?nomeMonarca .
    } ORDER BY ?data
    """)
    result_conquistas = sparql.query().convert()
    conquistas = [(r['nome']['value'], r['data']['value'], r['nomeMonarca']['value']) for r in result_conquistas['results']['bindings']]

    questions = []

    # Pergunta sobre o número de reis
    questions.append({
        "question": f"Quantos reis existem na ontologia?",
        "options": [str(num_reis), str(int(num_reis) + random.randint(1, 10)), str(int(num_reis) - random.randint(1, 10))],
        "answer": str(num_reis),
        "type": 'multiple_choice'
    })

    # Pergunta sobre dinastia
    dinastia = random.choice(dinastias)
    questions.append({
        "question": f"Qual das dinastias teve mais reis?",
        "options": dinastias,
        "answer": dinastia,
        "type": 'multiple_choice'
    })

    # Pergunta sobre descobrimentos
    descobrimento, descricao = random.choice(descobrimentos)
    questions.append({
        "question": f"Qual foi o descobrimento relacionado com: {descricao[:50]}...?",
        "options": [descobrimento, random.choice(descobrimentos)[0], random.choice(descobrimentos)[0]],
        "answer": descobrimento,
        "type": 'multiple_choice'
    })

    # Pergunta sobre uma conquista histórica
    conquista, data, nome_monarca = random.choice(conquistas)
    other_monarchs = random.sample([m[2] for m in conquistas if m[2] != nome_monarca], 2)
    questions.append({
        "question": f"Quem era o monarca durante a conquista de {conquista} em {data}?",
        "options": [nome_monarca] + other_monarchs,
        "answer": nome_monarca,
        "type": 'multiple_choice'
    })

    # Pergunta de Verdadeiro ou Falso sobre uma dinastia
    question_dinastia = random.choice(dinastias)
    correct_answer = 'Verdadeiro' if random.choice([True, False]) else 'Falso'
    questions.append({
        "question": f"A {question_dinastia} teve mais de 10 reis?",
        "answer": correct_answer,
        "type": 'true_false'
    })
    
    # Questão de correspondência entre monarcas e conquistas
    monarch_conquests = [(r['nomeMonarca']['value'], r['nome']['value']) for r in result_conquistas['results']['bindings']]
    
    unique_monarch_conquests = {}
    for monarch, conquest in monarch_conquests:
        if monarch not in unique_monarch_conquests:
            unique_monarch_conquests[monarch] = conquest
    
    selected_monarch_conquests = random.sample(list(unique_monarch_conquests.items()), 3)
    
    monarchs = [pair[0] for pair in selected_monarch_conquests]
    conquests = [pair[1] for pair in selected_monarch_conquests]
    
    random.shuffle(conquests)

    correspondence_question = {
        "question": "Associe os monarcas às suas conquistas:",
        "options": list(zip(monarchs, conquests)),
        "answer": monarchs,
        "type": 'correspondence'
    }
    
    questions.append(correspondence_question)

    return questions

test_questions = get_rei_questions()

@app.route('/')
def home():
    session['score'] = 0
    session['questions_answered'] = []
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    remaining_questions = [q for q in test_questions if q['question'] not in session['questions_answered']]
    
    if not remaining_questions:
        return redirect(url_for('score'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')
        
        for question in test_questions:
            if question['question'] == question_text:
                correct = question['answer'] == user_answer
                session['score'] = session.get('score', 0) + (1 if correct else 0)
                session['questions_answered'].append(question['question'])
                return render_template('result.html', correct=correct, correct_answer=question['answer'], score=session['score'])
    
    question = random.choice(remaining_questions)
    return render_template('quiz.html', question=question)

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
