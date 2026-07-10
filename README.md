# Enterprise Local RAG Engine

A production-ready, zero-cost Retrieval-Augmented Generation (RAG) platform designed to operate completely within a locally isolated hardware environment. The system processes complex enterprise documents, converts unstructured text into multi-dimensional dense vector spaces, and generates context-grounded responses without transmitting sensitive data to external cloud networks.

## 🚀 System Architecture Overview

The platform uses a decoupled microservices blueprint to separate the user interface, routing logic, data layer, and machine learning inference pipeline:

* **Presentation Layer:** Built with **Streamlit** to provide a multi-page analytical dashboard for document ingestion, parsing progress visualization, and conversational search.
* **Orchestration Backend:** Powered by **FastAPI** to handle asynchronous document pipelines, query parsing, and embedding generation management.
* **Vector Database Infrastructure:** Run inside a containerized **Oracle Database 23ai Free** instance, utilizing native kernel-level `vector_distance` operations to execute rapid cosine similarity calculations.
* **Local Machine Learning Nodes:** Orchestrated via an isolated **Ollama** daemon, utilizing `nomic-embed-text` for 768-dimensional vector mappings and `tinyllama` for text synthesis.
* **Memory & I/O Optimization:** Implements C-contiguous float arrays via Python's standard `array` module to eliminate application-level serialization overhead during database insertions.

---

## 🛠️ Technical Stack

* **Language:** Python 3.10+
* **API Framework:** FastAPI, Uvicorn
* **Frontend UI:** Streamlit
* **Database Engine:** Oracle Database 23ai Free (Docker Container)
* **Inference Host:** Ollama Client Runtime
* **Models Utilized:** `nomic-embed-text` (Embeddings), `tinyllama` (LLM)

---

## 🔧 Installation & Local Setup

Run the following commands sequentially in your terminal window to initialize the complete infrastructure ecosystem:

```bash
# 1. Clone the Codebase
git clone [https://github.com/YOUR_GITHUB_USERNAME/local-enterprise-rag.git](https://github.com/YOUR_GITHUB_USERNAME/local-enterprise-rag.git)
cd local-enterprise-rag

# 2. Spin Up the Oracle 23ai Vector Database Container
docker run -d --name local-oracle-23ai -p 1521:1521 -e ORACLE_PWD=YourSecurePassword123! -v oracle_data:/opt/oracle/oradata [container-registry.oracle.com/database/free:latest](https://container-registry.oracle.com/database/free:latest)

# 3. Initialize Ollama and Download Models
ollama pull nomic-embed-text
ollama pull tinyllama

# 4. Configure Virtual Environment and Dependencies
python -m venv venv
# Note: On Windows use .\venv\Scripts\Activate.ps1 to open
source venv/bin/activate
pip install -r requirements.txt

### 5. Configure Environment Variables
Create a file named .env inside your repository root folder:

DB_USER=system
DB_PASSWORD=YourSecurePassword123!
DB_DSN=localhost:1521/FREEPDB1
OLLAMA_BASE_URL=http://localhost:11434


---

## Execution Pipeline

To run the application, spin up the backend API layer and the frontend client interface in separate terminal sessions:

Start the FastAPI Backend Service:
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

Start the Streamlit Presentation Interface:
streamlit run app/ui.py --server.port 8501

Open your web browser and navigate to http://localhost:8501 to use the application.
