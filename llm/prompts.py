import json

def contract_prompt(campaign):
    return f"""
        You are a clause-writing assistant for a digital marketing agency. Based on the client's submitted campaign, your job is to generate a clear, professional clauses in structured JSON format.

       Additional Notes:
        - for payments use PKR (Pakistani Rupees)
        - you MUST follow the clause structure provided below.
        
        Contract MUST include the following:
        - 5 structured clauses. Each clause should have: 
        (
            title,
            
            text: A formal legal-style clause. Clause should reflect formal legal language, using appropriately complex and professional terminology. Example: "In the event of a material breach of the obligations herein, the non-breaching party shall be entitled to pursue equitable relief, including but not limited to specific performance or injunctive relief, in addition to any pecuniary damages arising from such breach, as adjudicated by a court of competent jurisdiction.,

            explanation: A plain-English, clear and simplified explanation of the clause ensuring non-legal users can grasp the intent of each section.
        )
        Clauses:

        - Campaign Overview:
        - - Company Name: ...
        - - Campaign Type: ...
        - - Platform: ...


        - Scope of Work:
        - - [Short bullet points describing deliverables]
        - - [Example: 8 short-form videos for Instagram per month]
        
        - Payment Terms

        - Timeline:
        
        - Penalty terms (in case of):
        - - Breach of contract
        - - Late Delivery
        - - Non-Compliance
        
        Campaign Data:
        {json.dumps(campaign)}
        
        The output should be a VALID JSON array of clauses.
        Do not wrap the result in any object. 
        The format should be:

        [
        {{ "title": "...", "text": "...", "explanation": "..." }},
        {{ "title": "...", "text": "...", "explanation": "..." }}
        ]
    """

def contract_prompt_v2(campaign):
    return f"""
You are a Contract Clause Writing Assistant for a digital marketing agency.
Your task is to generate a complete and well-structured JSON array containing formal, legally styled clauses for a marketing services contract.

Each clause must follow the structure, tone, and formatting rules described below.

🧩 Output Format

Return a VALID JSON array, containing exactly the following structure:

[
  {{
    "title": "",
    "text": "",
    "explanation": ""
  }}
]


Do not wrap the result in any other object, markdown formatting, or text commentary.
All values must be in PKR (Pakistani Rupees) where applicable.

Clause Structure Requirements
Each clause must contain:
title → the clause title.
text → a formal legal-style clause, using professional contract language.

Example tone:
“In the event of a material breach of the obligations herein, the non-breaching party shall be entitled to pursue equitable relief, including but not limited to specific performance or injunctive relief, in addition to any pecuniary damages arising from such breach, as adjudicated by a court of competent jurisdiction.”

explanation → a plain-English, reasoning-based explanation describing why this clause or choice was made, and what alternatives were considered or rejected, instead of a simple “what this means” summary.

Clauses to Include
You must generate the following 9 primary clauses, plus 4 additional legal clauses, for a total of 13 structured clauses:

Campaign Overview
Company Name
Campaign Type
Platform
Scope of Work

Include hour breakdown per task category, e.g., Strategy 10 hrs, Content 22 hrs.
Reflect realistic workload distribution.

Payment Terms
Include reasoning behind 50% advance payment choice.
Mention alternatives rejected (30%, 100%) and why.

Timeline
Justify duration chosen.
Show cost of extending (e.g., +PKR 6,400/month).
Confidentiality

Use a specific 2-year term for confidentiality obligations.

Intellectual Property (IP) Rights
Compare cost difference between exclusive vs. shared rights (e.g., exclusive = 40% higher).

Termination
Justify 30-day notice period based on project length.
Reference relevant provisions from Pakistan Contract Act.

Liability
Discuss cost impact if unlimited liability were chosen (60–80% higher).

Dispute Resolution
Compare arbitration vs. court in terms of time and cost implications.

Governing Law & Jurisdiction
Specify that the contract is governed by Pakistani law and handled in local jurisdiction.

Force Majeure
Include standard legal protection for unforeseen events (e.g., natural disasters, political instability).

Amendments & Modifications
Define process for written mutual consent before altering the agreement.

Entire Agreement Clause
State that this document represents the entire agreement and supersedes prior understandings.

Reasoning-Driven Explanations (XAI Style)

For each explanation:

Replace plain summaries with why this approach was chosen and what alternatives cost or imply.

Example:

“We selected a 50% advance to balance client commitment with agency risk exposure. A 30% deposit was rejected due to higher upfront content costs, while a 100% prepayment was deemed commercially unrealistic for client onboarding.”

Data and Accuracy Constraints

Do NOT hallucinate or invent financial, legal, or campaign data not found in the provided campaign JSON.

If necessary data is missing but reasonable interpolation is possible, you may:

Use the provided campaign data (e.g., price = 75,000 PKR).

Apply one standard assumption only (e.g., a typical 15% tax rate in Pakistan).

State assumptions transparently in the explanation.

Never fabricate names, figures, or entities.

Campaign Data

Use the provided campaign data below to contextualize clauses:

{json.dumps(campaign)}

Final Instruction

Generate 13 structured clauses (in JSON format) reflecting:
Formal, contract-grade tone in text.
Explainable, decision-oriented tone in explanation.
Consistent structure, accurate financial details, and transparent logic.

Return only the JSON array as output.
    """

def quote_prompt(campaign_data, hourly_rate=800):
        return f"""
        You are a quoting assistant for a digital marketing agency. Based on the input campaign data, estimate the financial breakdown and generate a professional justification to help the client understand the pricing.

        The pricing is based on a flat hourly rate of Rs. {hourly_rate}/hour. You must calculate the total cost using this formula:
        - total_cost = estimated_hours * hourly_rate
        - advance_payment = total_cost * (advance_percent / 100)
        - remaining_balance = total_cost - advance_payment

        Generate your output in **valid JSON** with two fields:

        1. "finance_data" — includes:
            - estimated_hours (integer)
            - hourly_rate (always Rs. 800)
            - total_cost (float with 2 decimals)
            - advance_percent (float with 2 decimals)
            - advance_payment (float with 2 decimals)
            - remaining_balance (float with 2 decimals)

        2. "justification" — a short, client-facing explanation (in plain English) of how the pricing was calculated, including a time estimate and value rationale.

        Here is the campaign data:

        {json.dumps(campaign_data, indent=2)}

        Now return the JSON:
        {{
            "data": {{ ... }},
            "justification": "..."
        }}

        Only return the JSON. Do not include any commentary or Markdown.
    """
