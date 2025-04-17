from openai import OpenAI
import os
import json
from prompt import  generate_graphql_prompt

class Openai_model:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)   
        self.model="gpt-4o-mini"

    def generate_response(self, data,user_message,role=None): 
        # prompt="""You are an AI assistant responding to user queries based on retrieved database data. Format your response as a short and natural chat reply.
            
        #     Role: {role}
        #     User Question: {user_message}
        #     Relevant Data: {data}
        #     Formatting Guidelines:
        #     Keep the response concise and precise.
        #     Directly answer the question without unnecessary details.
        #     Maintain a natural, conversational tone, like a chat message from the user.
        #     Use a clear and easy-to-understand format, including tables, charts, or visuals when appropriate.
        #     use a proper format in numbers and calculation when required with a flow.
        #     Avoid introductory phrases like "Based on the data" or "According to the information."
        #     If the data does not contain the answer, politely state that the information is unavailable rather than guessing.
        #     suggested actions are only for assistant role.

            
        #     Note: the suggested actions are only for assistant role and not for user 
        #     Mandandory: Make sure the suggested action should be related to the question and importantly that can be answer using the data.

        #     Show corresponding status name instead of status code in the response.
        #     For your reference status code and name:
        #      BBA-blood_bank_assinged , PA-pending, CMP -completed ,REJ-rejected ,AA-agent assigned , BA-blood arrival, BP-blood sample pickup,PP-pending pickup , BSP-blood sample pickup, CAL-Cancel

             
        #     Output format:
        #     {{
        #     "response": "Your response here",
        #     "suggested_actions": ["Action 1", "Action 2"]
        #     }}
            
        #     """ 
        
        prompt ="""You are an AI assistant responding to user queries based on retrieved database data. Format your response as a short and natural chat reply.
            
            Role: {role}
            User Question: {user_message}
            Relevant Data: {data}
            Formatting Guidelines:
            Keep the response concise and precise.
            Directly answer the question without unnecessary details.
            Maintain a natural, conversational tone, like a chat message from the user.
            Use a clear and easy-to-understand format, including tables, charts, or visuals when appropriate.
            use a proper format in numbers and calculation when required with a flow.
            Avoid introductory phrases like "Based on the data" or "According to the information."
            If the data does not contain the answer, politely state that the information is unavailable rather than guessing.
 
            Mandandory: Make sure the suggested action should be related to the question and importantly that can be answer using the data.

            Show corresponding status name instead of status code in the response.
            For your reference status code and name:
             BBA-blood_bank_assinged , PA-pending, CMP -completed ,REJ-rejected ,AA-agent assigned , BA-blood arrival, BP-blood sample pickup,PP-pending pickup , BSP-blood sample pickup, CAL-Cancel
            
            Actions for bloodorderview:

            Check order status (by request_id)
            Filter orders (by blood_group, blood_bank_name)
            View pending (PA)
            completed (CMP)
            rejected (REJ) orders
            Find orders in a date range
            Get agent-assigned (AA) orders
            Count orders by blood bank

            Actions for costandbillingview:

            View total cost & blood usage (by company_id)
            Check cost by month
            List company billing (company_name, total_cost)
            Find cost by blood component
            Get total patients per company
            Compare company costs
            Find most-used blood component
            Calculate avg. 
            cost per blood unit
            Generate company billing report
            
            suggest  relevant two actions only from the above actions 
            use direct values in actions based on the data provided.

            Output format:
            {{
            "response": "Your response here",
            "suggested_actions": ["Action 1", "Action 2"]
            }}
            
"""
        
        prompt = prompt.format(role=role,user_message=user_message, data=data)

        response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                )
        json_response = json.loads(response.choices[0].message.content)
        response_obj = {
            "response": json_response["response"],
            "suggested_actions": json_response.get("suggested_actions", [])
        }

        return response_obj
    
    
    def intent_classification(self,user_message="what is the order status?"):
        
        intent_list=['All_Orders', 'Order_Status', 'Pending_Orders', 'Approved_Orders', 'Rejected_Orders', 'Orders_By_Blood_Type',
                'Orders_By_BloodBank', 'Orders_By_Status_And_BloodBank', 'Total_Orders_By_BloodBank', 'Billing_Overview', 'Billing_By_Company',
                'Cost_By_Blood_Component', 'Total_Patients_By_Company', 'Blood_Usage_By_Company', 'Recent_Orders', 'Bye', 'Hello', 'Unknown']

        prompt = f"""You are an assistant for a blood bank order portal. Extract the intent and entities from the following query.

            Output ONLY a JSON object with the following structure:
            {{
            "intent": [one of: {intent_list}],
            "entities": {{
                "order_id": "extracted order ID or null",
                "blood_type": "extracted blood type or null",
                "date_range": "extracted date range or null",
                "hospital_id": "extracted hospital reference or null"
            }}
            }}"""
        
        response = self.client.chat.completions.create(
                        model=self.model,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "user message"+user_message}
                    ],
                )
        intent=json.loads(response.choices[0].message.content)

        return intent
            
        # return intent
    
    def graphql_query_generate(self,user_message="what are the approved orders?"):
        prompt="""you are assistant to generate a relevant graphql query based on user query.
        only use the mentioned fields and tables name with a correct format mentioned to generate the graphql query
        Input: user query

        Tables: bloodorderview , costandbillingview
        bloodorderview {
        request_id
        first_name
        last_name
        blood_group is one of[AB- ,O-, A+ ,B+ ,AB+ ,O+, A- ,B-]
        status  is one of [BBA , PA , CMP  ,REJ ,AA  , BA , BP  ,PP , BSP , CAL]
        blood_bank_name 
        }
        costandbillingview {
        blood_component
        company_id
        company_name
        month
        overall_blood_unit
        total_cost
        total_patient
        } 

        for your reference:
            status BBA-blood_bank_assinged , PA-pending, CMP -completed ,REJ-rejected ,AA-agent assigned , BA-blood arrival, BP-blood sample pickup,PP-pending pickup , BSP-blood sample pickup, CAL-Cancel
        
        Output ONLY a JSON object with the following structure:
        {
        "query": [graphql query]
        }
        """
       
        response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": generate_graphql_prompt},
                        {"role": "user", "content": "user message"+user_message},
                    ],
                )
        
        try:
            data=json.loads(response.choices[0].message.content)
        # print(data)
            return data['query']
        except:
            return response.choices[0].message.content



print("model loaded")