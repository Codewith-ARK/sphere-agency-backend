from llm.helper import gemini_client, format_response
from llm.prompts import quote_prompt


def generate_budget(campaign):
    # prompt = f"""
    # given the campaign data. Quote an accurate budget for this campaign. The resultant output should be a decimal value in PKR. Your response should NOT include any extra commentary.
    
    # CAMPAIGN_DATA:
    # {campaign}
    
    # """

    prompt = quote_prompt(campaign_data=campaign)
    response = gemini_client(prompt)

    return format_response(response.text)


def generate_task(campaign):
    prompt = f"""
    You are an expert project manager, your task is to generate and distribute tasks among employees given their skills, and current workload. Given the campaign data. You are to generate 5 tasks that are required to complete this campaign successfully. These tasks are going to be performed by the employees of the agency.
    
    CAMPAIGN and EMPLOYEE DATA:
    {campaign}
    

     Expected Output (strict JSON array of objects, no commentary, no markdown):
    {{
        "title":"task title",
        "priority":"high | medium | low" <lowercase values>,
        "hours_required": "numbers of hours required to perform this task",
        "objective":"a short description of what to achieve in this task. should be less than 240 characters. should be simple to understand and comprehend"
        "assigned_to":<id of employee>
    }}
    
    INSTRUCTIONS:
    - Output should be valid JSON response.
    - Do NOT provide any additional commentary.
    - Make sure to use your prior knowledge and think about this task, before generating tasks.
    """

    response = gemini_client(prompt)

    if response.text:
        return response.text

    else:
        return response

def generate_and_save_tasks(campaign, employees):
    import json
    from rest_framework.exceptions import ValidationError
    from tasks.serializers import TaskSerializer

    structured = {
        "id": campaign.id,
        "title": campaign.title,
        "campaignType": campaign.type,
        "platform": campaign.platform,
        "duration": f"{campaign.duration} Days",
        "employees": list(employees),
    }

    try:
        response = generate_task(structured)
        tasks = json.loads(response)  # might fail if LLM gives invalid JSON
    except Exception as e:
        print(f"Task generation failed for campaign {campaign.id}: {e}")
        return  # don't approve campaign, just exit

    # attach campaign ID
    for t in tasks:
        t["campaign"] = campaign.id

    try:
        serializer = TaskSerializer(data=tasks, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        print(f"Task saving failed for campaign {campaign.id}: {e}")
        return  # again, don’t update campaign status

    # ✅ Only if everything succeeded
    campaign.status = "approved"
    campaign.save()
    
    
from django.db import transaction
from llm.helper import format_response
from llm.prompts import contract_prompt, contract_prompt_v2
from .models import Contract, Campaign
from .serializers import ClauseSerializer
from rest_framework.exceptions import ValidationError

@transaction.atomic
def generate_and_save_contract(campaign_data, client_info):
    try:
        response = gemini_client(contract_prompt_v2(campaign_data, client_info))    
        clauses = format_response(response.text)
    except Exception as e:
        print(f"LLM/formatting failed for campaign {campaign_data['id']}: {e}")
        return

    campaign = Campaign.objects.get(id=campaign_data["id"])
    contract = Contract.objects.create(campaign=campaign)

    for c in clauses:
        c["contract"] = contract.id

    try:
        serializer = ClauseSerializer(data=clauses, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    except ValidationError as e:
        print(f"Clause saving failed for campaign {campaign.id}: {e}")
        return


