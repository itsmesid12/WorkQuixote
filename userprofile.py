import streamlit as st

user_data = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "location": "New York, USA",
    "bio": "Experienced software engineer looking for new opportunities.",
    "saved_jobs": ["Job 1", "Job 2", "Job 3"],
    "applied_jobs": ["Job 4", "Job 5"],
    "reviews": ["Company A", "Company B"],
}

def user_profile():
    st.title("User Profile")

    # Display user information
    st.subheader("User Information")
    st.write(f"Name: {user_data['name']}")
    st.write(f"Email: {user_data['email']}")
    st.write(f"Location: {user_data['location']}")
    st.write(f"Bio: {user_data['bio']}")

    # Display user activity history
    st.subheader("Activity History")
    st.write("Saved Jobs:")
    for job in user_data["saved_jobs"]:
        st.write(f"- {job}")

    st.write("Applied Jobs:")
    for job in user_data["applied_jobs"]:
        st.write(f"- {job}")

    st.write("Reviews:")
    for review in user_data["reviews"]:
        st.write(f"- {review}")

    # Edit profile details
    st.subheader("Edit Profile Details")
    new_name = st.text_input("Name", user_data["name"])
    new_email = st.text_input("Email", user_data["email"])
    new_location = st.text_input("Location", user_data["location"])
    new_bio = st.text_area("Bio", user_data["bio"])

    if st.button("Update Profile"):
        user_data["name"] = new_name
        user_data["email"] = new_email
        user_data["location"] = new_location
        user_data["bio"] = new_bio

        st.success("Profile updated successfully!")

if __name__ == "__main__":
    user_profile()