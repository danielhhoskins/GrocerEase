#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pathlib import Path
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
import json
from typing import Sequence, List

from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool

import nest_asyncio

nest_asyncio.apply()

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


# In[2]:


import llama_index
llama_index.set_global_handler("simple")


# ## OpenAI Agent with Query Engine Tools

# In[3]:


PagedCSVReader = download_loader("PagedCSVReader")

loader = PagedCSVReader(encoding="utf-8")
documents = loader.load_data(file=Path('/Users/danielhoskins/src/llms/GrocerEase_project/grocery.csv'))


# In[4]:


index = VectorStoreIndex.from_documents(documents)


# In[5]:


index.storage_context.persist(persist_dir="./storage/")


# In[ ]:


grocery_query_engine = index.as_query_engine(similarity_top_k=5)
# query_engine = CitationQueryEngine.from_args(
#     index,
#     similarity_top_k=5,
# )


# In[5]:


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


# In[12]:


agent = OpenAIAgent.from_tools(
    query_engine_tools,
    verbose=True,
    model="gpt-4",
    system_prompt="""You are a grocery assistant who suggests available grocery items to online grocery shoppers.
    You only suggest items that are in the inventory, and none others. 
    You try to suggest 3-5 items.
    You only recommend grocery items that suit the user's query.
    If it's at all possible that the user is seeking grocery suggestions, you interpret their query that way and use the tool to find suggestions from the inventory.
    When describing the grocery items, you only use the information you get from the tool.
    You do not provide suggestions that aren't related to groceries."""
)


# In[13]:


# response = agent.astream_chat("Hello")
# response_gen = response.response_gen

# for token in response.async_response_gen():
#     print(token, end="")


# ### Halloween party snack scenario

# In[14]:


# response = await agent.astream_chat("What snacks would be good for a halloween party?")
# response_gen = response.response_gen

# async for token in response.async_response_gen():
#     print(token, end="")


# In[15]:


# response = await agent.astream_chat("Tell me more about the first one")
# response_gen = response.response_gen

# async for token in response.async_response_gen():
#     print(token, end="")


# ### Hiking Scenario

# In[17]:


response =  agent.chat("I'm going on a three day hiking trip through the smoky mountains. What foods should I pack?")
response_gen = response.response_gen

for token in response.async_response_gen():
    print(token, end="")

a = 'hi'

# In[11]:


# response = await agent.astream_chat("I'm going on a three day hiking trip through the smoky mountains. What food should I pack?")
# response_gen = response.response_gen

# async for token in response.async_response_gen():
#     print(token, end="")


# In[ ]:




