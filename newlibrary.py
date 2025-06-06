import streamlit as st 
import sqlite3
import pandas as pd
import datetime
import base64
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import time
import random
from huggingface_hub import InferenceClient

# --- Setup page ---
st.set_page_config(page_title="📚 Digital Library Management System", layout="wide")

# --- Theme Presets ---
theme_options = {
    "Classic": {"bg": "#f9fafb", "text": "#111827", "card": "white"},
    "Pastel": {"bg": "#fdf6f0", "text": "#5b3a29", "card": "#fff4e6"},
    "Minimal": {"bg": "#ffffff", "text": "#000000", "card": "#f3f4f6"},
    "Cool Blue": {"bg": "#e0f2fe", "text": "#0c4a6e", "card": "#bae6fd"}
}

if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = "Classic"

# --- Sidebar Theme Selector ---
st.sidebar.markdown("### 🎨 Select Theme")
st.session_state.selected_theme = st.sidebar.selectbox("Choose a UI theme:", list(theme_options.keys()))
theme = theme_options[st.session_state.selected_theme]

# --- Apply Selected Theme ---
st.markdown(f"""
    <style>
        html, body, .stApp {{
            background-color: {theme['bg']};
            font-family: 'Segoe UI', sans-serif;
            color: {theme['text']};
            margin: 0;
            padding: 0;
        }}
        .main > div:first-child {{
            padding-top: 1.5rem;
            background-color: {theme['card']};
            border-radius: 12px;
            margin: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            animation: fadeIn 0.8s ease-in-out;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #f3f4f6 !important;
            padding: 1rem;
            border-right: 1px solid #e5e7eb;
            animation: slideIn 0.8s ease-in-out;
        }}
        h1, h2, h3, h4 {{
            color: #1e3a8a;
            font-weight: 700;
        }}
        .stButton > button {{
            background-color: #2563eb;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: #1d4ed8;
            transform: scale(1.03);
        }}
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {{
            background-color: white !important;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px;
        }}
        .stRadio > div {{
            gap: 8px;
        }}
        @keyframes fadeIn {{
            0% {{opacity: 0;}}
            100% {{opacity: 1;}}
        }}
        @keyframes slideIn {{
            0% {{transform: translateX(-30px); opacity: 0;}}
            100% {{transform: translateX(0); opacity: 1;}}
        }}
        #clock {{
            font-size: 13px;
            color: #4b5563;
            text-align: center;
            margin-top: 10px;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Digital Clock ---
st.sidebar.markdown("""
    <div id="clock">⏰ <span id="time"></span></div>
    <script>
        const timeSpan = window.parent.document.getElementById('time');
        setInterval(() => {
            const now = new Date();
            timeSpan.innerHTML = now.toLocaleTimeString();
        }, 1000);
    </script>
""", unsafe_allow_html=True)

# --- Welcome Toast ---
if 'toast_shown' not in st.session_state:
    st.toast("👋 Welcome to the Digital Library Management System!", icon="📘")
    st.session_state.toast_shown = True

st.title("📚 Digital Library Management System")

# --- AI Chatbot Helper (HuggingFace API) ---
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")  # Put this in your `.env` file or system environment

with st.sidebar.expander("🧠 Ask the Library Mentor"):
    user_q = st.text_input("Type your question:")
    if st.button("Ask AI") and user_q:
        try:
            model = ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                model_name="mistralai/mistral-7b-instruct",
                temperature=0.7
            )

            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful digital library mentor guiding users on any book-related or technical queries."
                ),
                HumanMessagePromptTemplate.from_template("{question}")
            ])

            messages = prompt.format_messages(question=user_q)
            response = model.invoke(messages)
            st.info(response.content)
        except Exception as e:
            st.warning(f"❌ AI error: {str(e)}")

# --- Footer ---
st.markdown("""
    <div style='text-align: center; font-size: 14px; padding: 15px; color: #6b7280;'>
        © 2025 Digital Library Management System | Crafted with ❤️ by 
        <span style='color: #1e40af; font-weight: 600;'>VAMSHI</span>
    </div>
""", unsafe_allow_html=True)

# --- Database Connection ---
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Library (
        BK_NAME TEXT, BK_ID TEXT PRIMARY KEY, AUTHOR_NAME TEXT, BK_STATUS TEXT, 
        CARD_ID TEXT, COVER BLOB, ADDED_ON TEXT, RESERVED_BY TEXT, RATING INTEGER, REVIEW TEXT
    )
""")
conn.commit()

