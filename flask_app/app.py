#!/usr/bin/env python3
from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# ================================
# Exemple simple d’IA : chatbot simulé
# ================================
def ia_chatbot(user_input):
    responses = [
        "Je suis une IA, je comprends que tu dis : " + user_input,
        "Intéressant 🤔, peux-tu développer sur : " + user_input,
        "Super idée ! Merci d'avoir partagé : " + user_input,
        "Hmm... je vais réfléchir sur : " + user_input
    ]
    return random.choice(responses)

# ================================
# Frontend HTML avec Bootstrap
# ================================
base_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Projet Flask IA</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #f8f9fa; }
    .navbar { margin-bottom: 20px; }
    .chat-box {
      background: white;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .message-user { color: blue; font-weight: bold; }
    .message-ia { color: green; font-style: italic; }
  </style>
</head>
<body>
  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Projet IA Flask</a>
      <div>
        <a class="btn btn-outline-light me-2" href="/">Accueil</a>
        <a class="btn btn-outline-light" href="/chat">Chatbot IA</a>
      </div>
    </div>
  </nav>

  <div class="container">
    {% block content %}{% endblock %}
  </div>
</body>
</html>
"""

# ================================
# Routes
# ================================
@app.route('/')
def home():
    return render_template_string(base_template + """
    {% block content %}
    <div class="text-center">
      <h1 class="display-4">Bienvenue 🚀</h1>
      <p class="lead">Ceci est un projet Flask amélioré avec IA et Bootstrap.</p>
      <a href="/chat" class="btn btn-primary btn-lg">Tester le Chatbot IA</a>
    </div>
    {% endblock %}
    """)

@app.route('/hello/<username>')
def hello_user(username):
    return render_template_string(base_template + """
    {% block content %}
    <h2>Bonjour {{ username }} 👋</h2>
    <p>Ravi de te voir sur notre serveur Flask IA.</p>
    {% endblock %}
    """, username=username)

@app.route('/chat', methods=["GET", "POST"])
def chat():
    user_message = None
    ia_response = None
    if request.method == "POST":
        user_message = request.form.get("message")
        ia_response = ia_chatbot(user_message)
    return render_template_string(base_template + """
    {% block content %}
    <div class="chat-box">
      <h3 class="mb-4">Chatbot IA 🤖</h3>
      <form method="POST">
        <div class="mb-3">
          <label for="message" class="form-label">Votre message :</label>
          <input type="text" class="form-control" id="message" name="message" placeholder="Écrivez ici..." required>
        </div>
        <button type="submit" class="btn btn-success">Envoyer</button>
      </form>

      {% if user_message %}
      <hr>
      <p class="message-user">👤 Vous : {{ user_message }}</p>
      <p class="message-ia">🤖 IA : {{ ia_response }}</p>
      {% endif %}
    </div>
    {% endblock %}
    """, user_message=user_message, ia_response=ia_response)

# ================================
# Lancement
# ================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

