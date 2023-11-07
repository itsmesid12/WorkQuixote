import streamlit as st

# Sample user data (replace with a real database in a production environment)
user_database = {
    "admin": "admin_12",
    "user1": "password1",
    "user2": "password2",
}

# Define Streamlit app layout for the admin panel
def admin_panel():
    st.title("Admin Panel")

    # Admin Login
    st.subheader("Admin Login")
    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")

    if st.button("Admin Login"):
        if admin_username in user_database and user_database[admin_username] == admin_password:
            st.success("Admin logged in successfully.")
            admin_functions()

    # Admin Functions (Protected)
    def admin_functions():
        st.subheader("User Accounts Management")

        # List User Accounts
        st.write("List of User Accounts:")
        for username in user_database.keys():
            st.write(username)

        # Delete User Account
        account_to_delete = st.text_input("Enter username to delete:")
        if st.button("Delete User Account"):
            if account_to_delete in user_database:
                del user_database[account_to_delete]
                st.success(f"User account '{account_to_delete}' deleted successfully.")
            else:
                st.warning("User account not found.")

if __name__ == "__main__":
    admin_panel()
