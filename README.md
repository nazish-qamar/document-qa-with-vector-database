# A document Q&A app built with langchain. The app always respond with the list of sources.
# The UI app is built with Chainlit and the OpenAI embedding and chat models are used for the demo. 
#
# Prerequisite:
### create ".env" file in the root directory with following key:
### OPENAI_API_KEY = YOUR_API_KEY
#
# To start the app run the following command in terminal: 
### chainlit run document_qa.py -w  
#
# Steps happening in the backend:
### 1. Creating chunks of the uploaded document.
### 2. Creating list of "Document" object with source as "metadata"
### 3. Creating embeddings of the "Document" object list using OpenAI Embedding model.
### 4. Creating Chroma vector database of embeddings
### 5. User query from the chainlit becomes the user prompt to the OpenAI chat model. Please note that if you want the output in a specif format then give the example format after your query. For example one case ask question as:
##### "Your question ### Your format ###"