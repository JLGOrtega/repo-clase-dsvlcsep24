import streamlit as st
from io import StringIO

import faiss
import cohere
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Cohere API
co = cohere.Client(os.environ["COHERE_API_KEY"])

# Function to chunk text manually (by character length)
def chunk_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to get embeddings using Cohere's API
def get_embedding(text):
    input_type="search_query"
    response = co.embed(texts=[text],
                         model="embed-english-v3.0",  
                         input_type=input_type,
                         embedding_types=['float'])
    return response.embeddings.float[0]

# Function to generate response using Cohere's generation API
def generate_response(context, query):
    response = co.generate(
        model="command-r-plus",
        prompt=f"Context: {context}\n\nQuestion: {query}\nAnswer:",
        max_tokens=512,
        temperature=0.7,
    )
    return response.generations[0].text.strip()


with open("texto_muestra.txt", "r", encoding="utf-8") as f:
    plain_text = f.read()

st.set_page_config(
    page_title="RAG App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])
if uploaded_file is not None:
    # with open(uploaded_file, "r", encoding="utf-8") as f:
        # plain_text = uploaded_file.read()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    plain_text = stringio.read()


chunks = chunk_text(plain_text, chunk_size=1000) ## CUIDADO CON EL NUMERO DE LLAMADAS

# 3. Embed each chunk and create a FAISS index
dimension = 1024  # Cohere embed-english-v3.0 dimension
index = faiss.IndexFlatL2(dimension)


embeddings = []
for chunk in chunks:
    embedding = get_embedding(chunk)
    embeddings.append(embedding)

# Convert embeddings to numpy array and add to FAISS
embeddings = np.array(embeddings).astype('float32')
index.add(embeddings)



st.header("RAG APP")
st.write("kjdkjd.d,kbj.dkjd,kbjsb.vdbvdsbdvb")

# 4. Query and retrieve relevant chunks


query = st.text_input("ASK: ", "HABLAME DE LA FLUORESCENCIA")


if st.button("RUN QUERY", type="primary"):
    

    query_embedding = np.array(get_embedding(query)).astype('float32').reshape(1, -1)

    # Perform search
    k = 1  # Top-1 most relevant chunk
    distances, indices = index.search(query_embedding, k=k)

    # Display the most relevant chunk
    retrieved_chunk = ""
    for i in range(k):
        retrieved_chunk += chunks[indices[0][i]] + "\n"

    st.write("Query: " + query)
    st.write("Retrieved chunk: " + retrieved_chunk)

    st.header("Generated Answer: " )

    # 5. Generate response using the retrieved chunk as context
    generated_answer = generate_response(retrieved_chunk, query)
    st.write("Generated Answer: " + generated_answer)


