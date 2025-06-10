import streamlit as st
import google.generativeai as genai
import uuid

# Configure Google API key directly
GOOGLE_API_KEY = "AIzaSyBq0alsqYVLK_ztxzKd_c4BAnX5NDEieR8"
if not GOOGLE_API_KEY:
    st.error("Google API key is not set.")
    st.stop()
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page configuration
st.set_page_config(page_title="🌟 My Goal Journey", page_icon="⭐", layout="centered")

# Initialize session state for goals and progress
if "goals" not in st.session_state:
    st.session_state.goals = {}  # Dictionary to store goals: {id: {"name": str, "category": str, "progress": int}}
if "selected_goal_id" not in st.session_state:
    st.session_state.selected_goal_id = None

# Function to generate daily tip using Gemini API
def get_daily_tip(goal_name, category):
    try:
        prompt = f"Give a short, actionable tip (1 sentence) for achieving a {category} goal: '{goal_name}'."
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No tip generated. Try again!"
    except Exception as e:
        return f"Error generating tip: {str(e)}"

# Function to generate motivational quote using Gemini API
def get_motivational_quote(goal_name, category):
    try:
        prompt = f"Create an inspiring one-sentence quote for a {category} goal: '{goal_name}', with positive emojis."
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "No quote generated. Try again!"
    except Exception as e:
        return f"Error generating quote: {str(e)}"

# Sidebar for goal management
with st.sidebar:
    st.header("🌟 My Goals")
    
    # Add new goal
    st.subheader("Add a New Goal")
    goal_name = st.text_input("Goal Name", placeholder="e.g., Run a marathon")
    goal_category = st.selectbox("Category", ["Health", "Work", "Education", "Finance", "Hobbies"])
    if st.button("Add Goal"):
        if goal_name:
            goal_id = str(uuid.uuid4())
            st.session_state.goals[goal_id] = {
                "name": goal_name,
                "category": goal_category,
                "progress": 0
            }
            st.success(f"Goal '{goal_name}' added!")
        else:
            st.error("Please enter a goal name.")

    # Display and select existing goals
    st.subheader("Your Goals")
    if st.session_state.goals:
        goal_options = {f"{goal['name']} ({goal['category']})": goal_id for goal_id, goal in st.session_state.goals.items()}
        selected_goal = st.selectbox("Select a Goal", options=list(goal_options.keys()))
        st.session_state.selected_goal_id = goal_options.get(selected_goal)
        
        # Delete selected goal
        if st.button("Delete Selected Goal"):
            if st.session_state.selected_goal_id in st.session_state.goals:
                goal_name = st.session_state.goals[st.session_state.selected_goal_id]["name"]
                del st.session_state.goals[st.session_state.selected_goal_id]
                st.session_state.selected_goal_id = None
                st.success(f"Goal '{goal_name}' deleted!")
    else:
        st.info("No goals added yet.")

# Main content area
st.title("🌟 My Goal Journey")
st.markdown("Stay on track with your goals and get inspired daily! 💪")

if st.session_state.selected_goal_id and st.session_state.selected_goal_id in st.session_state.goals:
    goal = st.session_state.goals[st.session_state.selected_goal_id]
    st.subheader(f"Goal: {goal['name']} ({goal['category']})")

    # Progress tracking
    st.subheader("Track Progress")
    progress = st.slider("Progress (%)", 0, 100, goal["progress"])
    if progress != goal["progress"]:
        st.session_state.goals[st.session_state.selected_goal_id]["progress"] = progress
        st.success(f"Progress updated to {progress}%!")
    st.progress(progress / 100.0)

    # Daily tip
    st.subheader("Daily Tip")
    if st.button("Get Daily Tip"):
        tip = get_daily_tip(goal["name"], goal["category"])
        st.write(tip)

    # Motivational quote
    st.subheader("Motivational Quote")
    if st.button("Get Motivational Quote"):
        quote = get_motivational_quote(goal["name"], goal["category"])
        st.markdown(f"**{quote}**")
else:
    st.info("Select or add a goal from the sidebar to get started.")

# Instructions
st.markdown("---")
st.markdown("""
### How to Get Started
1. **Create a Goal**: Add a new goal in the sidebar with a name and category.
2. **Choose a Goal**: Select a goal to view its progress and details.
3. **Update Progress**: Use the slider to track your progress.
4. **Stay Inspired**: Generate tips and quotes to keep motivated.
5. **Manage Goals**: Delete goals you no longer need.
""")

# Custom styling
st.markdown("""
<style>
.stApp { background-color: #f0f8ff; }
h1 { color: #2e7d32; }
</style>
""", unsafe_allow_html=True)