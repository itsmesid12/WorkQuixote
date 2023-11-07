import streamlit as st

# Sample job data (replace with real data from your job portal)
job_data = {
    "title": "Software Engineer",
    "company": "TechCorp",
    "location": "New York, USA",
    "description": "We are looking for a talented software engineer...",
    "application_link": "https://example.com/apply",
}

# Define Streamlit app layout for the job details page
def job_details():
    st.title("Job Details")

    # Display job information
    st.header(job_data["title"])
    st.write(f"Company: {job_data['company']}")
    st.write(f"Location: {job_data['location']}")
    st.write(f"Description: {job_data['description']}")

    # Application link
    st.subheader("Apply for this Job")
    st.write(f"Click the link below to apply for this job:")
    st.markdown(f"[Apply Here]({job_data['application_link']})")

    # User interaction options
    st.subheader("User Interaction")
    
    # Apply for the job
    if st.button("Apply for this Job"):
        st.success("You have successfully applied for this job!")

    # Save the job
    if st.button("Save this Job"):
        st.success("This job has been saved to your profile.")

    # Write a review/rating
    review_text = st.text_area("Write a Review/Rating (optional)", "")
    rating = st.selectbox("Rating (1-5)", list(range(1, 6)))
    if st.button("Submit Review/Rating"):
        if review_text:
            st.success("Your review has been submitted.")
        else:
            st.warning("Please write a review text if you want to submit a review.")

if __name__ == "__main__":
    job_details()
