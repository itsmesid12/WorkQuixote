import streamlit as st
from streamlit import session_state as state
import time

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://img.freepik.com/free-vector/seamless-gold-rhombus-grid-pattern-black-background_53876-97589.jpg?size=626&ext=jpg&ga=GA1.1.34264412.1698796800&semt=ais");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Create a session state to store the current page index
if 'page' not in state:
    state.page = 0

# Define the content with 50 lines of text
text_lines = [
    f"Line {i+1}" for i in range(50)
]

num_pages = len(text_lines) // 10
# Create a Streamlit app

st.title("Multi-Page Streamlit App")

# Display the current page title
st.header(f"Page {state.page + 1}")

# Display 10 lines of content for the current page
start_line = state.page * 10
end_line = (state.page + 1) * 10
for line in text_lines[start_line:end_line]:
    st.write(line)

# Create navigation buttons and page number input
col1, col2, col3 = st.columns([1, 4, 1])

if col1.button("Previous Page"):
    if state.page > 0:
        state.page -= 1

page_number = col2.number_input("Go to Page", min_value=1, max_value=num_pages, value=state.page + 1)

# Use an empty element to delay the update for the page number input
empty_placeholder = col2.empty()
if page_number != state.page + 1:
    empty_placeholder.text("Updating...")
    time.sleep(0.2)  # Add a short delay
    state.page = page_number - 1
    empty_placeholder.empty()

if col3.button("Next Page"):
    if state.page < num_pages - 1:
        state.page += 1
