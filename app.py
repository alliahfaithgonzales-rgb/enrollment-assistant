from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load FAQ knowledge base
with open('faq.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

def find_answer(user_query):
    """Find the best matching answer from FAQ"""
    query_words = user_query.lower().split()
    
    best_match = None
    max_matches = 0
    
    for key, item in faq_data.items():
        score = 0
        for keyword in item['keywords']:
            if keyword in user_query.lower():
                score += 1
        if score > max_matches:
            max_matches = score
            best_match = item
    
    if best_match:
        return best_match['answer']
    return "Sorry, I don't have an answer for that yet. Please contact the Registrar's Office directly."

@app.route('/')
def home():
    return """
    <html>
    <body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px;">
        <h1>📚 Enrollment Helpdesk Assistant</h1>
        <p>Ask me anything about enrollment!</p>
        
        <div style="margin: 20px 0;">
            <input type="text" id="question" placeholder="Type your question here..." 
                   style="width: 70%; padding: 10px; font-size: 16px;">
            <button onclick="sendQuestion()" 
                    style="padding: 10px 20px; font-size: 16px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Send
            </button>
        </div>
        
        <div id="answer" style="margin-top: 30px; padding: 15px; background: #f0f0f0; border-radius: 4px; display: none;"></div>
        
        <script>
            async function sendQuestion() {
                const q = document.getElementById('question').value;
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                const ansDiv = document.getElementById('answer');
                ansDiv.style.display = 'block';
                ansDiv.innerHTML = "<strong>Q:</strong> " + data.question + "<br><strong>A:</strong> " + data.answer;
            }
        </script>
    </body>
    </html>
    """
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_question = data.get('question', '')
    
    if not user_question:
        return jsonify({"error": "Please provide a question"}), 400
    
    answer = find_answer(user_question)
    
    return jsonify({
        "question": user_question,
        "answer": answer
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)