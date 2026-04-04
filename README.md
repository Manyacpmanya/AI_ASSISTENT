

# AI_ASSISTENT
LLM model for all web development


## 🐍 Python Setup (Installation)

Python is the main engine of this project — it runs backend logic, database operations, and AI processing.

---

### Step 1: Install Python

#### Windows

1. Download Python from official website
2. Run installer
3. Check "Add Python to PATH"
4. Click Install

#### Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

---

### Step 2: Verify Installation

#### Windows

```bash
python --version
```

#### Ubuntu

```bash
python3 --version
```

---

### Step 3: Install & Verify pip

#### Windows

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip --version
```

#### Ubuntu

```bash
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
pip3 --version
```

---

## 🤖 Ollama Setup (LLM Installation)

Ollama lets you run AI models locally without cloud APIs.

---

### Step 1: Install Ollama

#### Windows

* Download and install Ollama
* Open it (runs in background)

#### Ubuntu

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

### Step 2: Verify Installation

```bash
ollama --version
```

---

### Step 3: Download LLaMA3 Model

```bash
ollama pull llama3
```

---

### Step 4: Run the Model

```bash
ollama run llama3
```

---

### Step 5: API Usage

```
http://localhost:11434
```

---

## ▶️ Run the Project

### Step 1: Verify Installations

#### Windows

```bash
python --version
ollama --version
```

#### Ubuntu

```bash
python3 --version
ollama --version
```

---

### Step 2: Navigate to Project Folder

#### Windows / Ubuntu

```bash
cd "your-project-folder-path"
```

### Step 3: Create Virtual Environment

#### Windows

```bash
python -m venv venv
```

#### Ubuntu

```bash
python3 -m venv venv
```

---

### Step 4: Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Ubuntu

```bash
source venv/bin/activate
```

---

### Step 5: Install Dependencies

#### Windows

```bash
pip install -r requirements.txt
```

#### Ubuntu

```bash
pip3 install -r requirements.txt
```
---

Step 6:🔐 Configuration Setup

This project requires a configuration file for database and API settings.

### Step 1: Create config.py and update values

Update with your local system database details:

```python
DB_URI = "mysql+pymysql://root:yourpassword@localhost/your_db"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"
````
Make sure to execute the SQL queries provided in the `sample_db.sql` file using MySQL Workbench before running the project.

---


### Step 7: Run the Application

#### Windows

```bash
python main.py
```

#### Ubuntu

```bash
python3 main.py
```

---

### Output

