# Enterprise Local RAG Engine

A production-ready, zero-cost Retrieval-Augmented Generation (RAG) platform designed to operate entirely within a locally isolated hardware environment. The system processes complex enterprise documents, converts unstructured text into dense vector representations, and generates context-aware responses without transmitting sensitive data to external cloud services.

---

## 🚀 System Architecture

The platform follows a decoupled microservices architecture that separates the user interface, orchestration layer, data storage, and machine learning inference pipeline.

### Presentation Layer
- Built using **Streamlit**
- Provides:
  - Document ingestion interface
  - Parsing progress visualization
  - Conversational search dashboard
  - Multi-page analytics view

### Orchestration Backend
- Powered by **FastAPI**
- Handles:
  - Asynchronous document processing
  - Query parsing
  - Embedding generation workflows
  - Retrieval orchestration

### Vector Database Infrastructure
- Runs inside a containerized **Oracle Database 23ai Free** instance
- Uses native vector search capabilities
- Executes high-performance cosine similarity searches through `vector_distance`

### Local Machine Learning Layer
Managed through a local **Ollama** runtime:

| Component | Model |
|------------|--------|
| Embeddings | `nomic-embed-text` |
| Text Generation | `tinyllama` |

### Memory Optimization
- Uses Python's built-in `array` module
- Stores vectors as C-contiguous float arrays
- Reduces serialization overhead during database insertion

---

## 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| API Framework | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Database | Oracle Database 23ai Free |
| Inference Runtime | Ollama |
| Embedding Model | nomic-embed-text |
| LLM | tinyllama |
| Containerization | Docker |

---

## 📂 Project Structure

```text
local-enterprise-rag/
│
├── app/
│   ├── main.py
│   ├── ui.py
│   
│   
│   
│   
│
├── requirements.txt
└── README.md
```

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ganeshpishey/Semantic-search-engine.git
cd local-enterprise-rag
```

### 2. Start Oracle Database 23ai Container

```bash
docker run -d \
  --name local-oracle-23ai \
  -p 1521:1521 \
  -e ORACLE_PWD=YourSecurePassword123! \
  -v oracle_data:/opt/oracle/oradata \
  container-registry.oracle.com/database/free:latest
```

### 3. Install Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull tinyllama
```

### 4. Create Virtual Environment

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root directory:

```env
DB_USER=system
DB_PASSWORD=YourSecurePassword123!
DB_DSN=localhost:1521/FREEPDB1

OLLAMA_BASE_URL=http://localhost:11434
```

---

## ▶️ Running the Application

### Start FastAPI Backend

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Streamlit Frontend

```bash
streamlit run app/ui.py --server.port 8501
```

### Access the Application

Open your browser and navigate to:

```text
http://localhost:8501
```

---

## 🔄 End-to-End Execution Pipeline

```text
Document Upload
       │
       ▼
Document Parsing
       │
       ▼
Chunk Generation
       │
       ▼
Embedding Creation
(nomic-embed-text)
       │
       ▼
Oracle 23ai Vector Storage
       │
       ▼
Similarity Search
(vector_distance)
       │
       ▼
Context Retrieval
       │
       ▼
LLM Generation
(tinyllama)
       │
       ▼
Response Display
(Streamlit UI)
```

