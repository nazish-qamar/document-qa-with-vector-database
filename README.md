# A document Q&A app built with langchain that utilizes RetrievalQAWithSourcesChain chain to build RAG pattern-based chatbot for your custom document. The RetrievalQAWithSourcesChain ensures that the app responds with the list of sources.
### - The UI app is built with Chainlit
### - OpenAI embedding and chat models are used for the demo. 
#
# Prerequisite:
### create ".env" file in the root directory with following key:
### OPENAI_API_KEY = YOUR_API_KEY
#
# To start the app run the following command in terminal: 
### chainlit run document_qa.py -w  
# Note: Before running Q&A app, one could also run the chroma_db_basics.py file to get a feel of the ChromaDB Vector by running the command:
### chainlit run chroma_db_basics.py -w 
#
# Steps happening in the backend:
### 1. Creating chunks of the uploaded document.
### 2. Creating list of "Document" object with source as "metadata"
### 3. Creating embeddings of the "Document" object list using OpenAI Embedding model.
### 4. Creating Chroma vector database of embeddings
### 5. User query from the chainlit becomes the user prompt to the OpenAI chat model. Please note that if you want the output in a specific format then give the example format after your query. For example one case ask question as:
#### "Your question ### Your format ###"