import streamlit as st
import requests
from pypdf import PdfReader

st.set_page_config(page_title="Local RAG Engine", layout="wide")
st.title("🧠 Local Enterprise Retrieval-Augmented Generation (RAG) System")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("📥 Knowledge Ingestion Portal")
    
    ingest_mode = st.radio("Select Ingestion Input Mode:", ["Manual Text Chunk", "Batch PDF Document Upload"])
    
    if ingest_mode == "Manual Text Chunk":
        text_input = st.text_area("Add raw documentation context chunk:", height=200)
        if st.button("Commit Text Chunk", use_container_width=True):
            if not text_input.strip():
                st.error("Text block cannot be empty.")
            else:
                with st.spinner("Embedding and storing context..."):
                    try:
                        response = requests.post(f"http://127.0.0.1:8000/ingest?content={requests.utils.quote(text_input)}")
                        if response.status_code == 200:
                            st.success("Context successfully committed to Oracle 23ai.")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Backend offline: {str(e)}")
                        
    else:
        uploaded_file = st.file_uploader("Upload an enterprise PDF manual or report:", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Execute Batch Processing & Ingestion", use_container_width=True):
                with st.spinner("Extracting, chunking, and index-routing data..."):
                    try:
                        pdf_reader = PdfReader(uploaded_file)
                        raw_text_pool = ""
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                raw_text_pool += page_text + "\n"
                        
                        if not raw_text_pool.strip():
                            st.error("Failed to extract readable text characters from this file format.")
                        else:
                            chunk_size = 500
                            overlap = 50
                            chunks = []
                            
                            for i in range(0, len(raw_text_pool), chunk_size - overlap):
                                chunk = raw_text_pool[i:i + chunk_size]
                                if chunk.strip():
                                    chunks.append(chunk)
                            
                            st.write(f"📊 Document translated into **{len(chunks)}** optimized text matrices.")
                            
                            success_count = 0
                            progress_bar = st.progress(0)
                            
                            # Stream directly with optimized resource management
                            for idx, text_block in enumerate(chunks):
                                res = requests.post(f"http://127.0.0.1:8000/ingest?content={requests.utils.quote(text_block)}")
                                if res.status_code == 200:
                                    success_count += 1
                                progress_bar.progress((idx + 1) / len(chunks))
                                
                            st.success(f"Successfully processed and committed {success_count}/{len(chunks)} nodes to Oracle 23ai.")
                    except Exception as e:
                        st.error(f"Ingestion pipeline execution failure: {str(e)}")

    st.markdown("### 🛠️ System Maintenance Operations")
    if st.button("🔥 Purge Database Tablespace", use_container_width=True, type="secondary"):
        with st.spinner("Executing structural TRUNCATE command inside Oracle container..."):
            try:
                response = requests.post("http://127.0.0.1:8000/reset")
                if response.status_code == 200:
                    st.success("Tablespace completely evicted. Database is clean and ready for fresh ingestion maps.")
                else:
                    st.error(f"Purge operation rejected: {response.text}")
            except Exception as e:
                st.error(f"Connection failure to backend database driver: {str(e)}")

with col2:
    st.header("💬 Contextual AI Assistant & Search")
    query_input = st.text_input("Ask a question based strictly on your data:")
    limit_slider = st.slider("Max Match Constraints:", min_value=1, max_value=5, value=3)
    
    if st.button("Query Complete Pipeline", use_container_width=True):
        if not query_input.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Processing pipeline..."):
                try:
                    response = requests.get(f"http://127.0.0.1:8000/query_rag?query={requests.utils.quote(query_input)}&limit={limit_slider}")
                    if response.status_code == 200:
                        results = response.json()
                        
                        st.markdown("### 🤖 Synthesized AI Response (RAG):")
                        st.chat_message("assistant").write(results["ai_response"])
                        st.markdown("---")
                        
                        st.markdown("### 🔍 Raw Database Match Classes:")
                        if not results["matches"]:
                            st.warning("Zero context returns matched this structural query configuration.")
                        else:
                            for idx, match in enumerate(results["matches"]):
                                with st.container(border=True):
                                    st.write(f"**Match #{idx+1}**")
                                    st.info(match["chunk"])
                                    st.metric(label="Cosine Distance Metric (Lower = Better)", value=f"{match['cosine_distance']:.5f}")
                    else:
                        st.error(f"Pipeline Execution Error: {response.text}")
                except Exception as e:
                    st.error(f"Backend offline: {str(e)}")