import os
import streamlit as st
from langchain.chat_models import ChatOpenAI  # ✅ use this
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


import streamlit as st
from langchain_community.chat_models import ChatOpenAI

# Get API key from Streamlit secrets
openrouter_api_key = st.secrets["OPENROUTER_API_KEY"]

# Initialize the chat model with API key and base URL
model = ChatOpenAI(
    model_name="mistralai/mistral-7b-instruct:free",
    temperature=0.5,
    max_tokens=300,
    openai_api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)



# ... rest of your code here ...


# Set the API base for OpenRouter
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = openrouter_api_key

st.set_page_config(page_title="Quality Thought AI Mentor", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #fefefe;
        padding: 20px;
    }
    .stButton>button {
        background-color: white;
        color: #8B0000;
        border: 2px solid white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #8B0000;
        color: white;
        border: 2px solid white;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label, input, textarea, select, option, .stTextInput, .stSlider, .stSelectbox, .stTextArea, .stMarkdown {
        color: black !important;
    }
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .user-message {
        background-color: rgba(183, 111, 39, 0.3);
        text-align: right;
    }
    .bot-message {
        background-color: rgba(139, 0, 0, 0.3);
    }
    .module-btn {
        font-size: 24px !important;
        padding: 15px 0 !important;
    }
    .stAlert {
        color: black !important;
    }
    .welcome-box {
        text-align: center;
        background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        animation: fadeIn 2s ease-in-out;
    }
    .powered-by {
        text-align: center;
        margin-top: 50px;
        font-weight: bold;
        color: #8B0000;
        font-size: 18px;
    }
    .sidebar-module-button {
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        background-color: #f0f0f0;
        color: #333;
        width: 100%;
        text-align: left;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='welcome-box'>
    <h1>Welcome to Quality Thought AI Mentor 🧠</h1>
    <p>Your personal AI mentor for coding, analytics, and data science modules.</p>
    <p>Ask anything related to Python, SQL, PowerBI, Statistics, ML & DL in your preferred language!</p>
    <p>New update: Explore all major programming languages and interview topics from the sidebar.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for modules
st.sidebar.title("📚 Select a Module")
modules = [
    ("Python", "🐍"),
    ("SQL", "📓"),
    ("PowerBI", "📊"),
    ("Statistics", "📈"),
    ("Machine Learning", "🤖"),
    ("Deep Learning", "🧠"),
    ("Java", "☕"),
    ("JavaScript", "🟨"),
    ("C++", "💻"),
    ("HTML/CSS", "🌐"),
    ("R Programming", "📊"),
    ("Data Structures", "🗂️"),
    ("Algorithms", "🔍"),
    ("System Design", "🏗️"),
    ("Linux", "🐧"),
    ("DevOps", "⚙️"),
    ("Git & GitHub", "🔧")
]

if 'mentor_type' not in st.session_state:
    st.session_state.mentor_type = None
if 'mentor_emoji' not in st.session_state:
    st.session_state.mentor_emoji = "🧠"

for module, emoji in modules:
    if st.sidebar.button(f"{emoji} {module}"):
        st.session_state.mentor_type = module
        st.session_state.mentor_emoji = emoji

if st.session_state.mentor_type:
    st.subheader(f"{st.session_state.mentor_emoji} {st.session_state.mentor_type.upper()} Mentor Chat")
    experience = st.slider("Your experience (in years):", 0, 20, 1)
    user_input = st.text_input("Ask your question (multi-language supported):")
    output_container = st.empty()

    model = ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        temperature=0.5,
        max_tokens=300
    )

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            f"You are a helpful and experienced {st.session_state.mentor_type.upper()} mentor {st.session_state.mentor_emoji} assisting a learner with {experience} years of experience."
        ),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("🚀 Ask"):
            if user_input:
                try:
                    messages = prompt.format_messages(question=user_input)
                    response = model.invoke(messages)
                    output_container.markdown(f"**👤 You:** {user_input}")
                    output_container.markdown(f"**{st.session_state.mentor_emoji} Mentor:** {response.content}")
                except Exception as e:
                    output_container.error(f"An error occurred: {str(e)}")
            else:
                output_container.warning("Please enter a question first!")

    with btn_col2:
        if st.button("🧹 Clear"):
            output_container.empty()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='powered-by'>🚀 Powered by Vamshi</div>", unsafe_allow_html=True)
