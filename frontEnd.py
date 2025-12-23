import streamlit as st
from email.message import EmailMessage
import smtplib

st.set_page_config(page_title="RIASEC Test", layout="centered")

st.title("RIASEC Career Interest Test")

# ---------- USER INFO ----------
with st.form("info_form"):
    Name = st.text_input("Name")
    Education = st.text_input("Education")
    School = st.text_input("School / University")
    Subjects = st.text_input("Subjects")
    Email = st.text_input("Email")
    Phone = st.text_input("Phone Number")
    start = st.form_submit_button("Start Test")

if not start:
    st.stop()

# ---------- RIASEC SETUP ----------
scores = {
    "R": 0,
    "I": 0,
    "A": 0,
    "S": 0,
    "E": 0,
    "C": 0
}

questions = [
    ("I like to work on cars", "R"),
    ("I like to do puzzles", "I"),
    ("I am good at working independently", "A"),
    ("I like to work in teams", "S"),
    ("I am an ambitious person, I set goals for myself", "E"),
    ("I like to organize things (files, desks/offices)", "C"),
    ("I like to build things", "R"),
    ("I like to read about art and music", "A"),
    ("I like to have clear instructions to follow", "C"),
    ("I like to try to influence or persuade people", "E"),
    ("I like to do experiments", "I"),
    ("I like to teach or train people", "S"),
    ("I like trying to help people solve their problems", "S"),
    ("I like to take care of animals", "R"),
    ("I wouldn’t mind working 8 hours per day in an office", "C"),
    ("I like selling things", "E"),
    ("I enjoy creative writing", "A"),
    ("I enjoy science", "I"),
    ("I am quick to take on new responsibilities", "E"),
    ("I am interested in healing people", "S"),
    ("I enjoy trying to figure out how things work", "I"),
    ("I like putting things together or assembling things", "R"),
    ("I am a creative person", "A"),
    ("I pay attention to details", "C"),
    ("I like to do filing or typing", "C"),
    ("I like to analyze things", "I"),
    ("I like to play instruments or sing", "A"),
    ("I enjoy learning about other cultures", "S"),
    ("I would like to start my own business", "E"),
    ("I like to cook", "R"),
    ("I like acting in plays", "A"),
    ("I am a practical person", "R"),
    ("I like working with numbers or charts", "I"),
    ("I like to get into discussions about issues", "S"),
    ("I am good at keeping records of my work", "C"),
    ("I like to lead", "E"),
    ("I like working outdoors", "R"),
    ("I would like to work in an office", "C"),
    ("I’m good at math", "I"),
    ("I like helping people", "S"),
    ("I like to draw", "A"),
    ("I like to give speeches", "E")
]

st.header("Answer each question (1 = least like you, 5 = most like you)")

responses = []

with st.form("test_form"):
    for q, cat in questions:
        score = st.slider(q, 1, 5, 3, key=q)
        responses.append((q, cat, score))
        scores[cat] += score

    submit = st.form_submit_button("Submit Test")

if not submit:
    st.stop()

# ---------- EMAIL ONLY (NO DISPLAY) ----------
info = f"""Name: {Name}
Education: {Education}
School: {School}
Subjects: {Subjects}
Email: {Email}
Phone: {Phone}
"""

totals = f"""Realistic: {scores['R']}
Investigative: {scores['I']}
Artistic: {scores['A']}
Social: {scores['S']}
Enterprising: {scores['E']}
Conventional: {scores['C']}
"""

table = "\n".join(f"{q},{c},{s}" for q, c, s in responses)

msg = EmailMessage()
msg["From"] = st.secrets["EMAIL"]
msg["To"] = st.secrets["RECEIVER"]
msg["Subject"] = f"RIASEC Test Results – {Name}"

msg.set_content(f"""{info}

{totals}

Responses:
{table}
""")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(
        st.secrets["EMAIL"],
        st.secrets["EMAIL_PASSWORD"]
    )
    server.send_message(msg)

st.success(
    "Tripti Chapper Careers Counselling at mycareerhorizons@gmail.com has received your results. "
    "Please contact them to get your report."
)

