import pandas as pd

# 1️⃣ Load your messy CSV
df = pd.read_csv("messy_data.csv")

# 2️⃣ Drop duplicates & missing rows
df = df.drop_duplicates().dropna()

# 3️⃣ Fix text: remove extra spaces & normalize
for col in df.select_dtypes(include='object'):
    df[col] = df[col].str.strip().str.title()

# 4️⃣ Convert numeric columns properly
for col in df.select_dtypes(include='object'):
    if df[col].str.replace('.', '', 1).str.isdigit().all():
        df[col] = pd.to_numeric(df[col])

# 5️⃣ Save cleaned CSV
df.to_csv("cleaned_data.csv", index=False)

print("✅ Your CSV is clean and ready!")
