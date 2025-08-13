# 🚀 Complete Professional Quality Thought AI Mentor
# 🔐 Login & Register System Integration
import hashlib
import json

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    return users.get(username) == hash_password(password)

import os
import subprocess
import streamlit as st
openrouter_api_key = st.secrets["openrouter_api_key"]
from langchain_openai import ChatOpenAI  # ✅ Correct for new version
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from datetime import datetime

# ✅ Professional Page Configuration — MUST be first
st.set_page_config(
    page_title="AI-Powered Learning Mentor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Login Check (before app content)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    selected_theme = "Corporate Blue"
    theme = {
        "primary": "#1e3a8a", "secondary": "#dbeafe", "accent": "#3b82f6",
        "gradient": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
    }

    st.markdown(f"""
        <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, {theme['secondary']} 100%);
        }}
        .login-box {{
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 6px solid {theme['accent']};
            margin: 5% auto;
            max-width: 600px;
        }}
        .login-box h1 {{
            text-align: center;
            color: {theme['primary']};
        }}
        .stButton>button {{
            background: {theme['gradient']};
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            margin-top: 10px;
        }}
        .stButton>button:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='login-box'>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🧠 AI Mentor Login</h1>", unsafe_allow_html=True)
    menu = ["Login", "Register"]
    choice = st.selectbox("Select Action", menu)

    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.success(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Incorrect username or password")

    elif choice == "Register":
        st.subheader("Create New Account")
        new_user = st.text_input("Username", key="new_user")
        new_pass = st.text_input("Password", type="password", key="new_pass")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created successfully! Please login.")
            else:
                st.warning("Username already exists.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ✅ Logged in user display
st.sidebar.markdown(f"👋 Welcome, **{st.session_state.get('username', 'User')}**")
if st.sidebar.button("🔓 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ✅ Load API Key (Streamlit Cloud Compatible)
try:
    openrouter_api_key = st.secrets["openrouter_api_key"]
except:
    try:
        openrouter_api_key = os.getenv("openrouter_api_key")
    except:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            openrouter_api_key = os.getenv("openrouter_api_key")
        except:
            openrouter_api_key = None

# ✅ Initialize Model (will work when API key is added)
if openrouter_api_key:
   model = ChatOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    api_key= openrouter_api_key,  # OpenRouter API key
    base_url="https://openrouter.ai/api/v1",
    temperature=0.5,
    max_tokens=500
)

else:
    model = None

# 🔽 (Everything else in your original file continues from here... unchanged)
# 🔽 (Everything else in your original file continues from here... unchanged)
# ✅ Professional Theme System
with st.sidebar:
    st.markdown("### 🎨 Professional Themes")
    selected_theme = st.selectbox(
        "Choose Theme:",
        ["Corporate Blue", "Dark Professional", "Emerald Green", "Royal Purple", "Sunset Orange"],
        index=0
    )

# ✅ Theme Configurations
themes = {
    "Corporate Blue": {
        "primary": "#1e3a8a", "secondary": "#dbeafe", "accent": "#3b82f6",
        "gradient": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
    },
    "Dark Professional": {
        "primary": "#111827", "secondary": "#374151", "accent": "#6366f1",
        "gradient": "linear-gradient(135deg, #111827 0%, #374151 100%)"
    },
    "Emerald Green": {
        "primary": "#065f46", "secondary": "#d1fae5", "accent": "#10b981",
        "gradient": "linear-gradient(135deg, #065f46 0%, #10b981 100%)"
    },
    "Royal Purple": {
        "primary": "#581c87", "secondary": "#ede9fe", "accent": "#8b5cf6",
        "gradient": "linear-gradient(135deg, #581c87 0%, #8b5cf6 100%)"
    },
    "Sunset Orange": {
        "primary": "#c2410c", "secondary": "#fed7aa", "accent": "#f97316",
        "gradient": "linear-gradient(135deg, #c2410c 0%, #f97316 100%)"
    }
}
theme = themes[selected_theme]

# ✅ Professional CSS Styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {{
        background: linear-gradient(135deg, #ffffff 0%, {theme['secondary']} 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    .hero-header {{
        background: {theme['gradient']};
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: slideInDown 0.8s ease-out;
    }}
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .stButton>button {{
        background: {theme['gradient']};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        width: 100%;
        margin: 0.2rem 0;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }}
    
    .mentor-section {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid {theme['accent']};
    }}
    
    .response-box {{
        background: linear-gradient(135deg, {theme['secondary']} 0%, white 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid {theme['accent']};
        margin: 1.5rem 0;
        animation: fadeInUp 0.6s ease-out;
    }}
    
    .user-input-box {{
        background: linear-gradient(135deg, #f8fafc 0%, {theme['secondary']} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid {theme['primary']};
        margin: 1rem 0;
    }}
    
    .tool-section {{
        background: linear-gradient(135deg, white 0%, {theme['secondary']} 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid {theme['accent']};
    }}
    
    .stats-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-top: 4px solid {theme['accent']};
        margin: 1rem 0;
    }}
    
    @keyframes slideInDown {{
        from {{ transform: translateY(-100px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{ transform: translateY(30px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    .stTextArea>div>div>textarea {{
        border-radius: 10px;
        border: 2px solid {theme['secondary']};
        font-family: 'Courier New', monospace;
    }}
    
    .stSelectbox>div>div>div {{
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# ✅ Hero Section
st.markdown(f"""
    <div class='hero-header' style='padding-top: 2rem; padding-bottom: 2rem;'>
        <div class='hero-title' style='font-size: 3.5rem; font-weight: 900;'>
            🧠 AI-Powered Learning Mentor
        </div>
        <p style='font-size: 1.18rem; font-weight: 400; opacity: 0.97; margin: 0.7rem 0 0 0;'>
            Your personalized platform for Programming, Data Science & Cloud Mastery.
        </p>
        <p style='font-size: 1.12rem; font-weight: 400; opacity: 0.96; margin: 0.35rem 0 0 0;'>
            Practise real code, get instant AI feedback, and unlock your career potential — all in one place.
        </p>
    </div>
""", unsafe_allow_html=True)

# ✅ Organized Module System
programming_languages = [
    ("Python", "🐍"), ("Java", "☕"), ("C++", "💻"), ("JavaScript", "🔨"),
    ("TypeScript", "🟪"), ("Rust", "🦀"), ("Go", "🐹"), ("Kotlin", "🟩"),
    ("R Programming", "📊"), ("C#", "🔷"), ("PHP", "🐘"), ("Swift", "🍎"),
    ("Ruby", "💎"), ("Scala", "⚖️"), ("Dart", "🎯")
]

web_development = [
    ("HTML/CSS", "🌐"), ("React", "⚛️"), ("Angular", "🅰️"), ("Vue.js", "💚"),
    ("Node.js", "🟢"), ("Express.js", "🚀"), ("Django", "🎸"), ("Flask", "🌶️")
]

data_science = [
    ("Numpy", "📐"), ("Pandas", "📊"), ("Scikit-learn", "🔬"), ("TensorFlow", "🧠"),
    ("PyTorch", "🔥"), ("Statistics", "📈"), ("Machine Learning", "🤖"),
    ("Deep Learning", "🧠"), ("Data Analysis", "📊"), ("Matplotlib", "📈")
]

database_tools = [
    ("SQL", "📓"), ("MongoDB", "🍃"), ("PostgreSQL", "🐘"), ("MySQL", "🐬"),
    ("Redis", "🔴"), ("Elasticsearch", "🔍")
]

cloud_devops = [
    ("AWS", "☁️"), ("Azure", "🔷"), ("GCP", "☁️"), ("Docker", "🐳"),
    ("Kubernetes", "⚙️"), ("Terraform", "🌍"), ("Jenkins", "🔧"), ("DevOps", "⚙️")
]

computer_science = [
    ("Data Structures", "📒"), ("Algorithms", "🔍"), ("System Design", "🏗️"),
    ("Operating Systems", "�"), ("Computer Networks", "🌐"), ("Cybersecurity", "🔒")
]

tools_platforms = [
    ("Git & GitHub", "🔧"), ("Linux", "🐧"), ("VS Code", "📝"), ("Jupyter", "�"),
    ("Postman", "📮"), ("Figma", "🎨")
]

testing_qa = [
    ("Unit Testing", "🧪"), ("Selenium", "🕷️"), ("Jest", "�"), ("Pytest", "🐍"),
    ("API Testing", "🔗"), ("Performance Testing", "⚡")
]

career_interview = [
    ("HR Questions", "🧾"), ("Resume Tips", "📄"), ("Behavioral Rounds", "🧠"),
    ("Interview Prep", "🎯"), ("Coding Interviews", "💻"), ("System Design Interviews", "🏗️")
]

# Combine all modules for total count
all_modules = (programming_languages + web_development + data_science +
               database_tools + cloud_devops + computer_science +
               tools_platforms + testing_qa + career_interview)

# ✅ Enhanced Session State with Progress Tracking
if 'mentor_type' not in st.session_state:
    st.session_state.mentor_type = None
    st.session_state.code_input = ""
    st.session_state.user_progress = {}
    st.session_state.chat_history = []
    st.session_state.bookmarks = []
    st.session_state.user_notes = {}
    st.session_state.session_start = datetime.now()
    st.session_state.total_queries = 0

# ✅ Enhanced Sidebar with Organized Categories
st.sidebar.title("📚 Learning Modules")

# ✅ Enhanced Stats Dashboard
if st.session_state.mentor_type:
    # Track progress
    if st.session_state.mentor_type not in st.session_state.user_progress:
        st.session_state.user_progress[st.session_state.mentor_type] = {
            'started': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'queries': 0,
            'completed_topics': []
        }

    progress = st.session_state.user_progress[st.session_state.mentor_type]
    session_time = datetime.now() - st.session_state.session_start

    st.sidebar.markdown("### 📊 Session Dashboard")
    st.sidebar.metric("🎯 Active Module", st.session_state.mentor_type)
    st.sidebar.metric("⏱️ Session Time", str(session_time).split('.')[0])
    st.sidebar.metric("💬 Total Queries", st.session_state.total_queries)
    st.sidebar.metric("📚 Modules Explored", len(st.session_state.user_progress))

st.sidebar.markdown("---")

# Organized module categories
categories = [
    ("💻 Programming Languages", programming_languages),
    ("🌐 Web Development", web_development),
    ("📊 Data Science & AI", data_science),
    ("🗄️ Database & Storage", database_tools),
    ("☁️ Cloud & DevOps", cloud_devops),
    ("🔬 Computer Science", computer_science),
    ("🛠️ Tools & Platforms", tools_platforms),
    ("🧪 Testing & QA", testing_qa),
    ("🎯 Career & Interview", career_interview)
]

# Display categories with expandable sections
for category_name, category_modules in categories:
    with st.sidebar.expander(category_name):
        for module, emoji in category_modules:
            if st.button(f"{emoji} {module}", key=f"btn_{module}"):
                st.session_state.mentor_type = module
                st.session_state.code_input = ""
                st.rerun()

# ✅ Additional Sidebar Features
st.sidebar.markdown("---")

# Quick Actions
st.sidebar.markdown("### ⚡ Quick Actions")
if st.sidebar.button("📋 View All Progress"):
    st.session_state.show_progress = True

if st.sidebar.button("📖 Learning Roadmap"):
    st.session_state.show_roadmap = True

if st.sidebar.button("🔖 My Bookmarks"):
    st.session_state.show_bookmarks = True

if st.sidebar.button("📝 My Notes"):
    st.session_state.show_notes = True

# Export Options
st.sidebar.markdown("### 📤 Export Options")
if st.sidebar.button("📄 Export Progress Report"):
    # Generate progress report
    report = f"""
# Quality Thought AI Mentor - Progress Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Session Summary
- Total Queries: {st.session_state.total_queries}
- Modules Explored: {len(st.session_state.user_progress)}
- Session Duration: {datetime.now() - st.session_state.session_start}

## Module Progress
"""
    for module, data in st.session_state.user_progress.items():
        report += f"- {module}: Started {data['started']}, {data['queries']} queries\n"

    st.sidebar.download_button(
        "💾 Download Report",
        report,
        file_name=f"learning_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# ✅ Main Interaction Area (Your original functionality enhanced)
if st.session_state.mentor_type:
    st.markdown(f"""
        <div class='mentor-section'>
            <h2>{st.session_state.mentor_type} Mentor 🧠</h2>
            <p>Professional AI guidance for mastering {st.session_state.mentor_type}</p>
        </div>
    """, unsafe_allow_html=True)

    # Experience and Language (Your original)
    col1, col2 = st.columns(2)
    with col1:
        experience = st.slider("Your experience (in years):", 0, 10, 1)
    with col2:
        lang = st.selectbox("Select Interface Language", 
                           ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], 
                           index=0)

    # Default Templates (Your original)
    default_templates = {
        "Python": "print('Hello, World!')",
        "Java": "public class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }",
        "C++": "#include<iostream>\nusing namespace std;\nint main() { cout << \"Hello World\"; return 0; }",
        "SQL": "SELECT * FROM your_table;",
        "JavaScript": "console.log('Hello, World!');"
    }

    template = default_templates.get(st.session_state.mentor_type, "")
    code_area = st.text_area("Ask a question or write code to run:", 
                            value=st.session_state.code_input or template, 
                            height=150)
    st.session_state.code_input = code_area

    output_container = st.empty()

    # API Key Check
    if not openrouter_api_key:
        st.warning("⚠️ API Key not configured. Please add your OPENROUTER_API_KEY to use AI features.")
        st.info("💡 The app structure is ready - just add your API key to activate AI responses!")

    # Prompt Setup (Your original)
    if model:
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                f"You are a helpful and experienced {st.session_state.mentor_type.upper()} mentor assisting a user with {experience} years experience. Reply in {lang}."
            ),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

    # Check if this is a career/interview module for different button layout
    is_career_module = st.session_state.mentor_type in [module[0] for module in career_interview]

    if is_career_module:
        # Special buttons for Career & Interview modules
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎯 Get Interview Questions"):
                if code_area and model:
                    try:
                        interview_prompt = ChatPromptTemplate.from_messages([
                            SystemMessagePromptTemplate.from_template(
                                f"Generate relevant interview questions for {st.session_state.mentor_type}. "
                                f"Provide practical questions with difficulty suitable for {experience} years experience. Reply in {lang}."
                            ),
                            HumanMessagePromptTemplate.from_template("{question}")
                        ])
                        messages = interview_prompt.format_messages(question=code_area)
                        response = model.invoke(messages)

                        st.markdown("**📝 Your Topic:**")
                        st.info(code_area)
                        st.markdown("**🎯 Interview Questions:**")
                        st.success(response.content)
                    except Exception as e:
                        output_container.error(f"❌ Error: {str(e)}")
                else:
                    output_container.warning("⚠️ Enter a topic and ensure API key is configured.")

        with col2:
            if st.button("💡 Get Sample Answers"):
                if code_area and model:
                    try:
                        answer_prompt = ChatPromptTemplate.from_messages([
                            SystemMessagePromptTemplate.from_template(
                                f"Provide detailed sample answers for {st.session_state.mentor_type} questions. "
                                f"Make answers suitable for {experience} years experience level. Reply in {lang}."
                            ),
                            HumanMessagePromptTemplate.from_template("{question}")
                        ])
                        messages = answer_prompt.format_messages(question=code_area)
                        response = model.invoke(messages)

                        st.markdown("**❓ Your Question:**")
                        st.info(code_area)
                        st.markdown("**💡 Sample Answer:**")
                        st.success(response.content)
                    except Exception as e:
                        output_container.error(f"❌ Error: {str(e)}")
                else:
                    output_container.warning("⚠️ Enter a question and ensure API key is configured.")

        with col3:
            if st.button("📄 Save Interview Prep"):
                try:
                    filename = f"interview_prep_{st.session_state.mentor_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, "w") as f:
                        f.write(f"# {st.session_state.mentor_type} Interview Preparation\n")
                        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(f"Topic/Question: {code_area}\n\n")
                        f.write("=== NOTES ===\n")
                        f.write("Add your preparation notes here...\n")
                    st.success(f"✅ Interview prep saved as {filename}")
                except Exception as e:
                    st.error(f"❌ Save error: {str(e)}")

    else:
        # Original buttons for programming modules
        col1, col2, col3 = st.columns(3)

        # 🚀 Ask Mentor (Your original functionality)
        with col1:
            if st.button("🚀 Ask Mentor"):
                if code_area:
                    if model:
                        try:
                            messages = prompt.format_messages(question=code_area)
                            response = model.invoke(messages)

                            # Update progress tracking
                            st.session_state.total_queries += 1
                            st.session_state.user_progress[st.session_state.mentor_type]['queries'] += 1

                            # Add to chat history
                            st.session_state.chat_history.append({
                                'module': st.session_state.mentor_type,
                                'question': code_area,
                                'response': response.content,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })

                            # Display user input and response cleanly
                            st.markdown("**👤 Your Question:**")
                            st.info(code_area)
                            st.markdown("**🧠 AI Mentor Response:**")
                            st.success(response.content)

                            # Add bookmark option
                            col_bookmark, col_note = st.columns(2)
                            with col_bookmark:
                                if st.button("🔖 Bookmark This", key="bookmark_response"):
                                    bookmark = {
                                        'module': st.session_state.mentor_type,
                                        'question': code_area,
                                        'response': response.content,
                                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    }
                                    st.session_state.bookmarks.append(bookmark)
                                    st.success("✅ Bookmarked!")

                            with col_note:
                                if st.button("📝 Add Note", key="add_note"):
                                    st.session_state.show_note_input = True
                        except Exception as e:
                            output_container.error(f"❌ Error: {str(e)}")
                    else:
                        output_container.warning("⚠️ Please configure your API key to use AI features.")
                else:
                    output_container.warning("⚠️ Enter a question or code first.")

        # 💻 Run Code (Your original functionality)
        with col2:
            if st.button("💻 Run Code"):
                if st.session_state.mentor_type in ["Python", "Java", "C++"] and code_area:
                    try:
                        with open("temp_code.txt", "w") as f:
                            f.write(code_area)

                        if st.session_state.mentor_type == "Python":
                            result = subprocess.run(["python", "temp_code.txt"], capture_output=True, text=True)
                        elif st.session_state.mentor_type == "C++":
                            subprocess.run(["g++", "temp_code.txt", "-o", "temp.out"], check=True)
                            result = subprocess.run(["./temp.out"], capture_output=True, text=True)
                        elif st.session_state.mentor_type == "Java":
                            with open("Main.java", "w") as f:
                                f.write(code_area)
                            subprocess.run(["javac", "Main.java"], check=True)
                            result = subprocess.run(["java", "Main"], capture_output=True, text=True)

                        st.markdown("**💻 Code Output:**")
                        st.code(result.stdout or result.stderr, language="text")
                    except Exception as e:
                        output_container.error(f"Code execution error: {str(e)}")
                else:
                    output_container.warning("⚠️ Code execution is supported for Python, C++, Java only.")

        # 📥 Save Code (Your original functionality)
        with col3:
            if st.button("📥 Save Code"):
                try:
                    filename = f"saved_code_{st.session_state.mentor_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, "w") as f:
                        f.write(f"# {st.session_state.mentor_type} Code - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(code_area)
                    st.success(f"✅ Code saved as {filename}")
                except Exception as e:
                    st.error(f"❌ Save error: {str(e)}")

    # ✅ Additional Tools (Your original enhanced)
    st.markdown("""
        <div class='tool-section'>
            <h3>🔧 Extra Tools</h3>
            <p>Professional AI-powered tools for enhanced learning</p>
        </div>
    """, unsafe_allow_html=True)

    tool_choice = st.selectbox("Choose AI Tool", [
        "Code Explainer", "Syntax Checker", "Interview Prep", "Resume Feedback", "Cheat Sheet Generator"
    ], index=0)

    tool_input = st.text_area("Enter your content or paste code/question here:", height=150)

    if st.button("🎯 Run Tool"):
        if tool_input:
            if model:
                try:
                    tool_prompt = ChatPromptTemplate.from_messages([
                        SystemMessagePromptTemplate.from_template(
                            f"You are a professional assistant for {tool_choice}. Provide accurate, clear, and brief output in {lang}."
                        ),
                        HumanMessagePromptTemplate.from_template("{question}")
                    ])
                    messages = tool_prompt.format_messages(question=tool_input)
                    tool_result = model.invoke(messages)

                    st.markdown(f"**🎯 {tool_choice} Result:**")
                    st.success(tool_result.content)
                except Exception as e:
                    st.error(f"❌ Tool Error: {str(e)}")
            else:
                st.warning("⚠️ Please configure your API key to use AI tools.")
        else:
            st.warning("⚠️ Please enter something for the tool to work on.")

else:
    

    # Use regular Streamlit components instead of HTML
    st.markdown("### 🌟 Features:")
    st.markdown("""
    - **🧠 AI-Powered Mentoring:** Get personalized guidance from expert AI mentors
    - **💻 Real Code Execution:** Run Python, Java, and C++ code instantly
    - **🎯 Professional Tools:** Code explainer, syntax checker, interview prep, and more
    - **🌍 Multi-Language Support:** Learn in English, Telugu, Hindi, Tamil, Kannada, Malayalam
    - **📊 Comprehensive Modules:** 71 learning modules covering programming, cloud, data science
    """)

    st.markdown("### 🚀 Getting Started:")
    st.markdown("""
    1. **Select a Module:** Choose from 71 modules in the sidebar
    2. **Set Experience:** Adjust the slider based on your skill level
    3. **Choose Language:** Select your preferred interface language
    4. **Start Learning:** Ask questions, write code, and get AI guidance!
    """)

    st.info("💡 **Pro Tip:** Start with a module that matches your current learning goals. The AI mentor will adapt its responses based on your experience level!")

    # ✅ Welcome Test Section
    st.markdown("""
        <div class='tool-section'>
            <h3>🧪 Test the Platform</h3>
            <p>Try a quick test to see how the platform works!</p>
        </div>
    """, unsafe_allow_html=True)

    test_input = st.text_area(
        "🧪 Test Question (Try: 'What is Python?' or 'Explain machine learning'):",
        placeholder="Enter any programming or technology question to test the AI mentor...",
        height=100
    )

    if st.button("🚀 Test AI Mentor", use_container_width=True):
        if test_input.strip():
            if model:
                try:
                    test_prompt = ChatPromptTemplate.from_messages([
                        SystemMessagePromptTemplate.from_template(
                            "You are a helpful programming and technology mentor. Provide clear, concise, and educational responses."
                        ),
                        HumanMessagePromptTemplate.from_template("{question}")
                    ])
                    messages = test_prompt.format_messages(question=test_input)
                    response = model.invoke(messages)

                    st.markdown("**🧪 Test Result:**")
                    st.success(response.content)
                    st.success("✅ Test successful! Now select a module from the sidebar to start learning.")
                except Exception as e:
                    st.error(f"❌ Test Error: {str(e)}")
            else:
                st.warning("⚠️ Please configure your API key to test AI features.")
        else:
            st.warning("⚠️ Enter a test question first.")

# ✅ Additional Features Display
if 'show_progress' in st.session_state and st.session_state.show_progress:
    st.markdown("### 📊 Learning Progress Dashboard")
    if st.session_state.user_progress:
        for module, data in st.session_state.user_progress.items():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"📚 {module}", f"{data['queries']} queries")
            with col2:
                st.metric("📅 Started", data['started'])
            with col3:
                progress_percent = min(data['queries'] * 10, 100)  # 10% per query, max 100%
                st.metric("📈 Progress", f"{progress_percent}%")
    else:
        st.info("Start learning to see your progress!")

    if st.button("❌ Close Progress"):
        del st.session_state.show_progress

if 'show_roadmap' in st.session_state and st.session_state.show_roadmap:
    st.markdown("### 🗺️ Learning Roadmap")

    roadmaps = {
        "Full Stack Developer": ["HTML/CSS", "JavaScript", "React", "Node.js", "SQL", "Git & GitHub"],
        "Data Scientist": ["Python", "Statistics", "Pandas", "Numpy", "Machine Learning", "Deep Learning"],
        "Cloud Engineer": ["Linux", "AWS", "Docker", "Kubernetes", "Terraform", "DevOps"],
        "Mobile Developer": ["Java", "Kotlin", "Swift", "React Native", "Git & GitHub"],
        "AI/ML Engineer": ["Python", "Statistics", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"]
    }

    selected_path = st.selectbox("Choose your career path:", list(roadmaps.keys()))
    st.markdown(f"**🎯 Recommended learning path for {selected_path}:**")

    for i, skill in enumerate(roadmaps[selected_path], 1):
        completed = skill in st.session_state.user_progress
        status = "✅" if completed else "⏳"
        st.markdown(f"{i}. {status} {skill}")

    if st.button("❌ Close Roadmap"):
        del st.session_state.show_roadmap

if 'show_bookmarks' in st.session_state and st.session_state.show_bookmarks:
    st.markdown("### 🔖 My Bookmarks")
    if st.session_state.bookmarks:
        for i, bookmark in enumerate(st.session_state.bookmarks):
            with st.expander(f"📌 {bookmark['module']} - {bookmark['timestamp']}"):
                st.markdown(f"**Question:** {bookmark['question']}")
                st.markdown(f"**Answer:** {bookmark['response']}")
                if st.button(f"🗑️ Remove", key=f"remove_bookmark_{i}"):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()
    else:
        st.info("No bookmarks yet. Click '🔖 Bookmark This' on any AI response!")

    if st.button("❌ Close Bookmarks"):
        del st.session_state.show_bookmarks

if 'show_notes' in st.session_state and st.session_state.show_notes:
    st.markdown("### 📝 My Learning Notes")

    # Add new note
    new_note = st.text_area("✍️ Add a new note:", height=100)
    if st.button("💾 Save Note") and new_note.strip():
        note_key = f"note_{len(st.session_state.user_notes)}"
        st.session_state.user_notes[note_key] = {
            'content': new_note,
            'module': st.session_state.mentor_type or 'General',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        st.success("✅ Note saved!")
        st.rerun()

    # Display existing notes
    if st.session_state.user_notes:
        for note_key, note in st.session_state.user_notes.items():
            with st.expander(f"📄 {note['module']} - {note['timestamp']}"):
                st.markdown(note['content'])
                if st.button(f"🗑️ Delete", key=f"delete_note_{note_key}"):
                    del st.session_state.user_notes[note_key]
                    st.rerun()
    else:
        st.info("No notes yet. Start taking notes to track your learning!")

    if st.button("❌ Close Notes"):
        del st.session_state.show_notes

# ✅ Professional Footer
st.markdown("---")
st.markdown("### 🧠 AI-Powered Learning Mentor")
st.markdown("*Empowering developers worldwide with AI-powered learning*")

# Stats in columns
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📚 Learning Modules", f"{len(all_modules)}")
with col2:
    st.metric("🌍 Languages", "6")
with col3:
    st.metric("⚡ AI Response", "Real-time")
with col4:
    st.metric("🔧 Tools", "8+")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>© 2024 Powered by <strong>Munesula Vamshi</strong> | AI-Powered Learning Mentor</p>
    <p><em>Professional Edition • Real-time API Integration • Advanced Learning Platform</em></p>
</div>
""", unsafe_allow_html=True)
