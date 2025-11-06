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

def contract_prompt_v2(campaign, client_info):
    return f"""
        You are a Contract Clause Writing Assistant for a digital marketing agency.
        Your task is to generate a complete and well-structured JSON array containing formal, legally styled clauses for a marketing services contract.

        Each clause must follow the structure, tone, and formatting rules described below.

        - Output Format:
            Return a VALID JSON array, containing exactly the following structure:

            [
            {{
                "title": "",
                "text": "",
                "explanation": ""
            }}
            ]


        Do not wrap the result in any other object, markdown formatting, or text commentary. All values must be in PKR (Pakistani Rupees) where applicable.

        Clause Structure Requirements
        - Each clause must contain:
        - - title → the clause title.
        - - text → a formal legal-style clause, using professional contract language.

        Example tone:
        - “In the event of a material breach of the obligations herein, the non-breaching party shall be entitled to pursue equitable relief, including but not limited to specific performance or injunctive relief, in addition to any pecuniary damages arising from such breach, as adjudicated by a court of competent jurisdiction.”

        - explanation → a plain-English, reasoning-based explanation describing why this clause or choice was made, and what alternatives were considered or rejected, instead of a simple “what this means” summary.

        - - Clauses to Include
        You must generate the following 9 primary clauses, plus 4 additional legal clauses, for a total of 13 structured clauses:

        - Campaign Overview
        - - Campaign Type
        - - Platform

        - Scope of Work (SNIPPET REPLACEMENT)

        - INSTRUCTION FOR "text" FIELD:
        - The "text" value for the Scope of Work clause must be strictly formal legal wording only — no numeric hour breakdowns, no task-hour lists, and no platform-specific hour entries.
        - The clause should state, in formal contract language, the agency's obligation to provide the services described in the campaign and to deliver the listed deliverables (optionally referencing an appendix or schedule for detailed deliverables).
        - Example style: "The Agency shall provide digital marketing services as described in this Agreement and as further detailed in Schedule A (Deliverables). The Agency shall perform such services with reasonable skill, care and in accordance with industry standards. Specific task allocations, time estimates, and resource breakdowns are set forth in the Explanation accompanying this clause."

        - INSTRUCTION FOR "explanation" FIELD:
        - All **detailed hour breakdowns** go here. The explanation must:
            1. Provide a clear **hour-per-task-category** breakdown (e.g., Strategy: 10 hrs; Content creation — video: 22 hrs; Content creation — static: 15 hrs; Campaign setup: YouTube Search Ads: 8 hrs; Instagram Ads: 5 hrs; Reporting & optimization: X hrs, etc.).
            2. **Justify** each number with reasoning: explain why a given platform or content type requires more or less time (e.g., YouTube Search Ads require more setup because of keyword research, ad groups, bidding configuration and video asset formatting; Instagram requires simpler targeting and fewer technical settings).
            3. **Compare chosen platform(s) with alternatives** so clients understand trade-offs — explicitly state an example comparison such as: "YouTube Search Ads setup: 8 hrs vs. Instagram Ads setup: 5 hrs — difference driven by targeting complexity and creative asset prep."
            4. Show **task-level distinctions** (for example: pre-production planning, filming/creation, editing, review rounds, ad setup, and optimization) and allocate hours to each where appropriate.
            5. When applicable, show **why content formats differ** (e.g., video editing and post-production typically consume 22 hrs due to scripting, shoots, multi-stage editing and revisions; static image creative requires ~15 hrs due to concept, design and fewer revision cycles).
            6. If an item is extrapolated from campaign data (e.g., price = 75,000 PKR present in campaign JSON), the explanation may calculate time-based costings or per-hour cost impacts — but must **explicitly state any assumptions** (for example: "Assuming agency billing at PKR X/hr — assumption stated because hourly rate not in campaign data").
            7. Make the explanation **decision-focused (XAI style)**: explain why these hour splits were chosen, which alternatives were considered (e.g., concentrated monthly burst vs. steady weekly cadence), and what the time/cost implications of those alternatives would be.
            8. Do **not** invent precise technical details or platform specs not present in the campaign JSON. If necessary data is missing but a reasonable interpolation can be made, state the interpolation clearly and use **only one standard assumption** (e.g., a single standard hourly rate or a standard tax rate if relevant), and show the math in the explanation.
            9. The resultant output should be a textual based response. No markdown, HTML, special characters intended to format the text in any should be provided.

        - FORMAT RULES:
        - The "text" must remain a single-paragraph legal clause (no bullet hour lists).
        - The "explanation" may use short bullet points or a small JSON-like object inside the explanation string to present the hour breakdown neatly, but must remain plain-English and transparent about assumptions.
        - Example brief mapping inside explanation (illustrative only — adapt to campaign data):
            - Strategy: 10 hrs — reason: campaign planning, audience research.
            - Video Content: 22 hrs — reason: scripting, shoot coordination, editing, revisions.
            - Static Content: 15 hrs — reason: concept + design + 2 review rounds.
            - Platform Setup: YouTube Search Ads: 8 hrs vs Instagram Ads: 5 hrs — reason: targeting complexity & asset requirements.

        - ACCURACY / NO-HALLUCINATION:
        - Do not fabricate hourly rates, tax percentages, or platform metrics that are not derivable from the campaign JSON.
        - If the campaign JSON lacks necessary inputs (e.g., hourly rate), the explanation may propose one **clearly-stated** assumption and use it consistently — but must label it as an assumption.

        - XAI EMPHASIS:
        - The explanation must explicitly show the decision process: "We chose X hours because A, B, C; alternative Y was rejected because D; cost/time tradeoff is E."
        - Where platform differences exist, provide at least one concrete comparative sentence so the client can see why time allocation differs by platform and content type (use the YouTube vs Instagram and video vs static examples as templates).

        - Payment Terms
        - - Include reasoning behind 50% advance payment choice.
        - - Mention alternatives rejected (30%, 100%) and why.

        - Timeline
        - - Justify duration chosen.
        - - Show cost of extending (e.g., +PKR 6,400/month).

        - Confidentiality
        Use a specific 2-year term for confidentiality obligations.

        - Intellectual Property (IP) Rights
        Compare cost difference between exclusive vs. shared rights (e.g., exclusive = 40% higher).

        - Termination
        - - Justify 30-day notice period based on project length.
        - - Reference relevant provisions from Pakistan Contract Act.

        - Liability
        - - Discuss cost impact if unlimited liability were chosen (60–80% higher).

        - Dispute Resolution
        - - Compare arbitration vs. court in terms of time and cost implications.

        - Governing Law & Jurisdiction
        - - Specify that the contract is governed by Pakistani law and handled in local jurisdiction.

        - - Force Majeure
        - Include standard legal protection for unforeseen events (e.g., natural disasters, political instability).

        - Amendments & Modifications
        - - Define process for written mutual consent before altering the agreement.

        - Entire Agreement Clause
        - - State that this document represents the entire agreement and supersedes prior understandings.

        Reasoning-Driven Explanations (XAI Style)

        For each explanation: Replace plain summaries with why this approach was chosen and what alternatives cost or imply.

        Example:

        “We selected a 50% advance to balance client commitment with agency risk exposure. A 30% deposit was rejected due to higher upfront content costs, while a 100% prepayment was deemed commercially unrealistic for client onboarding.”

        Data and Accuracy Constraints

        - Do NOT hallucinate or invent financial, legal, or campaign data not found in the provided campaign JSON.
        - If necessary data is missing but reasonable interpolation is possible, you may:
        - Use the provided campaign data (e.g., price = 75,000 PKR).
        - Apply one standard assumption only (e.g., a typical 15% tax rate in Pakistan).
        - State assumptions transparently in the explanation.
        - Never fabricate names, figures, or entities.

        Campaign Data

        Use the provided campaign data below to contextualize clauses:

        {json.dumps(campaign)}
        
        Party One (for context):
        name: Agency Sphere
        location: Pakistan
        CEO: Rafique Bijoro
        
        Party Two - Client/Agency:
        {client_info}

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
