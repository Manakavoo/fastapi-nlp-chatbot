import requests
import ast

# GraphQL endpoint URL

# HASURA_GRAPHQL_URL = "https://internals.inhlth.app/hasura/v1/graphql"
# HASURA_ADMIN_SECRET = "xo6fSNmltkYvNj1OIRNi27hzIwtW+brpSNJZ+JZxk/4="
# HASURA_USER="dataops"

# HASURA_GRAPHQL_URL="http://localhost:8080/v1/graphql"
# HASURA_ADMIN_SECRET="adminsecretkey"
# HASURA_USER="user"

# HASURA_HEADERS = {
#     "Content-Type": "application/json",
#     "x-hasura-admin-secret": HASURA_ADMIN_SECRET,
#     "x-hasura-role" : HASURA_USER
# }

class GraphqlClient:
    def __init__(self,HASURA_GRAPHQL_URL,HASURA_ADMIN_SECRET,HASURA_ROLE="user"):
        self.HASURA_GRAPHQL_URL = HASURA_GRAPHQL_URL
        self.HASURA_ADMIN_SECRET = HASURA_ADMIN_SECRET
        self.HASURA_HEADERS = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": self.HASURA_ADMIN_SECRET,
            "x-hasura-role" : HASURA_ROLE
        }

    def execute_graphql_query(self,query, variables=None):
        print("execute_graphql_query")
        query=query.replace("\n", " ")
        try:
            response = requests.post(self.HASURA_GRAPHQL_URL, json={"query": query, "variables": variables}, headers=self.HASURA_HEADERS)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"GraphQL query failed: {str(e)}")
            return None



# ggl = GraphqlClient("http://localhost:8080/v1/graphql","adminsecretkey")

# query ="query GetCompletedOrders {\n  bloodorderview(\n    where: { status: { _eq: \"CMP\" } }\n  ) {\n    request_id\n    first_name\n    last_name\n    blood_group\n    status\n    blood_bank_name\n  }\n}"

# # query = ast.literal_eval(f'"{query}"')
# data_response=ggl.execute_graphql_query(query)

# print(data_response)