* Flask server starts
* Open browser: [http://127.0.0.1:5001](http://127.0.0.1:5001)
* Your AI assistant is ready

---

## 🔁 System Flow

```
index.html  (ai_assistent ui)
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
```

---

## 🟢 1. User Question (Frontend Input)

```javascript
let question = document.getElementById("question").value;
```

Explanation:

* Finds input box
* Gets user input

Example:

```
Show CGPA of 4GW22CS001
```

---

## 🟢 JavaScript API Call

```javascript
let res = await fetch("http://127.0.0.1:5001/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
});
```

Explanation:

* Sends data to backend
* Converts to JSON

---

## 🟢 2. Backend API (Flask)

```python
@app.route('/ask', methods=['POST'])
def ask():
```

```python
question = request.json['question']
```

Output:

```
"Show CGPA of 4GW22CS001"
```

---

## 🟢 3. Fetch Table Data (MySQL)

```sql
SELECT u.name, u.usn, u.branch, sa.cgpa
FROM users u
JOIN student_academics sa ON u.id = sa.student_id
```

Example Output:

```
Ram | 4GW22CS001 | CSE | 8.5
```

---

```python
rows = result.fetchall()
```

```
[('Ram','4GW22CS001','CSE',8.5)]
```

---

```python
data = " ".join([str(r) for r in rows])
```

```
(Ram, 4GW22CS001, CSE, 8.5)
```

---

## 🟢 4. Split Data into Chunks

```python
words = text.split()
```

Chunks:

* (Ram, 4GW22CS001, CSE, 8.5)
* (Ravi, 4GW22CS002, CSE, 9.1)

Reason:
LLM cannot process large data at once

---

## 🟢 5. Generate Embeddings

```python
model.encode(chunks)
```

Example:

```
"Ram 4GW22CS001 8.5"
→ [0.12, -0.45, 0.89]
```

---

## 🟢 6. Store in FAISS

```python
dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))
```

---

## 🟢 7. Question → Embedding

```python
query_embedding = create_embeddings([question])[0]
```

---

## 🟢 8. Similarity Search

```python
D, I = index.search(np.array([query_embedding]), k)
```

---

## 🟢 9. Build Context

```python
context = " ".join([chunks[i] for i in top])
```

---

## 🟢 10. Send to LLM (Ollama)

```
DATA:
(Ram, 4GW22CS001, CSE, 8.5)

QUESTION:
Show CGPA of 4GW22CS001
```

---

## 🟢 11. LLM Decision

* SQL Query OR
* Direct Answer

---

## 🟢 12. Execute SQL

```python
result = conn.execute(text(sql_query)).fetchone()
```

---

## 🟢 13. Format Response

```python
final_answer = "CGPA is 8.5"
```

---

## 🟢 14. Return to UI

```python
return jsonify({"answer": final_answer})
```

---

## 🟢 15. Save to chat_logs

```sql
INSERT INTO chat_logs (question, answer)
```

---

## 📦 requirements.txt Explanation

* flask → Backend server
* sqlalchemy → Database connection
* pymysql → MySQL driver
* faiss-cpu → Vector search
* sentence-transformers → Embeddings
* numpy → Numerical processing
* requests → API calls
* python-dotenv → Environment variables

---

## 🧠 What is NumPy?

NumPy is used for handling arrays and vectors.

Features:

* Faster than Python lists
* Used for calculations
* Required for embeddings

Example:

```
[0.12, -0.45, 0.89]
```

## 📝 Data Retrieval Methods

Your system can fetch data for LLM processing in **two ways** 

---

### 1️⃣ Single Table Join (Example: `users` + `student_academics`)

**Purpose:** Train LLM on **specific structured data** from one or two related tables.

**Code (main.py):**

```python
def get_all_data():
    with engine.connect() as conn:
        result = conn.execute(text("""
        SELECT u.name, u.usn, u.branch, sa.cgpa
        FROM users u
        JOIN student_academics sa ON u.id = sa.student_id
        """))
        rows = result.fetchall()
        return " ".join([str(r) for r in rows])
```

---

### 2️⃣ Multiple Tables (Dynamic Retrieval)

**Purpose:** Train LLM on **all relevant tables** to answer queries spanning multiple datasets.

**Code (main.py):**

```python
def get_all_data():
    all_text = ""

    tables = [
        "users",
        "student_academics",
        "student_backlogs",
        "teacher_feedback",
        "activity",
        "copyrights",
        "events",
        "gatepass",
        "internship",
        "late",
        "mini_projects",
        "participants",
        "participation"
    ]

    with engine.connect() as conn:
        for table in tables:
            try:
                result = conn.execute(text(f"SELECT * FROM {table} LIMIT 50"))
                rows = result.fetchall()

                # Convert each row to string
                table_text = f"\n--- {table.upper()} ---\n"
                table_text += " ".join([str(r) for r in rows])

                all_text += table_text

            except Exception as e:
                print(f"Skipping {table}: {e}")

    return all_text
```


### Output

| **Query Example**         | **Output Source** | **LLM Role**                      |
| ------------------------- | ----------------- | --------------------------------- |
| roadmap of Python         | LLM-generated     | Generates from training data      |
| Show detail of 4GW23CI031 | Database / RAG    | Formats/summarizes retrieved data |

