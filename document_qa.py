import os

from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
import chainlit as cl
from chainlit.types import AskFileResponse


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embeddings = OpenAIEmbeddings()

welcome_message = """Welcome to the chainlit PDF Q&A demo! To get started
1. Upload a PDF or text file
2. Ask a question related to the file content
"""

def process_file(file: AskFileResponse):
    import tempfile

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile() as tempfile:
        tempfile.write(file.content)
        loader = Loader(tempfile.name)
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs

def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    # save data in the user session
    cl.user_session.set("docs", docs)

    # create a unique namespace for the file
    docsearch = chroma.from_documents(
        docs, embeddings
    )
    return docsearch

@cl.on_chat_start
async def start():
    # sending an image with the local file path
    await cl.Message(content="You can now chat with your PDFs.").send()
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # No async implementation in the Pinecone client, fallback to sync
    docsearch = await cl.make_async(get_docsearch)(file)

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=512),
        chain_type="stuff",
        retriever=docsearch.as_retriever(max_tokens_limit=4097),
    )