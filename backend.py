from fastapi import FastAPI
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import os
from graphQL import GraphqlClient
from model import Openai_model
from query_match import  keyword_match #, find_matching_query
import ast
import os

# Load `.env` only in local development
if os.getenv("RENDER") is None:  # Render automatically sets 'RENDER' in hosted env
    load_dotenv()

HASURA_GRAPHQL_URL = os.getenv("HASURA_GRAPHQL_URL")
HASURA_ADMIN_SECRET = os.getenv("HASURA_ADMIN_SECRET")
HASURA_ROLE = os.getenv("HASURA_ROLE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str
    user_role: str|None = None


app=FastAPI()

graphql_client = GraphqlClient(HASURA_GRAPHQL_URL,HASURA_ADMIN_SECRET,HASURA_ROLE)
Openai_client = Openai_model(OPENAI_API_KEY)


def store_data(updates):
    file_path = "output_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

                if not isinstance(data, list):
                    data = [data]
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    
    data.append(updates)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/")
def home(): 
    return {"Response": "Connection Successful"}


@app.post("/chat")
def chat(request:ChatRequest):
    print("chat")
    message=request.message
    role=request.user_role
    role=role.replace("_"," ").title()
    with open("queries.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if message.replace(" ","_") in data['queries']:
        query=data['queries'][message]['query'].replace("\n"," ").replace("\\","")
    
    # elif "order" in message.lower():
    #     query="query { bloodorderview { request_id first_name last_name blood_group status } }"
    
    elif "bill" in message.lower():
        query="query { costandbillingview { company_name month overall_blood_unit total_cost total_patient } }"
    
    elif "cost" in message.lower():
        query="query { costandbillingview { blood_component company_name total_cost } }"
    elif "report" in message.lower():
        query="query { costandbillingview { company_name blood_component total_cost overall_blood_unit } }"
    elif "hi" in message.lower() or "hello" in message.lower() or "hey" in message.lower():
        return {'Response': f"Hello,{role} How can I help you today?"}
    else:
        # query=data.get(keyword_match(message),[])
        # query=data.get(find_matching_query(message),[])
        query= Openai_client.graphql_query_generate(message)
        
        if not query or query=="Unknown":
            return {'Response': "Sorry, I don't have enough information to answer that question."}

    data = graphql_client.execute_graphql_query(query)

    if data is  None:
        return {'Response':"Sorry, something went wrong in query execution."}  
     
    response_obj = Openai_client.generate_response(data,message,role)
    # print(response['suggested_actions'])
    suggested_actions=response_obj["suggested_actions"]
    response=response_obj["response"]
    

    updates = {
        "message": message,
        "query":query,
        "data": data,
        "response": response,
        "suggested_actions": suggested_actions
    }
    store_data(updates)
    
    return {"Response": response, "suggested_actions": suggested_actions}



