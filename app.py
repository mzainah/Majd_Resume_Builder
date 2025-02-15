from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def read_file_lines(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    # Read experience and titles from files
    experiences = read_file_lines('experience.txt')
    titles = read_file_lines('titles.txt')
    return render_template('index.html', experiences=experiences, titles=titles)

@app.route('/build_resume', methods=['POST'])
def build_resume():
    data = request.get_json()
    return jsonify({'status': 'success', 'resume': data})

if __name__ == '__main__':
    app.run(debug=True)