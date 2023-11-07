import streamlit as st

# Sample company data (replace with real data from your job portal)
company_data = {
    "name": "TechCorp",
    "description": "A leading technology company",
}

# Sample review data (replace with real reviews from your job portal)
reviews_data = [
    {"user": "User1", "rating": 4, "review": "Great company to work for!"},
    {"user": "User2", "rating": 5, "review": "Excellent work environment."},
]

# Define Streamlit app layout for the company reviews page
def company_reviews():
    st.title("Company Reviews")

    # Display company information
    st.header(company_data["name"])
    st.write(f"Description: {company_data['description']}")

    # Display existing reviews
    st.subheader("Existing Reviews")
    if reviews_data:
        for review in reviews_data:
            st.write(f"User: {review['user']}")
            st.write(f"Rating: {review['rating']}")
            st.write(f"Review: {review['review']}")
            st.write("---")

    else:
        st.info("No reviews available for this company.")

    # User interaction options
    st.subheader("User Interaction")

    # Write a new review
    new_review = st.text_area("Write a New Review")
    new_rating = st.selectbox("Rating (1-5)", list(range(1, 6)))

    if st.button("Submit Review"):
        if new_review and new_rating:
            reviews_data.append({"user": "YourUsername", "rating": new_rating, "review": new_review})
            st.success("Your review has been submitted.")
        else:
            st.warning("Please provide both a review and a rating to submit your review.")

if __name__ == "__main__":
    company_reviews()
