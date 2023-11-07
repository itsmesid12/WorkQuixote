import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('job_data.db')
cursor = conn.cursor()

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Retrieve job descriptions and job IDs from the database
cursor.execute('SELECT id, jd FROM jobs')
job_data = cursor.fetchall()
job_ids = [row[0] for row in job_data]
job_descriptions = [row[1] for row in job_data]

# Fit the vectorizer on job descriptions
tfidf_matrix = vectorizer.fit_transform(job_descriptions)

# Create a list to store applied jobs
applied_jobs = []

option1 = ["Home", "Recommendations", "Applied", "About"]
option2 = ['Yes','No']
option3 = ['Yes','No']

def load_queries():
    try:
        with open("user_queries.txt", "r") as file:
            queries = file.read().splitlines()
            return queries
    except FileNotFoundError:
        return []

def write_queries(queries, file_name="user_queries.txt"):
    try:
        with open(file_name, "w") as file:
            for query in queries:
                file.write(query + '\n')
    except Exception as e:
        print(f"Error writing queries to {file_name}: {str(e)}")

def main():
    st.title("WORKQUIXOTE")

    st.sidebar.title("Sidebar")
    selected_section = st.sidebar.selectbox("WORKQUIXOTE", option1, key='selectbox1')

    if selected_section == "Home":
        display_home()
    elif selected_section == "Recommendations":
        display_recommendations()
    elif selected_section == "Applied Jobs":
        display_applied_jobs()
    elif selected_section == "About":
        display_about()

def display_home():
    st.header("Welcome to WorkQuixote")
    st.write("This is the home section. You can find job listings here.")

    query = st.text_input("Enter your job search query")

    if st.button("Search"):
        write_queries(query)
        filtered_jobs = filter_jobs(query)
        display_jobs(filtered_jobs)

def display_about():
    st.header("About")
    st.write(
        "\"WorkQuixote\" is a revolutionary job search platform designed to empower job seekers and employers alike. Named after the literary hero Don Quixote, who tilted at windmills and chased impossible dreams, our app encourages users to dream big and pursue their ideal careers with confidence."
    )

def filter_jobs(query):
    query_vector = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vector, tfidf_matrix).flatten()
    related_jobs_indices = cosine_similarities.argsort()[::-1]

    top_n = 10  # Adjust this to control the number of results
    top_job_ids = [job_ids[i] for i in related_jobs_indices[:top_n]]
    top_jobs = fetch_jobs_from_database(top_job_ids)
    return top_jobs

def display_jobs(jobs):
    st.header("Job Listings")

    if jobs:
        for i, job in enumerate(jobs):
            st.markdown(
                f'<div id="details-container-{i}" style="border: 1px solid #d1d1d1; border-radius: 15px; padding: 20px; background-color: rgba(255, 255, 255, 0.7); color: #333; margin-bottom: 20px; position: relative;">'
                f'<strong style="font-size: 24px;">{job[1]}</strong><br>'
                f'🏢{job[4]}<br>'
                f'🌍{job[5]}<br>'
                f'💼{job[6]}<br>'
                f'📄{job[7]}<br><br>'
                f'<div id="posted-days" style="position: absolute; left: 10px; bottom: 10px; font-size: 14px;">'
                f'{job[9]}'
                f'</div>'
                f'<div id="apply-link" style="position: absolute; right: 30px; bottom: 20px; font-size: 18px">'
                f'<a href={job[2]}>Apply</a>'
                f'</div>'
                '</div>',
                unsafe_allow_html=True
            )

            with st.expander(f"Job Details"):
                st.write(job[3])
            
            option = st.selectbox(f'Did you Applied?', option2, key=f'apply_{i}')
            if option == 'Yes':
                applied_jobs.append(job)

def display_applied_jobs():
    st.header("Applied Jobs")
    st.write("Here are the jobs for which you have selected 'Yes' as your application status:")

    if applied_jobs:
        for job in applied_jobs:
            # Display the details of each applied job
            st.markdown(
                f'<div id="details-container" style="border: 1px solid #d1d1d1; border-radius: 15px; padding: 20px; background-color: rgba(255, 255, 255, 0.7); color: #333; margin-bottom: 20px; position: relative;">'
                f'<strong style="font-size: 24px;">{job[1]}</strong><br>'
                f'🏢{job[4]}<br>'
                f'🌍{job[5]}<br>'
                f'💼{job[6]}<br>'
                f'📄{job[7]}<br><br>'
                f'<div id="posted-days" style="position: absolute; left: 10px; bottom: 10px; font-size: 14px;">'
                f'{job[9]}'
                f'</div>'
                '</div>',
                unsafe_allow_html=True
            )

            with st.expander("Job Details"):
                st.write(job[3])

def display_recommendations():
    st.header("Recommendations")
    st.write("Based on your previous queries, here are some job recommendations:")
    saved_queries = load_queries()

    if saved_queries:
        unique_queries = list(set(saved_queries))

        if unique_queries:
            most_recent_query = unique_queries[-1]
            filtered_jobs = filter_jobs(most_recent_query)
            display_jobs(filtered_jobs)

def fetch_jobs_from_database(indices):
    placeholders = ', '.join(['?'] * len(indices)
)
    cursor.execute(f'SELECT * FROM jobs WHERE id IN ({placeholders})', indices)
    job_data = cursor.fetchall()
    return job_data

if __name__ == '__main__':
    main()
