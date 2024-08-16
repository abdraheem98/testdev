from flask import Flask, jsonify, request, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='mydatabase',
        user='user',
        password='password',
        host='db'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/greetings', methods=['GET'])
def get_greetings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM greetings LIMIT 1;')
    message = cursor.fetchone()
    conn.close()
    if message:
        return jsonify(message[0])
    else:
        return jsonify("No greeting found")

@app.route('/api/add', methods=['POST'])
def add():
    new_message = request.json.get('message')
    if not new_message:
        return jsonify({"error": "Message is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO greetings (message) VALUES (%s);', (new_message,))
    conn.commit()
    conn.close()
    return jsonify({"status": "Message added"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