# --- Navigation Sidebar ---
tabs = st.sidebar.radio("Choose Feature:", [
    "➕ Add Book", "📄 View Books", "✏️ Edit Book", "🗑️ Delete", "📌 Reserve", "⭐ Rate", 
    "🔍 Search", "📊 Stats", "📤 Export", "📥 Import CSV"
])

# --- Smart Filter (only in View Books) ---
if tabs == "📄 View Books":
    st.markdown("### 🔎 Smart Filters")
    with st.expander("Click to filter by Author or Status"):
        authors = pd.read_sql("SELECT DISTINCT AUTHOR_NAME FROM Library", conn)['AUTHOR_NAME'].tolist()
        statuses = pd.read_sql("SELECT DISTINCT BK_STATUS FROM Library", conn)['BK_STATUS'].tolist()
        selected_author = st.selectbox("Filter by Author", ["All"] + authors)
        selected_status = st.selectbox("Filter by Status", ["All"] + statuses)

        query = "SELECT * FROM Library"
        filters = []
        if selected_author != "All":
            filters.append(f"AUTHOR_NAME = '{selected_author}'")
        if selected_status != "All":
            filters.append(f"BK_STATUS = '{selected_status}'")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        df = pd.read_sql(query, conn)
        st.dataframe(df)

# --- Feature Pages Logic (assumed unchanged) ---
# --- Functions ---
def add_book(name, book_id, author, status, card_id, cover_file):
    cover_data = cover_file.read() if cover_file else None
    added_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""
            INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, COVER, ADDED_ON)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, book_id, author, status, card_id, cover_data, added_on))
        conn.commit()
        st.success(f"✅ Book '{name}' added successfully!")
    except sqlite3.IntegrityError:
        st.error("🚫 Book ID already exists!")

def show_books():
    cursor.execute("SELECT BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, ADDED_ON FROM Library")
    data = cursor.fetchall()
    if not data:
        st.info("No books available.")
        return
    df = pd.DataFrame(data, columns=["Book Name", "Book ID", "Author", "Status", "Card ID", "Added On"])
    df["Added On"] = pd.to_datetime(df["Added On"]).dt.strftime('%Y-%m-%d %H:%M:%S')
    st.markdown("## 📚 All Books")
    st.dataframe(df, use_container_width=True)

def delete_book(book_id):
    cursor.execute("DELETE FROM Library WHERE BK_ID=?", (book_id,))
    conn.commit()
    st.success("🗑️ Book deleted successfully!")

def reserve_book(book_id, card_id):
    cursor.execute("UPDATE Library SET BK_STATUS='Issued', CARD_ID=? WHERE BK_ID=?", (card_id, book_id))
    conn.commit()
    st.success("📌 Book reserved successfully!")

def rate_book(book_id, rating, review):
    cursor.execute("UPDATE Library SET RATING=?, REVIEW=? WHERE BK_ID=?", (rating, review, book_id))
    conn.commit()
    st.success("⭐ Rating submitted successfully!")

def show_statistics():
    total = cursor.execute("SELECT COUNT(*) FROM Library").fetchone()[0]
    available = cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Available'").fetchone()[0]
    issued = cursor.execute("SELECT COUNT(*) FROM Library WHERE BK_STATUS='Issued'").fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Total Books", total)
    col2.metric("✅ Available", available)
    col3.metric("📤 Issued", issued)

    st.subheader("📊 Library Statistics Chart")
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(['Total', 'Available', 'Issued'], [total, available, issued], color=['blue', 'green', 'red'])
    st.pyplot(fig)

