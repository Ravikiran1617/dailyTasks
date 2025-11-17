import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Read the CSV file
# Replace 'your_file.csv' with your actual CSV filename
df = pd.read_csv('customers.csv')

# Print column names to verify
print("Column names in the CSV:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Create a figure with multiple subplots
fig = plt.figure(figsize=(16, 12))

# 1. Top 15 Countries by Customer Count
plt.subplot(2, 3, 1)
if 'Country' in df.columns:
    country_counts = df['Country'].value_counts().head(15)
    plt.barh(range(len(country_counts)), country_counts.values, color='steelblue')
    plt.yticks(range(len(country_counts)), country_counts.index, fontsize=8)
    plt.xlabel('Number of Customers')
    plt.title('Top 15 Countries by Customer Count')
    plt.gca().invert_yaxis()
else:
    plt.text(0.5, 0.5, 'Country column not found', ha='center', va='center')
    plt.title('Top 15 Countries by Customer Count')

# 2. Subscription Status Distribution (if column exists)
plt.subplot(2, 3, 2)
subscription_col = None
for col in df.columns:
    if 'subscription' in col.lower() or 'subscript' in col.lower():
        subscription_col = col
        break

if subscription_col:
    subscription_counts = df[subscription_col].value_counts()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    plt.pie(subscription_counts.values, labels=subscription_counts.index, 
            autopct='%1.1f%%', startangle=90, colors=colors[:len(subscription_counts)])
    plt.title('Subscription Status Distribution')
else:
    # Alternative: Show Customer ID distribution or first/last name distribution
    plt.text(0.5, 0.5, 'Subscription column not found\nShowing data distribution', 
             ha='center', va='center')
    plt.title('Data Distribution')

# 3. Top 10 Cities by Customer Count
plt.subplot(2, 3, 3)
if 'City' in df.columns:
    city_counts = df['City'].value_counts().head(10)
    plt.bar(range(len(city_counts)), city_counts.values, color='coral')
    plt.xticks(range(len(city_counts)), city_counts.index, rotation=45, ha='right', fontsize=8)
    plt.ylabel('Number of Customers')
    plt.title('Top 10 Cities by Customer Count')
else:
    plt.text(0.5, 0.5, 'City column not found', ha='center', va='center')
    plt.title('Top 10 Cities by Customer Count')

# 4. Top 15 Companies by Customer Count
plt.subplot(2, 3, 4)
if 'Company' in df.columns:
    company_counts = df['Company'].value_counts().head(15)
    plt.barh(range(len(company_counts)), company_counts.values, color='lightgreen')
    plt.yticks(range(len(company_counts)), company_counts.index, fontsize=8)
    plt.xlabel('Number of Customers')
    plt.title('Top 15 Companies')
    plt.gca().invert_yaxis()
else:
    plt.text(0.5, 0.5, 'Company column not found', ha='center', va='center')
    plt.title('Top 15 Companies')

# 5. Geographic Distribution
plt.subplot(2, 3, 5)
if 'Country' in df.columns:
    top_countries = df['Country'].value_counts().head(10)
    other_count = df['Country'].value_counts()[10:].sum()
    if other_count > 0:
        top_countries['Others'] = other_count
    
    plt.pie(top_countries.values, labels=top_countries.index, 
            autopct='%1.1f%%', startangle=90)
    plt.title('Customer Distribution by Country (Top 10)')
else:
    plt.text(0.5, 0.5, 'Country column not found', ha='center', va='center')
    plt.title('Customer Distribution by Country')

# 6. Customer Distribution Summary
plt.subplot(2, 3, 6)
summary_text = f"""
Dataset Summary:
━━━━━━━━━━━━━━━━━━━━━━
Total Rows: {len(df)}

Total Columns: {len(df.columns)}
"""

if 'Country' in df.columns:
    summary_text += f"\nUnique Countries: {df['Country'].nunique()}"
    summary_text += f"\nTop Country: {df['Country'].mode()[0]}"
    summary_text += f"\n({df['Country'].value_counts().iloc[0]} customers)"

if 'City' in df.columns:
    summary_text += f"\n\nUnique Cities: {df['City'].nunique()}"

if 'Company' in df.columns:
    summary_text += f"\n\nUnique Companies: {df['Company'].nunique()}"

plt.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
         verticalalignment='center')
plt.axis('off')
plt.title('Dataset Overview', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('customer_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Additional detailed statistics
print("\n" + "="*50)
print("DETAILED STATISTICS")
print("="*50)

if 'Country' in df.columns:
    print("\n📊 Top 10 Countries:")
    print(df['Country'].value_counts().head(10))

if 'Company' in df.columns:
    print("\n🏢 Top 10 Companies:")
    print(df['Company'].value_counts().head(10))

if 'City' in df.columns:
    print("\n🌆 Top 10 Cities:")
    print(df['City'].value_counts().head(10))

if subscription_col:
    print(f"\n📧 {subscription_col} Distribution:")
    print(df[subscription_col].value_counts())

# Create expanded country distribution plot
if 'Country' in df.columns:
    plt.figure(figsize=(14, 8))
    country_counts_all = df['Country'].value_counts().head(20)
    colors_gradient = plt.cm.viridis([i/len(country_counts_all) for i in range(len(country_counts_all))])
    plt.barh(range(len(country_counts_all)), country_counts_all.values, color=colors_gradient)
    plt.yticks(range(len(country_counts_all)), country_counts_all.index)
    plt.xlabel('Number of Customers', fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.title('Top 20 Countries by Customer Count', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('countries_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

print("\n✅ Visualizations saved successfully!")
print("   - customer_analysis.png")
print("   - countries_distribution.png")