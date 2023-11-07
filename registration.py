import streamlit as st

# User database (replace with a real database in a production environment)
user_database = {}

# Define Streamlit app layout for the combined registration and login form
def registration_and_login():
    st.title("Registration and Login")

    st.write("Select Action: ")
    user_action = st.radio("Login", ["Register", "Login"])

    # Registration Section
    if user_action == "Register":
        st.subheader("User Registration")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Register"):
            if new_username and new_password:
                # Check if the username is already taken
                if new_username in user_database:
                    st.warning("Username already exists. Please choose a different username.")
                else:
                    # Store user registration data (insecure, use a real database for production)
                    user_database[new_username] = new_password
                    st.success("Registration successful. You can now log in.")

    # Login Section
    if user_action == "Login":
        st.subheader("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in user_database:
                if user_database[username] == password:
                    st.success(f"Welcome, {username}! You are now logged in.")
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.warning("Username not found. Please register or check your username.")

if __name__ == "__main__":
    registration_and_login()
