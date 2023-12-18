import pandas as pd
import os
import torch
import openai
import regex as re
import json
import requests
from tqdm import tqdm
from transformers import pipeline
import tiktoken
import pandas as pd
import re
from urllib import parse
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from itertools import islice
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from itertools import islice
import base64
import requests
from pathlib import Path
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.llms import OpenAI
import requests
import requests
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import nltk
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
nltk.download('punkt')

def split_into_chunks(text, chunk_size=4000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def activity_entities_extractor(input_to_llm):
    response_schemas = [
        ResponseSchema(name="Post ID", description="ID of the Linkedin Post"),
        ResponseSchema(name="Post Topic", description="Topic Described By Linkedin Post"),
        ResponseSchema(name="URL", description="List of URLs, if present"),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    chat_model = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.5, openai_api_key = "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")

    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("""
            You are a helpful assistant who evaluates Linkedin Activity by a user over a given time period split by "\n\n". Generate a one line description of topic discussed in the each of the posts and extract urls if present for each post.
            {format_instructions}
            Linkedin Articles: {question}""")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    clean_transcript = input_to_llm
    transcription_token_length = num_tokens_from_string(clean_transcript, "gpt-3.5-turbo-16k")
    if transcription_token_length<16000:
      _input = prompt.format_prompt(question=clean_transcript)
      output = chat_model(_input.to_messages())
      return(output)
      #return(output_parser.parse(output.content))
    else:
      print("Token Limit Exceeded. Summarizing and evaluating")
      complete_content_chunks = split_into_chunks(clean_transcript,16000)
      summarized_transcription = []
      for chunk in complete_content_chunks:
        doc =  Document(page_content=chunk, metadata={"source": "transcription"})
        summ_chain = load_summarize_chain(chat_model, chain_type="stuff")
        transcription = summ_chain.run([doc])
        summarized_transcription.append(transcription)
      summarized_transcription = ' '.join(summarized_transcription)
      summ_chain = load_summarize_chain(chat_model, chain_type="stuff")
      doc_summarized =  Document(page_content=summarized_transcription, metadata={"source": "summarized_transcription"})
      summarized_transcription_updated = summ_chain.run([doc_summarized])
      _input = prompt.format_prompt(question=summarized_transcription_updated+'\nURL: '+str(list(self.transcriptions.keys())[0]))
      output = chat_model(_input.to_messages())
      topic_dict[output_parser.parse(output.content)['URL']] = output_parser.parse(output.content)
      return(output_parser.parse(output.content))

activity_data = pd.read_csv(r'post_details.csv')
activity_data['post_info'] = activity_data['post_info'].astype(str).apply(lambda x: x.replace("\n",""))
activity_data['like_count'] = activity_data['like_count'].astype(str).apply(lambda x: x.replace("\n","")[:4])
activity_data['date_of_post'] = activity_data['date_of_post'].astype(str).apply(lambda x: x.replace("\n",""))


input_to_llm = ""

for index in activity_data.index:
  input_to_llm+="Post Description Number {}: ".format(index)+str(activity_data.at[index, 'post_info'])+"Like Count : "+str(activity_data.at[index, 'like_count'])+"\n\n"

response = activity_entities_extractor(input_to_llm)
response_split = response.content.split("}\n{")
updated_responses = []

for r in response_split:
  r = r.replace("\n\t","").replace("\n","").strip()
  r = re.sub('\s+', ' ', r).strip()
  r = r.replace("json{","")
  r = r.replace("```","")
  updated_responses.append(r)

post_info = pd.DataFrame(columns=['Post_ID','Topic','URL'])

for i in updated_responses:
  post_details = i.split('''","''')  
  post_info = post_info.append({'Post_ID': post_details[0].split(":")[1].replace('"',""), 'Topic': post_details[1].split(":")[1], 'URL': post_details[2].split(":")[1]}, ignore_index=True)

post_info['Post_ID'] = post_info['Post_ID'].astype(int)
post_info.set_index('Post_ID', inplace=True)
activity_with_inference = pd.merge(activity_data, post_info, left_index=True, right_index=True)
activity_with_inference.to_csv(r'activity_with_inference.csv')
