import pandas as pd
import os
import torch
import regex as re
import json
import requests
from tqdm import tqdm
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import huggingface_hub
from huggingface_hub import notebook_login

huggingface_hub.login(token='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')

def activity_entities_extractor(articles):
    model_id = "mistralai/Mixtral-8x7B-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True)

    text = f"""
    You are a helpful assistant who evaluates Linkedin Activity by a user over a given time period split by "\n\n". Generate a one line description of topic discussed in the each of the posts and extract urls if present for each post.
    
    Format Instructions: {{"post_id_1": post_id_1, "post_topic_1": post_topic_1, "post_url_1": url_1 if any, post_id_2": post_id_2, "post_topic_2": post_topic_2, "post_url_2": url_2 if any, ...}}
    
    Linkedin Articles: {articles}
    """
    
    inputs = tokenizer(text, return_tensors="pt").to(0)
    outputs = model.generate(**inputs, max_new_tokens=1000)
    return(tokenizer.decode(outputs[0], skip_special_tokens=True))   

activity_data = pd.read_csv(r'post_details.csv')
activity_data['post_info'] = activity_data['post_info'].astype(str).apply(lambda x: x.replace("\n",""))
activity_data['like_count'] = activity_data['like_count'].astype(str).apply(lambda x: x.replace("\n","")[:4])
activity_data['date_of_post'] = activity_data['date_of_post'].astype(str).apply(lambda x: x.replace("\n",""))


input_to_llm = ""

for index in activity_data.index:
  input_to_llm+="Post Description Number {}: ".format(index)+str(activity_data.at[index, 'post_info'])+"Like Count : "+str(activity_data.at[index, 'like_count'])+"\n\n"

response = activity_entities_extractor(input_to_llm)
print(response)
