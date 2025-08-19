import streamlit as st
import os
from dotenv import load_dotenv
import requests
import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
st.set_page_config(
    page_title="Battle of the Bots",
    page_icon="🤖⚔️",
    layout="wide"
)
st.markdown("""
<style>
body {
    background: url('https://images.unsplash.com/photo-1612832021480-feb5b74c1a65?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzMjM4NDZ8MHwxfGFsbHwxfHxhaSUyQ2h1bWFufGVufDB8fHx8MTY5xNjYxNTk5&ixlib=rb-4.0.3&q=80&w=1080') no-repeat center center fixed;
    background-size: cover;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.title {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 2px 2px 8px #000;
}
.subheader {
    text-align: center;
    font-size: 1.5rem;
    color: #FFD700;
    margin-bottom: 2rem;
}
.card {
    background: linear-gradient(145deg, rgba(0,0,0,0.7), rgba(30,30,30,0.7));
    border-radius: 15px;
    padding: 25px;
    margin: 15px;
    transition: transform 0.2s;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
}
.card h3 {
    color: #FFD700;
}
.card p {
    color: #FFF;
    line-height: 1.5;
}
.rating {
    margin-top: 10px;
    margin-bottom: 20px;
}
.download-btn {
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🤖⚔️ Battle of the Bots ⚔️🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">See which AI stands out with bold opinions!</div>', unsafe_allow_html=True)
if OPENROUTER_API_KEY:
    st.success("✅ OpenRouter API key detected from .env file.")
else:
    st.warning("⚠️ API key NOT found. API calls will fail!")

st.markdown("---")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS = {
    "GPT Free": "openai/gpt-3.5-turbo",
    "DeepSeek Free": "deepseek/deepseek-chat-v3-0324",
    "LLaMa Free": "meta-llama/llama-4-maverick"
}
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
def ask_model(model_id, prompt):
    try:
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "You are free to give strong, distinct, and opinionated answers. Avoid being neutral."},
                {"role": "user", "content": prompt}
            ]
        }
        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ API call failed: {e}"

def extract_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def find_most_contrasting_sentence(all_responses):
    all_sentences = {m: extract_sentences(t) for m, t in all_responses.items()}
    contrasting = {}
    vectorizer = TfidfVectorizer()
    for model, sentences in all_sentences.items():
        max_score = -1
        chosen = ""
        for sentence in sentences:
            others = [s for m, sents in all_sentences.items() if m != model for s in sents]
            if not others: continue
            tfidf = vectorizer.fit_transform([sentence] + others)
            distances = cosine_distances(tfidf[0:1], tfidf[1:]).flatten()
            score = distances.mean()
            if score > max_score:
                max_score = score
                chosen = sentence
        contrasting[model] = chosen
    return contrasting

def generate_pdf(results, contrasts, ratings, user_prompt):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Battle of the Bots - Results")
    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Prompt: {user_prompt}")
    y -= 30
    for model, text in results.items():
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, model)
        y -= 20
        c.setFont("Helvetica", 11)
        for line in text.split("\n"):
            c.drawString(60, y, line[:90])
            y -= 15
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(60, y, f"Most Contrasting Sentence: {contrasts.get(model, 'N/A')}")
        y -= 15
        c.drawString(60, y, f"User Rating: {ratings.get(model, 'N/A')}/5")
        y -= 30
    winner = max(ratings, key=ratings.get)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"🏆 Winner: {winner} with {ratings[winner]}⭐")
    c.save()
    buffer.seek(0)
    return buffer
if "results" not in st.session_state:
    st.session_state.results = {}
if "contrasts" not in st.session_state:
    st.session_state.contrasts = {}
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
user_prompt = st.text_area(
    "Enter your provocative question:",
    "Should AI be allowed to vote in political elections?"
)
if st.button("🔥 Run the Battle"):
    with st.spinner("⚔️ Summoning AI gladiators..."):
        st.session_state.results = {name: ask_model(mid, user_prompt) for name, mid in MODELS.items()}
        st.session_state.contrasts = find_most_contrasting_sentence(st.session_state.results)

results = st.session_state.results
contrasts = st.session_state.contrasts
ratings = st.session_state.ratings


if results:
    for model, text in results.items():
        st.markdown(
            f"""
            <div class="card">
                <h3>{model}</h3>
                <p>{text}</p>
                <p><b>Most Contrasting Sentence:</b> <i>{contrasts.get(model, 'N/A')}</i></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        ratings[model] = st.slider(f"Rate {model}'s response:", 1, 5, key=f"rating_{model}")

    st.session_state.ratings = ratings
    winner = max(ratings, key=ratings.get)
    st.success(f"🏆 Winner: {winner} with {ratings[winner]}⭐")

    pdf_file = generate_pdf(results, contrasts, ratings, user_prompt)
    st.download_button(
        label="📄 Download Battle as PDF",
        data=pdf_file,
        file_name="battle_of_the_bots.pdf",
        mime="application/pdf"
    )
