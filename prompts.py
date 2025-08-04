# prompts.py

# Prompt to extract structured data from a user's free-text query
QUERY_STRUCTURING_PROMPT = """
You are an expert at parsing and structuring user queries.
Your task is to extract key entities from the user's query and return them as a JSON object.
The possible entities are: age, gender, medical_procedure, location, and policy_duration_months.
If an entity is not mentioned, do not include it in the JSON.
The policy duration should be converted to months. For example, "3-month-old policy" is 3, "2 year policy" is 24.

Query: "{query}"

Return ONLY the JSON object.
"""


# Prompt for the final decision-making step
FINAL_ANALYSIS_PROMPT = """
You are an expert insurance claims analyst. Your task is to make a decision based STRICTLY on the provided policy clauses.

**1. Claim Details (Structured from user query):**
{claim_details}

**2. Relevant Policy Clauses (Retrieved from documents):**
{context}

**3. Your Task:**
Evaluate the claim against the provided policy clauses.
- Determine if the claim should be "Approved" or "Rejected".
- If a financial amount or coverage percentage is mentioned in the clauses, state the "amount". If not, set it to "Not Applicable".
- Provide a clear justification for your decision by referencing the specific clause(s) that apply.

**4. Response Format:**
You MUST return your response as a valid JSON object with the following structure:
{{
  "decision": "Approved" or "Rejected",
  "amount": "The calculated amount or 'Not Applicable'",
  "justification": [
    {{
      "clause_text": "The exact text of the policy clause you used.",
      "reasoning": "Your brief explanation of how this clause leads to your decision."
    }}
  ]
}}

Return ONLY the JSON object. Do not add any introductory text.
"""