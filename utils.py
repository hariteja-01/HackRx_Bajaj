# utils.py
import os
import glob
import json
from typing import List, Dict

import google.generativeai as genai
from dotenv import load_dotenv

import chromadb
from chromadb.utils import embedding_functions

import pypdf
import docx

from prompts import QUERY_STRUCTURING_PROMPT, FINAL_ANALYSIS_PROMPT

# --- CONFIGURATION ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DOCUMENTS_DIR = "documents"
VECTOR_STORE_DIR = "vector_store"
CHROMA_COLLECTION = "policy_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- INITIALIZATION ---
# Initialize ChromaDB client and embedding function
# This setup is fast and runs locally
client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"}
)

# Initialize Gemini Pro model
# This is the new, correct line
llm = genai.GenerativeModel('models/gemini-1.5-flash-latest')


# --- DOCUMENT PROCESSING ---
def load_documents() -> List[str]:
    """Loads and extracts text from PDF and DOCX files in the documents directory."""
    print("Loading documents...")
    texts = []
    # Load PDFs
    for pdf_path in glob.glob(os.path.join(DOCUMENTS_DIR, "*.pdf")):
        print(f"  - Reading {os.path.basename(pdf_path)}")
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                texts.append(page.extract_text())
    # Load DOCX
    for docx_path in glob.glob(os.path.join(DOCUMENTS_DIR, "*.docx")):
        print(f"  - Reading {os.path.basename(docx_path)}")
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            if para.text:
                texts.append(para.text)
    return texts

def chunk_and_index_documents():
    """Chunks documents and stores them in the vector database."""
    if collection.count() > 0:
        print("Documents are already indexed. Skipping.")
        return

    docs = load_documents()
    if not docs:
        print("No documents found to index.")
        return

    # Simple chunking: Join all text and split by paragraphs
    full_text = "\n".join(docs)
    chunks = [chunk for chunk in full_text.split('\n\n') if chunk.strip()]

    print(f"Indexing {len(chunks)} document chunks...")
    collection.add(
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )
    print("Indexing complete!")


# --- LLM AND RETRIEVAL LOGIC ---
def structure_query(query: str) -> Dict:
    """Uses LLM to convert a natural language query to a structured JSON."""
    prompt = QUERY_STRUCTURING_PROMPT.format(query=query)
    response = llm.generate_content(prompt)
    # Clean up the response to get a valid JSON string
    json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(json_string)

def retrieve_relevant_clauses(query: str, n_results: int = 5) -> List[str]:
    """Searches the vector database for clauses relevant to the query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]

def get_final_decision(claim_details: Dict, context: List[str]) -> Dict:
    """Uses LLM to make a final decision based on claim and context."""
    import json
    prompt = FINAL_ANALYSIS_PROMPT.format(
        claim_details=json.dumps(claim_details, indent=2),
        context="\n- ".join(context)
    )
    response = llm.generate_content(prompt)
    # Clean up the response to get a valid JSON string
    json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(json_string)