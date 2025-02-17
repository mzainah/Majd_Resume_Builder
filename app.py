from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

class JobTitle:
    def __init__(self, title, company, start_date, end_date):
        self.title = title
        self.company = company
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_line(cls, line):
        try:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) == 3:
                title = parts[0]
                company = parts[1]
                dates = parts[2].split('-')
                start_date = dates[0].strip()
                end_date = dates[1].strip() if len(dates) > 1 else "Present"
                return cls(title, company, start_date, end_date)
        except Exception as e:
            print(f"Error parsing line: {line}, Error: {e}")
        return None

def read_file_content(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    print(f"Attempting to read from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip() and not line.strip().upper() == 'SKILLS']
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def read_experiences():
    return read_file_content('experience.txt')

def read_titles():
    titles = []
    for line in read_file_content('titles.txt'):
        job_title = JobTitle.from_line(line)
        if job_title:
            titles.append(job_title)
    return titles

def read_skills():
    skills = read_file_content('skills.txt')
    return sorted(skills)  # Sort skills alphabetically

@app.route('/')
def index():
    experiences = read_experiences()
    titles = read_titles()
    skills = read_skills()
    
    title_dicts = [
        {
            'title': title.title,
            'company': title.company,
            'start_date': title.start_date,
            'end_date': title.end_date
        }
        for title in titles
    ]
    
    print(f"\nLoaded data:")
    print(f"- {len(experiences)} experiences")
    print(f"- {len(title_dicts)} titles")
    print(f"- {len(skills)} skills")
    
    return render_template('index.html', 
                         experiences=experiences, 
                         titles=title_dicts,
                         skills=skills)

@app.route('/build_resume', methods=['POST'])
def build_resume():
    data = request.get_json()
    return jsonify({'status': 'success', 'resume': data})

@app.route('/help')
def help():
     return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)