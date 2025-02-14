import streamlit as st
from streamlit_option_menu import option_menu

def main():
    st.set_page_config(page_title="Kids Learning Platform", layout="wide")
    
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Courses", "Leaderboards", "Project Gallery", "Admin"],
            icons=["house", "book", "trophy", "image", "gear"],
            menu_icon="cast",
            default_index=0
        )
    
    if selected == "Home":
        st.title("Welcome to the Kids Learning Platform!")
        st.write("Explore hands-on, project-based learning across various subjects.")
    
    elif selected == "Courses":
        st.title("Courses")
        difficulty_levels = ["Foundation", "Novice", "Apprentice", "Proficient", "Expert", "Mastery"]
        age_ranges = ["4-7", "8-10", "11-13", "14+"]
        
        selected_age = st.multiselect("Select Age Range:", age_ranges)
        selected_difficulty = st.multiselect("Select Difficulty Level:", difficulty_levels)
        
        st.write("Courses will be filtered based on selected criteria.")
    
    elif selected == "Leaderboards":
        st.title("Leaderboards")
        category = st.radio("Select Category:", ["Badges Earned", "Modules Completed", "Monthly Progress"])
        st.write(f"Showing leaderboard for {category}.")
        # Placeholder leaderboard data
        leaderboard_data = {"User123": 10, "User456": 8, "User789": 6}
        st.table(leaderboard_data)
    
    elif selected == "Project Gallery":
        st.title("Project Gallery")
        st.write("View final projects submitted by students. All content is manually approved by admins.")
        # Placeholder for gallery display
        st.image("https://via.placeholder.com/400", caption="Sample Project")
    
    elif selected == "Admin":
        st.title("Admin Panel")
        st.write("Only authorized admins can add, edit, or delete courses and modules.")
        # Admin features placeholder
        admin_access = st.checkbox("I am an Admin")
        if admin_access:
            st.write("Admin functions will be available here.")
    
if __name__ == "__main__":
    main()
