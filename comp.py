import pandas as pd

df = pd.read_excel("elma_s2_s3.xlsx")

h1 = df.iloc[0]
h2 = df.iloc[1]

print("Header 1:", h1.tolist())
print("Header 2:", h2.tolist())

print("First data row:", df.iloc[2].tolist())
