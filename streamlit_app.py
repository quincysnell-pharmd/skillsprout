import streamlit as st
import uuid

# -----------------------------
# Sample data for demonstration
# In a production app, these would be stored in a database
# -----------------------------

# Classes data
CLASSES_DATA = [
    {
        "id": 1,
        "title": "Gardening 101",
        "description": "Learn basic gardening techniques, how plants grow, and how to maintain a healthy garden.",
        "modules": [
            {"module_id": 11, "module_title": "Seed Planting Basics"},
            {"module_id": 12, "module_title": "Watering Schedules"},
            {"module_id": 13, "module_title": "Soil Quality & Fertilizers"},
        ]
    },
    {
        "id": 2,
        "title": "Cooking for Beginners",
        "description": "Explore simple recipes, kitchen safety, and the basics of healthy meals.",
        "modules": [
            {"module_id": 21, "module_title": "Kitchen Safety 101"},
            {"module_id": 22, "module_title": "Easy Breakfast Recipes"},
            {"module_id": 23, "module_title": "Healthy Lunch Ideas"},
        ]
    },
    {
        "id": 3,
        "title": "Young Entrepreneurship",
        "description": "Learn how to develop a business idea, pitch it, and manage your mini-enterprise.",
        "modules": [
            {"module_id": 31, "module_title": "Finding a Business Idea"},
            {"module_id": 32, "module_title": "Pitch Practice"},
            {"module_id": 33, "module_title": "Basic Money Management"},
        ]
    },
    {
        "id": 4,
        "title": "Introduction to Coding",
        "description": "Understand coding fundamentals, logical thinking, and build small projects.",
        "modules": [
            {"module_id": 41, "module_title": "What is Coding?"},
            {"module_id": 42, "module_title": "Basic Python Syntax"},
            {"module_id": 43, "module_title": "Mini Project: Calculator"},
        ]
    },
]

# Badges data
BADGES_DATA = [
    {
        "badge_id": 101,
        "title": "Green Thumb",
        "description": "Awarded for completing the Gardening 101 course."
    },
    {
        "badge_id": 102,
        "title": "Junior Chef",
        "description": "Awarded for completing the Cooking for Beginners course."
    },
    {
        "badge_id": 103,
        "title": "Kid Boss",
        "description": "Awarded for completing the Young Entrepreneurship course."
    },
    {
        "badge_id": 104,
        "title": "Code Explorer",
        "description": "Awarded for completing the Introduction to Coding course."
    },
]

# In-memory "database" for user data
if "users" not in st.session_state:
    st.session_state["users"] = {}  # Key: username, Value: user_info dict

# In-memory "database" for friendships
if "friendships" not in st.session_state:
    st.session_state["friendships"] = {}  # Key: username, Value: set of friend_usernames

# -----------------------------
# Utility Functions
# -----------------------------
def register_user(username, password, full_name):
    """
    Registers a new user in the session state if the username is not taken.
    Returns True if successful, False if username already exists.
    """
    if username in st.session_state["users"]:
        return False
    
    st.session_state["users"][username] = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "password": password,
        "full_name": full_name,
        "bio": "Hey there! I’m excited to learn new skills on SkillSprout!",
        "completed_modules": set(),  # (class_id, module_id)
        "earned_badges": set(),      # badge_id
    }
    st.session_state["friendships"][username] = set()  # Initialize empty friend list
    return True

def login_user(username, password):
    """
    Verifies user credentials.
    Returns True if login successful, else False.
    """
    user_data = st.session_state["users"].get(username)
    if user_data and user_data["password"] == password:
        return True
    return False

def add_friend(user, friend_username):
    """
    Adds a friend if they exist and are not already a friend.
    """
    if friend_username in st.session_state["users"] and friend_username != user:
        st.session_state["friendships"][user].add(friend_username)
        st.session_state["friendships"][friend_username].add(user)

def complete_module(username, class_id, module_id):
    """
    Marks a module as completed for the user.
    """
    user_data = st.session_state["users"].get(username)
    if user_data:
        user_data["completed_modules"].add((class_id, module_id))

def award_badge_if_eligible(username, class_id):
    """
    Checks if the user has completed all modules in a class.
    If yes, awards the corresponding badge.
    """
    user_data = st.session_state["users"].get(username)
    if not user_data:
        return

    # Find the class
    class_info = next((c for c in CLASSES_DATA if c["id"] == class_id), None)
    if not class_info:
        return

    # Check if all modules are completed
    class_module_ids = {m["module_id"] for m in class_info["modules"]}
    completed_in_this_class = {
        pair for pair in user_data["completed_modules"] if pair[0] == class_id
    }
    completed_module_ids = {m_id for (_, m_id) in completed_in_this_class}

    # If all modules in the class have been completed, award badge
    if class_module_ids == completed_module_ids:
        # Find the badge for this class
        # This is a simple mapping: index in CLASSES_DATA -> index in BADGES_DATA
        # You can customize or extend this as needed
        badge = None
        if class_id == 1:
            badge = 101
        elif class_id == 2:
            badge = 102
        elif class_id == 3:
            badge = 103
        elif class_id == 4:
            badge = 104

        if badge and badge not in user_data["earned_badges"]:
            user_data["earned_badges"].add(badge)
            st.success(f"You earned a new badge: {get_badge_title(badge)}!")

