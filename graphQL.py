import requests

# GraphQL endpoint URL

HASURA_GRAPHQL_URL = "https://internals.inhlth.app/hasura/v1/graphql"
HASURA_ADMIN_SECRET = "xo6fSNmltkYvNj1OIRNi27hzIwtW+brpSNJZ+JZxk/4="

HASURA_HEADERS = {
    "Content-Type": "application/json",
    "x-hasura-admin-secret": HASURA_ADMIN_SECRET,
    "x-hasura-role" : "dataops"
}

class GraphqlClient:
    def __init__(self,HASURA_GRAPHQL_URL,HASURA_ADMIN_SECRET):
        self.HASURA_GRAPHQL_URL = HASURA_GRAPHQL_URL
        self.HASURA_ADMIN_SECRET = HASURA_ADMIN_SECRET
        self.HASURA_HEADERS = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": self.HASURA_ADMIN_SECRET,
            "x-hasura-role" : "dataops"
        }

    def execute_graphql_query(self,query, variables=None):
        print("execute_graphql_query")
        query=query.replace("\n", " ")
        try:
            response = requests.post(HASURA_GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HASURA_HEADERS)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"GraphQL query failed: {str(e)}")
            return None

