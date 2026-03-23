from sentence_transformers import SentenceTransformer
import chromadb

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded!")


# Documents
documents = [
    "Python is a programming language used for AI",
    "Machine learning helps computers learn from data",
    "ChromaDB is a vector database for embeddings",
    "Cats are cute and fluffy animals",
    "Neural networks are inspired by human brain",
    "Deep learning uses multiple layers of neural networks",
    "Natural language processing helps computers understand text",
    "Data science combines statistics and programming",
]
# Convert to embeddings
embeddings = model.encode(documents)


print(f"Total documents: {len(embeddings)}")
print(f"Each embedding size: {len(embeddings[0])} numbers")
print(f"First embedding preview: {embeddings[0][:5]}")

# Create ChromaDB client
client=chromadb.Client()

# Use existing if exists, create if not!
collection=client.get_or_create_collection("my_documents")

# Add documents to collection to chromaDB [store documents]
collection.add(
    documents=documents,
    ids=[f"doc{i}" for i in range(len(documents))]
)

print(f"Stored {collection.count()} documents!")


#Interactive search loop
print("\n Smart Document Search Engine")
print("Type 'quit' to exit\n")

while True:
  
  query=input("Search: ")
  
  if query.lower() in ['quit','q']:
    print("Thank you for using it!")
    break

  results = collection.query(        #find similart search
    query_texts=[query],
    n_results=3        # return top 3 most similar
)

#print(results)     # returns dictionary

  print(f"\n Top 3 Results:")
  print("="*50)
  print(f"\n Most Relevant Documents:")
  for i, (doc,distance) in enumerate(zip(      #zip joints two list side by side
      results['documents'][0],
      results['distances'][0]
  )):
    similarity = round((2 - distance) / 2, 4)
    print(f"{i+1}. {doc}")
    print(f" Similarity: {similarity:.4f}")

  print("="*50 + "\n")



