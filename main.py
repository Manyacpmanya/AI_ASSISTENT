from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, text
import requests
from config import DB_URI, OLLAMA_URL, MODEL_NAME
from rag_utils import split_text, create_embeddings, build_index, retrieve_chunks

app = Flask(__name__)
engine = create_engine(DB_URI)

def get_all_data():
    with engine.connect() as conn:
        result = conn.execute(text("""
        SELECT u.name, u.usn, u.branch, sa.cgpa
        FROM users u
        JOIN student_academics sa ON u.id = sa.student_id
        """))
        rows = result.fetchall()
        return " ".join([str(r) for r in rows])

def ask_ollama(context, question):
    prompt = f"""
You are an AI assistant for a college HOD.

IMPORTANT RULES:
- DO NOT write code
- DO NOT explain programming steps
- Give only final answer
- Answer should be clean and user-friendly
- Use bullet points or numbering
- Keep it short and clear
- If data is available, answer directly from it

DATA:
{context}

QUESTION:
{question}

FINAL ANSWER:
"""

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False   # ✅ Fix for JSON error
        })

        data = res.json()

        # ✅ Safe extraction
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        else:
            return "⚠️ Unable to generate proper response."

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

is_processing = False   # 🔒 GLOBAL LOCK

@app.route("/ask", methods=["POST"])
def ask():
    global is_processing

    # 🚫 Block multiple requests
    if is_processing:
        return jsonify({"answer": "⏳ Please wait... processing previous request"}), 429

    is_processing = True  # 🔒 Lock

    try:
        question = request.json.get("question")

        data = get_all_data()
        chunks = split_text(data)
        embeddings = create_embeddings(chunks)
        index = build_index(embeddings)

        query_embedding = create_embeddings([question])[0]
        top = retrieve_chunks(index, query_embedding)

        context = " ".join([chunks[i] for i in top if i < len(chunks)])

        answer = ask_ollama(context, question)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"❌ Error: {str(e)}"})

    finally:
        is_processing = False   # 🔓 Unlock (VERY IMPORTANT)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
