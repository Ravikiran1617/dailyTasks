import pandas as pd

chunks = pd.read_csv("customers.csv", chunksize=10)

for chunk in chunks:
    # Process each chunk
    print(chunk.shape)
