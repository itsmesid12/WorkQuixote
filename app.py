import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sqlite3
from streamlit import session_state as state


conn = sqlite3.connect('job_data.db')
cursor = conn.cursor()


vectorizer = TfidfVectorizer()
job_index = 0
if 'job_index' not in state:
    state.job_index = 0

jobs_per_page = 10

st.set_page_config(
        page_title="WORKQUIXOTE",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded"
)


cursor.execute('SELECT id, jd FROM jobs')
job_data = cursor.fetchall()
job_ids = [row[0] for row in job_data]
job_descriptions = [row[1] for row in job_data]


tfidf_matrix = vectorizer.fit_transform(job_descriptions)


option1 = ["Home", "Recommendations", "About"]
option2 = ['','Yes','No']
option3 = ['','Yes','No']

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
    selected_section = st.sidebar.selectbox("WORKQUIXOTE", option1)

    if selected_section == "Home":
        display_home()
    elif selected_section == "Recommendations":
        display_recommendations()
    elif selected_section == "About":
        display_about()

def display_home():
    st.header("Welcome to WorkQuixote")
    st.write("This is the home section. You can find job listings here.")

    if 'page' not in state:
        state.page = 0

    query = st.text_input("Enter your job search query")

    if st.button("Search"):
        if not query.isalpha():
            st.error("Please enter a query with alphabetic characters only.")
        else:
            write_queries(query)
            filtered_jobs = filter_jobs(query)
            num_pages = len(filtered_jobs) // 10
            start_page = state.page * 10
            end_page = (state.page + 1) * 10

            display_jobs(filtered_jobs[start_page:end_page])

            col1, col2 = st.columns(2)

            if col1.button('Previous'):
                if state.page > 0:
                    state.page -= 1

            if col2.button("Next"):
                if state.page < num_pages - 1:
                    state.page += 1

def display_about():
    st.write(
        """
        # **WORKQUIXOTE: Redefining Your Job Search**

        ## **Introduction**

        **WORKQUIXOTE** is a revolutionary job search platform designed to empower job seekers and employers alike. Named after the literary hero Don Quixote, who tilted at windmills and chased impossible dreams, our app encourages users to dream big and pursue their ideal careers with confidence.

        ## **Features**

        ### **1. Tailored Job Recommendations**

        WORKQUIXOTE uses advanced algorithms to provide personalized job recommendations based on your skills, interests, and preferences. Our platform employs cutting-edge technologies like natural language processing to match your qualifications with job listings from various sources, ensuring that you discover the most relevant opportunities.

        ### **2. User-Friendly Interface**

        Our user-friendly interface makes the job search process a breeze. With intuitive navigation, clear instructions, and customizable search filters, finding your dream job has never been easier. Whether you're a tech guru or a non-tech professional, WORKQUIXOTE is designed to be inclusive and accessible to all.

        ### **3. Applied Jobs Tracking**

        Keep track of your job applications seamlessly. WORKQUIXOTE allows you to mark which jobs you've applied for, making it easier to manage your application status and stay organized throughout your job hunt.

        ### **6. Real-Time Job Alerts**

        Stay up to date with the latest job openings in your preferred industry. WORKQUIXOTE sends real-time job alerts to your inbox, ensuring you don't miss out on any opportunities.
     
    """ )

def filter_jobs(query):
    query_vector = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vector, tfidf_matrix).flatten()
    related_jobs_indices = cosine_similarities.argsort()[::-1]

    top_n = 45  # Adjust this to control the number of results
    top_job_ids = [job_ids[i] for i in related_jobs_indices[:top_n]]
    top_jobs = fetch_jobs_from_database(top_job_ids)
    return top_jobs

def display_jobs(jobs):
    st.header("Job Listings")
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
        with st.expander('View Details'):
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

def display_applied_job():
    st.header("Applied Jobs")
    st.write("Saved Jobs")

def fetch_jobs_from_database(indices):
    placeholders = ', '.join(['?'] * len(indices)
)
    cursor.execute(f'SELECT * FROM jobs WHERE id IN ({placeholders})', indices)
    job_data = cursor.fetchall()
    return job_data

if __name__ == '__main__':
    main()
