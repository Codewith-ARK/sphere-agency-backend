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