def get_badge_title(badge_id):
    """
    Return the badge title by badge_id
    """
    badge_info = next((b for b in BADGES_DATA if b["badge_id"] == badge_id), None)
    return badge_info["title"] if badge_info else "Unknown Badge"

def get_class_title(class_id):
    """
    Return the class title by class_id
    """
    class_info = next((c for c in CLASSES_DATA if c["id"] == class_id), None)
    return class_info["title"] if class_info else "Unknown Class"

# -----------------------------
# Main App
# -----------------------------

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

def show_login_page():
    st.title("SkillSprout - Login / Register")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_username = st.text_input("Username (Login)", key="login_username")
        login_password = st.text_input("Password (Login)", type="password", key="login_password")
        if st.button("Login"):
            if login_user(login_username, login_password):
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = login_username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")

    with tab_register:
        st.subheader("Register")
        register_username = st.text_input("Choose a Username", key="register_username")
        register_password = st.text_input("Choose a Password", type="password", key="register_password")
        register_full_name = st.text_input("Your Full Name", key="register_full_name")

        if st.button("Register"):
            if not register_username or not register_password or not register_full_name:
                st.warning("Please fill all fields to register.")
            else:
                if register_user(register_username, register_password, register_full_name):
                    st.success("Registration successful! Please login now.")
                else:
                    st.error("Username already exists. Please choose another username.")


def show_home_page():
    st.title("SkillSprout - Home")
    st.write("Welcome to SkillSprout! A place where you can grow your skills, earn badges, and connect with friends.")
    st.write("Use the sidebar to navigate to different sections of the app.")

def show_profile_page():
    st.title("My Profile")
    current_user_data = st.session_state["users"][st.session_state["current_user"]]
    
    st.write(f"**Username:** {current_user_data['username']}")
    st.write(f"**Full Name:** {current_user_data['full_name']}")

    # Edit bio
    st.subheader("Bio")
    updated_bio = st.text_area("Update your bio", value=current_user_data["bio"])
    if st.button("Save Bio"):
        current_user_data["bio"] = updated_bio
        st.success("Bio updated!")

    # Display earned badges
    st.subheader("My Badges")
    if current_user_data["earned_badges"]:
        for badge_id in current_user_data["earned_badges"]:
            badge_title = get_badge_title(badge_id)
            st.markdown(f"- **{badge_title}**")
    else:
        st.write("No badges yet. Keep learning!")

    # Display progress / completed modules
    st.subheader("Completed Modules")
    if current_user_data["completed_modules"]:
        for (class_id, module_id) in current_user_data["completed_modules"]:
            st.markdown(f"- {get_class_title(class_id)} | Module ID: {module_id}")
    else:
        st.write("No modules completed yet. Start learning from the Classes page!")

def show_classes_page():
    st.title("Available Classes")
    st.write("Pick a class to see its modules and mark them complete to earn badges.")

    for class_info in CLASSES_DATA:
        with st.expander(class_info["title"]):
            st.write(class_info["description"])
            st.write("**Modules:**")
            for mod in class_info["modules"]:
                mod_title = mod["module_title"]
                mod_id = mod["module_id"]

                # Check if the module is already completed
                current_user_data = st.session_state["users"][st.session_state["current_user"]]
                is_completed = (class_info["id"], mod_id) in current_user_data["completed_modules"]

                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"- {mod_title} (Module ID: {mod_id})")
                with col2:
                    if not is_completed:
                        if st.button(f"Complete {mod_id}", key=f"{class_info['id']}-{mod_id}"):
                            complete_module(st.session_state["current_user"], class_info["id"], mod_id)
                            st.success(f"Module '{mod_title}' marked as complete.")
                            award_badge_if_eligible(st.session_state["current_user"], class_info["id"])
                    else:
                        st.write(":white_check_mark: Completed")

def show_friend_circle_page():
    st.title("Friendship Circle")
    st.write("Connect with other learners!")

    all_usernames = list(st.session_state["users"].keys())
    current_user = st.session_state["current_user"]

    # Current friends list
    st.subheader("My Friends")
    friend_list = st.session_state["friendships"][current_user]
    if friend_list:
        for friend in friend_list:
            friend_data = st.session_state["users"][friend]
            st.write(f"- {friend_data['full_name']} (@{friend_data['username']})")
    else:
        st.write("No friends yet!")

    # Add a new friend
    st.subheader("Add a Friend")
    possible_friends = [u for u in all_usernames if u != current_user and u not in friend_list]
    friend_to_add = st.selectbox("Select a user to add", options=["Select..."] + possible_friends)
    if st.button("Add Friend"):
        if friend_to_add != "Select...":
            add_friend(current_user, friend_to_add)
            st.success(f"You are now friends with {friend_to_add}!")
        else:
            st.warning("Please select a valid friend.")

def main():
    if not st.session_state["logged_in"]:
        show_login_page()
    else:
        # Sidebar navigation
        menu = ["Home", "My Profile", "Classes", "Friendship Circle", "Logout"]
        choice = st.sidebar.selectbox("Navigate", menu)

        if choice == "Home":
            show_home_page()
        elif choice == "My Profile":
            show_profile_page()
        elif choice == "Classes":
            show_classes_page()
        elif choice == "Friendship Circle":
            show_friend_circle_page()
        elif choice == "Logout":
            st.session_state["logged_in"] = False
            st.session_state["current_user"] = None
            st.experimental_rerun()

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
