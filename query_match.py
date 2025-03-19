
import numpy as np
import re
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import string

# import os
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# from sentence_transformers import SentenceTransformer ,util
# # method 1# Load model once
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Load predefined queries once
# def load_queries(file_path="question.json"):
#     with open(file_path, "r") as file:
#         return json.load(file)["predefined_questions"]

# predefined_questions = load_queries()

# # Precompute embeddings
# question_embeddings = {}
# for question_type, question in predefined_questions.items():
#     question_embeddings[question_type] = model.encode(question["questions"], convert_to_tensor=True)

# # Function to find best matching query
# def find_matching_query(user_message):
#     user_embedding = model.encode(user_message, convert_to_tensor=True)
    
#     best_score = -1
#     best_query_type = "Unknown"
    
#     for query_type, embeddings in question_embeddings.items():
#         similarity_scores = util.pytorch_cos_sim(user_embedding, embeddings)[0]  # Compute all at once
#         max_score = similarity_scores.max().item()  # Get highest score
        
#         if max_score > best_score:
#             best_score = max_score
#             best_query_type = query_type

#     return best_query_type if best_score >= 0.4 else "Unknown"


#method 2
def text_preprocessing(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = word_tokenize(text)
    text = [lemmatizer.lemmatize(word) for word in text if word not in stop_words and word not in string.punctuation]
    text = ' '.join(text)
    return text

def keyword_match(user_question):
    # print("keyword_match")
    keywords = {
    "All_Orders": ["all", "orders", "every", "blood", "requests", "list","get","show","display",'all orders','placed','all blood','all requests','many','count'],
    "Order_Status": ["status", "check", "specific", "order", "id", "request","get","show","display"],
    "Orders_By_Blood_Type":['order','sort','Blood','Type','blood','list','group',"get","show","display"],
    'Orders_By_BloodBank':['order','bank name','blood','bank','group',"get","show","display","list"],
    'Orders_By_Status_And_BloodBank':['order','status','Blood_Type','blood','bank name','bank','group'],
    'Total_Orders_By_BloodBank':['total','order','bank','blood','count','find',"get","show","display","summarise"],
    'Billing_Overview':['bill','cost','amount','blood','bank','money','hospital','overview','find',"get","show","display"],
    'Billing_By_Company':['bill','cost','amount','blood','bank','money','hospital','find','company'],
    'Cost_By_Blood_Component':['cost','money','expenses','blood','component','group','find','hospital',"get","show","display"],
    'Total_Patients_By_Company':['total','patient','blood bank','group','find',"get","show","display"],
    'Blood_Usage_By_Company':['blood','units','usage','supply','blood bank','group','find',"hospital"],
    'Recent_Orders':['recent','new','latest','current',"get","show","display","order"],
    "Hello":['Hi','hello','good','hey','vanakam'],
    "Bye":['bye','see','thanks','you','end']
}
    user_question = text_preprocessing(user_question)
    words = re.findall(r'\b\w+\b', user_question)
    
    scores = {}
    for query_type, key_words in keywords.items():
        scores[query_type] = sum(1 for word in words if word in key_words)
    
    best_query_type = max(scores.items(), key=lambda x: x[1])[0]
    
    if scores[best_query_type] < 1:
        return "Unknown"
    
    return best_query_type


