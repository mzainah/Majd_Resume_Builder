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
            # Expected format: "Title | Company | StartDate-EndDate"
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

def read_experiences(filename):
    # Get absolute path
    file_path = os.path.join(os.path.dirname(__file__), filename)
    print(f"Attempting to read experiences from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            experiences = [line.strip() for line in file if line.strip()]
            print(f"Read {len(experiences)} experiences:")
            for exp in experiences:
                print(f"- {exp}")
            return experiences
    except FileNotFoundError:
        print(f"Experience file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading experience file: {e}")
        return []

def read_titles(filename):
    # Get absolute path
    file_path = os.path.join(os.path.dirname(__file__), filename)
    print(f"Attempting to read titles from: {file_path}")
    
    titles = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Read {len(lines)} lines from titles file:")
            for line in lines:
                line = line.strip()
                print(f"Processing line: {line}")
                if line:
                    job_title = JobTitle.from_line(line)
                    if job_title:
                        titles.append(job_title)
                        print(f"Added title: {job_title.title} at {job_title.company}")
    except FileNotFoundError:
        print(f"Titles file not found: {file_path}")
    except Exception as e:
        print(f"Error reading titles file: {e}")
    
    print(f"Total titles processed: {len(titles)}")
    return titles

@app.route('/')
def index():
    # Read experiences and titles from files
    print("\n=== Reading Experiences ===")
    experiences = read_experiences('experience.txt')
    
    print("\n=== Reading Titles ===")
    titles = read_titles('titles.txt')
    
    # Convert titles to dictionary for template
    title_dicts = [
        {
            'title': title.title,
            'company': title.company,
            'start_date': title.start_date,
            'end_date': title.end_date
        }
        for title in titles
    ]
    
    print(f"\nSending to template:")
    print(f"- {len(experiences)} experiences")
    print(f"- {len(title_dicts)} titles")
    
    return render_template('index.html', 
                         experiences=experiences, 
                         titles=title_dicts)

@app.route('/build_resume', methods=['POST'])
def build_resume():
    data = request.get_json()
    return jsonify({'status': 'success', 'resume': data})

if __name__ == '__main__':
    app.run(debug=True)