def export_books():
    cursor.execute("SELECT BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, ADDED_ON FROM Library")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Book Name", "Book ID", "Author", "Status", "Card ID", "Added On"])
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="library_inventory.csv">📥 Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

# --- Feature Pages ---
if tabs == "➕ Add Book":
    st.subheader("➕ Add a New Book")
    bk_name = st.text_input("Book Name")
    bk_id = st.text_input("Book ID")
    author = st.text_input("Author")
    status = st.selectbox("Status", ["Available", "Issued"])
    card_id = st.text_input("Card ID")
    cover_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
    if st.button("Add Book"):
        add_book(bk_name, bk_id, author, status, card_id, cover_file)

elif tabs == "📄 View Books":
    st.subheader("📄 Book Inventory")
    show_books()

elif tabs == "✏️ Edit Book":
    st.subheader("✏️ Edit Book Details")
    edit_id = st.text_input("Enter Book ID to Edit")
    if edit_id:
        cursor.execute("SELECT * FROM Library WHERE BK_ID=?", (edit_id,))
        book = cursor.fetchone()
        if book:
            new_name = st.text_input("Book Name", value=book[0])
            new_author = st.text_input("Author", value=book[2])
            new_status = st.selectbox("Status", ["Available", "Issued"], index=0 if book[3]=="Available" else 1)
            new_card_id = st.text_input("Card ID", value=book[4])
            if st.button("Update Book"):
                cursor.execute("""
                    UPDATE Library SET BK_NAME=?, AUTHOR_NAME=?, BK_STATUS=?, CARD_ID=? WHERE BK_ID=?
                """, (new_name, new_author, new_status, new_card_id, edit_id))
                conn.commit()
                st.success("✅ Book updated successfully!")
        else:
            st.error("❌ Book ID not found!")

elif tabs == "🗑️ Delete":
    st.subheader("🗑️ Delete Book")
    del_id = st.text_input("Enter Book ID to Delete")
    if st.button("Delete"):
        delete_book(del_id)

elif tabs == "📌 Reserve":
    st.subheader("📌 Reserve a Book")
    res_id = st.text_input("Enter Book ID")
    res_card = st.text_input("Enter Card ID")
    if st.button("Reserve"):
        reserve_book(res_id, res_card)

elif tabs == "⭐ Rate":
    st.subheader("⭐ Rate a Book")
    rate_id = st.text_input("Enter Book ID")
    rating = st.slider("Select Star Rating", 1, 5)
    review = st.text_area("Write a review")
    if st.button("Submit Rating"):
        rate_book(rate_id, rating, review)

elif tabs == "🔍 Search":
    st.subheader("🔍 Search Book")
    search_q = st.text_input("Enter title, author or book ID")
    if search_q:
        cursor.execute("SELECT * FROM Library WHERE BK_NAME LIKE ? OR BK_ID LIKE ? OR AUTHOR_NAME LIKE ?", (f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"))
        results = cursor.fetchall()
        for book in results:
            st.write(f"📖 {book[0]} | 🆔 {book[1]} | ✍️ {book[2]}")

elif tabs == "📊 Stats":
    st.subheader("📊 Library Statistics")
    show_statistics()

elif tabs == "📤 Export":
    st.subheader("📤 Export Inventory")
    export_books()

elif tabs == "📥 Import CSV":
    st.subheader("📥 Import Library Records from CSV")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = {"Book Name", "Book ID", "Author", "Status", "Card ID", "Added On"}
            if not required_cols.issubset(df.columns):
                st.error(f"❌ CSV must contain columns: {', '.join(required_cols)}")
            else:
                inserted = 0
                for _, row in df.iterrows():
                    try:
                        cursor.execute("""
                            INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID, ADDED_ON)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            row["Book Name"], row["Book ID"], row["Author"], row["Status"], row["Card ID"], row["Added On"]
                        ))
                        inserted += 1
                    except sqlite3.IntegrityError:
                        continue
                conn.commit()
                st.success(f"✅ Imported {inserted} new records successfully!")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")