from flask import Flask, jsonify
from flask import request
from llama_index import load_index_from_storage

from pathlib import Path
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
import json
from typing import Sequence, List, Dict

from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool

import requests
import json


# import nest_asyncio

# nest_asyncio.apply()

from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index import VectorStoreIndex
from llama_index import download_loader

import json
from typing import Sequence

from llama_index.tools import BaseTool, FunctionTool

import os
from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext
import llama_index

def get_cart_quantity(item_title):
    url = "https://grocerease-testing.bubbleapps.io/version-test/api/1.1/obj/cart_item"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps([{"key": "title", "constraint_type": "equals", "value": item_title}])
    response = requests.get(url, headers=headers, data=payload)
    response_dict = response.json()
    return response_dict['quantity'], response_dict['_id']

def update_cart_item_quantity(uid, new_quantity):
    # URL with the given UID
    url = f"https://grocerease-testing.bubbleapps.io/version-test/api/1.1/obj/cart_item/{uid}"

    # Headers for Bearer Authentication
    headers = {
        "Authorization": "Bearer 7bfc2ef87b1ca030158dda3d0a1533c4",
        "Content-Type": "application/json"
    }

    # JSON payload
    payload = {
        "quantity": new_quantity
    }

    # Making the PATCH request
    response = requests.patch(url, json=payload, headers=headers)

    # Returning the response
    return response.json()

app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Hello World!"

    

# NOTE: for local testing only, do NOT deploy with your key hardcoded
os.environ["OPENAI_API_KEY"] = "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"
PagedCSVReader = download_loader("PagedCSVReader")

llama_index.set_global_handler("simple")

# def initialize_index():
#     global index
#     loader = PagedCSVReader(encoding="utf-8")
#     documents = loader.load_data(file=Path('./documents/grocery.csv'))
#     index = VectorStoreIndex.from_documents(documents)
#     index.storage_context.persist(persist_dir="./storage/")

PagedCSVReader = download_loader("PagedCSVReader")
loader = PagedCSVReader(encoding="utf-8")
documents = loader.load_data(file=Path('./documents/grocery.csv'))
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="./storage/")





#LlamaIndex set-up:
grocery_query_engine = index.as_query_engine(similarity_top_k=5)
query_engine_tools = [
    QueryEngineTool(
        query_engine=grocery_query_engine,
        metadata=ToolMetadata(
            name="get_grocery_items",
            description=(
                "Retrieves relavant grocery items that are available in the inventory."
            ),
        ),
    )]
agent = OpenAIAgent.from_tools(
    query_engine_tools,
    verbose=True,
    model="gpt-4-1106-preview",
    system_prompt="""You are a grocery assistant who suggests available grocery items to online grocery shoppers.
    You only suggest items that are in the inventory, and none others.
    If an item isn't relevant to the user's query, don't list it. 
    Always answer in one sentence or less.
    When describing the grocery items, you only use the information you get from the tool.
    You suggest a maximum of 5 relevant items from the inventory.
    If it's at all possible that the user is seeking grocery suggestions, you interpret their query that way and use the tool to find suggestions from the inventory.
    You do not provide suggestions that aren't related to groceries."""
)

def get_response_source_nodes_data_dicts(response) -> List[Dict]:
    def csv_line_text_to_dict(line_text):
        line_text = line_text.lstrip('\ufeff')
        lines = line_text.strip().split('\n')
        data_dict = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in lines}
        return data_dict
    # print(type(response))
    # print("sources: ", response.sources)
    if len(response.sources) >= 1:
        num_source_nodes = len(response.sources[0].raw_output.source_nodes)
        nodes = [response.sources[0].raw_output.source_nodes[i] for i in range(num_source_nodes)]
    else:
        nodes = []
    ret = []
    for node in nodes:
        ret.append(csv_line_text_to_dict(node.node.text))
    return ret

@app.route("/", methods=["GET"])
def query_index():
    global index
    # Retrieve the text from the POST request's data
    query_text = request.args.get("text", None)
    
    if query_text is None:
        return (
            "No text found in the request body. Please include a 'text' field in the JSON body.",
            400,
        )
    
    response = agent.chat(query_text)
    response_AI_message_text = response.response
    response_source_nodes_data_dicts = get_response_source_nodes_data_dicts(response)
    for item in response_source_nodes_data_dicts:
        item["cart_quantity"] = 0
    ret_dict = {"response_AI_message_text": response_AI_message_text, "items": response_source_nodes_data_dicts}
    
    return jsonify(ret_dict), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)