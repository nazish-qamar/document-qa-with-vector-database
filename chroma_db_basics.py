#export HNSWLIB_NO_NATIVE = 1
import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_vector_database")

collection.add(

    documents=["my name is Someone", "my name is not Someone"], # list of our documents
    metadatas=[{"source":"name is true"},{"source":"name is false"}], # to output the source from where the model got the information
    ids=["id1","id2"] 
)

results = collection.query(
    query_texts=['What is my name?'],
    n_results=1
)

print(results)