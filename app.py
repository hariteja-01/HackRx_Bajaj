# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import utils

# --- API SETUP ---
app = FastAPI(
    title="LLM Document Processing System",
    description="Process natural language queries against policy documents."
)

class QueryRequest(BaseModel):
    query: str

# --- STARTUP EVENT ---
@app.on_event("startup")
def on_startup():
    """This function runs when the server starts."""
    print("--- Server starting up ---")
    # This is the "Ingestion" step. It loads, chunks, and indexes your documents.
    utils.chunk_and_index_documents()
    print("--- System ready ---")

# --- API ENDPOINT ---
@app.post("/process_query/")
async def process_query(request: QueryRequest):
    """
    The main endpoint to process a user's query.
    """
    try:
        print(f"\nReceived query: {request.query}")

        # 1. Structure the query using Gemini Pro
        print("Step 1: Structuring query...")
        claim_details = utils.structure_query(request.query)
        print(f"  > Structured Details: {claim_details}")

        # 2. Retrieve relevant clauses from Vector DB
        print("Step 2: Retrieving relevant clauses...")
        context_clauses = utils.retrieve_relevant_clauses(request.query, n_results=5)
        print(f"  > Found {len(context_clauses)} relevant clauses.")

        # 3. Get final decision from Gemini Pro
        print("Step 3: Synthesizing final decision...")
        decision = utils.get_final_decision(claim_details, context_clauses)
        print("  > Decision generated.")

        return decision

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse LLM JSON output. Error: {e}")
        raise HTTPException(status_code=500, detail="Error parsing response from the language model.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")