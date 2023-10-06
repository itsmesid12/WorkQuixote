from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

# Sample job data
job_postings = [
    {
        "title": "Software Engineer",
        "company": "TechCo",
        "location": "New York",
        "description": "Looking for a software engineer with Python expertise.",
    },
    {
        "title": "Data Scientist",
        "company": "DataCorp",
        "location": "San Francisco",
        "description": "Data scientist needed to analyze large datasets.",
    },
    {
        "title": "Web Developer",
        "company": "WebDev Inc.",
        "location": "Los Angeles",
        "description": "Front-end web developer with HTML, CSS, and JavaScript skills.",
    },
    # Add more job postings here
]

@app.route("/")
def index():
    return render_template("index.html", job_postings=job_postings)

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")
    filtered_jobs = [job for job in job_postings if keyword.lower() in job["title"].lower() or keyword.lower() in job["description"].lower()]
    return render_template("index.html", job_postings=filtered_jobs, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)
