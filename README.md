# AI_ASSISTENT
LLM model for all web development

## 🔁 System Flow

ai_assistent.php (UI)  
↓  
fetch() API call  
↓  
main.py (/ask route)  
↓  
get_all_data() → MySQL  
↓  
rag_utils.py (RAG processing)  
↓  
Ollama API  
↓  
Return Answer  
↓  
UI display  

---

## 🟢 1. User Question (Frontend Input)

JavaScript code:

let question = document.getElementById("question").value;

Explanation:
- Finds input box
- Gets user input

Example:
Input: Show CGPA of 4GW22CS001

---

JavaScript API Call:

let res = await fetch("http://127.0.0.1:5001/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
});

Explanation:
- Sends data to backend
- Converts to JSON

---

## 🟢 2. Backend API (Flask)

@app.route('/ask', methods=['POST'])
def ask():

Explanation:
- API endpoint to receive request

---

question = request.json['question']

Output:
question = "Show CGPA of 4GW22CS001"

---

## 🟢 3. Fetch Table Data (MySQL)

SQL Query:

SELECT u.name, u.usn, u.branch, sa.cgpa
FROM users u
JOIN student_academics sa ON u.id = sa.student_id

Example Output:

Ram | 4GW22CS001 | 8.5

---

rows = result.fetchall()

Output:
[('Ram','4GW22CS001','CSE',8.5)]

---

data = " ".join([str(r) for r in rows])

Output:
(Ram, 4GW22CS001, CSE, 8.5)

---

## 🟢 4. Split Data into Chunks

words = text.split()

Chunks:
Chunk 1: (Ram, 4GW22CS001, CSE, 8.5)  
Chunk 2: (Ravi, 4GW22CS002, CSE, 9.1)

Reason:
LLM cannot process large data at once

---

## 🟢 5. Generate Embeddings

model.encode(chunks)

Example:
"Ram 4GW22CS001 8.5"
→ [0.12, -0.45, 0.89]

Meaning:
Similar text → similar vectors

---

## 🟢 6. Store in FAISS

dim = len(embeddings[0])  
index = faiss.IndexFlatL2(dim)  
index.add(np.array(embeddings))  

Purpose:
Fast similarity search

---

## 🟢 7. Question → Embedding

query_embedding = create_embeddings([question])[0]

Example:
"Show CGPA of 4GW22CS001"
→ [0.11, -0.40, 0.91]

---

## 🟢 8. Similarity Search

D, I = index.search(np.array([query_embedding]), k)

Output:
I = [0]

Meaning:
Most relevant chunk found

---

## 🟢 9. Build Context

context = " ".join([chunks[i] for i in top])

Output:
(Ram, 4GW22CS001, CSE, 8.5)

---

## 🟢 10. Send to LLM (Ollama)

Prompt:

DATA:
(Ram, 4GW22CS001, CSE, 8.5)

QUESTION:
Show CGPA of 4GW22CS001

---

## 🟢 11. LLM Decision

Case 1:
SELECT cgpa FROM students WHERE usn='4GW22CS001';

Case 2:
CGPA is 8.5

---

## 🟢 12. Execute SQL

result = conn.execute(text(sql_query)).fetchone()

Output:
(8.5)

---

## 🟢 13. Format Response

final_answer = "CGPA is 8.5"

---

## 🟢 14. Return to UI

return jsonify({"answer": final_answer})

Output:
{
  "answer": "CGPA is 8.5"
}

---

## 🟢 15. Save to chat_logs

INSERT INTO chat_logs (question, answer)

Example:

Show CGPA of 4GW22CS001 → CGPA is 8.5

---

## 📦 requirements.txt Explanation

flask  
Backend server

sqlalchemy  
Database connection

pymysql  
MySQL driver

faiss-cpu  
Vector search

sentence-transformers  
Embeddings

numpy  
Numerical processing

requests  
API calls

python-dotenv  
Environment variables

---

## 🧠 What is NumPy?

NumPy is used for handling arrays and vectors.

Features:
- Faster than Python lists
- Used for calculations
- Required for embeddings

Example:
[0.12, -0.45, 0.89]
