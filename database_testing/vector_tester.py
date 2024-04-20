from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time

load_dotenv()
vectorapi = os.getenv("VECTOR_API_KEY")

pinecone = Pinecone(api_key=vectorapi)

index_name = "docs-quickstart-index"

pinecone.create_index(
    name=index_name,
    dimension=8,
    metric="cosine",
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    ) 
) 

index = pinecone.Index(index_name)

print(index.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
        {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
        {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
        {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    ],
    namespace="ns1"
))

print(index.upsert(
    vectors=[
        {"id": "vec5", "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]},
        {"id": "vec6", "values": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]},
        {"id": "vec7", "values": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
        {"id": "vec8", "values": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}
    ],
    namespace="ns2"
))

time.sleep(10)

print(index.describe_index_stats())

print(index.query(
    namespace="ns1",
    vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    top_k=3,
    include_values=True
))

print(index.query(
    namespace="ns2",
    vector=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    top_k=3,
    include_values=True
))

pinecone.delete_index(index_name)