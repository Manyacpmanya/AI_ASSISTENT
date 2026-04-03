# AI_ASSISTENT
LLM model for all web development

## 🔐 Configuration Setup

This project requires a configuration file for database and API settings.

### 🔹 Step 1: Create config.py and update values
Update with your local system database details:

DB_URI = "mysql+pymysql://root:yourpassword@localhost/your_db"

OLLAMA_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "llama3"

---

## 🐍 Python Setup (Installation)

Python is the **main engine** of this project — it runs backend logic, database operations, and AI processing.

---

### 🔹 Step 1: Install Python

#### 🪟 Windows

1. Download Python from official website
2. Run installer
3. Check: Add Python to PATH
4. Click Install

#### 🐧 Ubuntu

sudo apt update
sudo apt install python3 python3-pip -y

---

### 🔹 Step 2: Verify Installation

#### 🪟 Windows

python --version

#### 🐧 Ubuntu

python3 --version

---

### 🔹 Step 3: Install & Verify pip

#### 🪟 Windows

python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip --version

#### 🐧 Ubuntu

python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
pip3 --version

---

## 🤖 Ollama Setup (LLM Installation)

Ollama lets you run AI models locally without cloud APIs.

---

### 🔹 Step 1: Install Ollama

#### 🪟 Windows

* Download and install Ollama
* Open it (runs in background)

#### 🐧 Ubuntu

curl -fsSL https://ollama.com/install.sh | sh

---

### 🔹 Step 2: Verify Installation

ollama --version

---

### 🔹 Step 3: Download LLaMA3 Model

ollama pull llama3

---

### 🔹 Step 4: Run the Model

ollama run llama3

---

### 🔹 Step 5: API Usage

http://localhost:11434

---

## ▶️ Run the Project

### 🔹 Step 1: Verify Installations

#### 🪟 Windows

python --version
ollama --version

#### 🐧 Ubuntu

python3 --version
ollama --version

---

### 🔹 Step 2: Navigate to Project Folder

#### 🪟 Windows

cd "your-project-folder-path"

#### 🐧 Ubuntu

cd /path/to/your/project

---

### 🔹 Step 3: Create Virtual Environment

#### 🪟 Windows

python -m venv venv

#### 🐧 Ubuntu

python3 -m venv venv

---

### 🔹 Step 4: Activate Virtual Environment

#### 🪟 Windows

venv\Scripts\activate

#### 🐧 Ubuntu

source venv/bin/activate

---

### 🔹 Step 5: Install Dependencies

#### 🪟 Windows

pip install -r requirements.txt

#### 🐧 Ubuntu

pip3 install -r requirements.txt

---

### 🔹 Step 6: Run the Application

#### 🪟 Windows

python main.py

#### 🐧 Ubuntu

python3 main.py

---

### ✅ Output

* Flask server starts
* Open browser → http://127.0.0.1:5001
* Your AI assistant is ready 🚀


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
