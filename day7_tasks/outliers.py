import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Sample dataset for demonstration
data = {
    'Age': [25, 28, 22, 35, 29, 150, 31, 27, 33, 26, 30, 24],
    'Salary': [50000, 55000, 48000, 62000, 51000, 500000, 53000, 49000, 58000, 52000, 54000, 47000],
    'Experience': [2, 5, 1, 8, 3, 25, 4, 2, 6, 3, 5, 1]
}
df = pd.DataFrame(data)

print("="*70)
print("OUTLIER DETECTION METHODS - COMPLETE GUIDE")
print("="*70)
print("\nSample Dataset:")
print(df)
print("\n")

# ============================================================================
# METHOD 1: IQR (Interquartile Range) Method - MOST COMMON
# ============================================================================
print("="*70)
print("METHOD 1: IQR (Interquartile Range) Method")
print("="*70)
print("Best for: Normally distributed data, general purpose\n")

def detect_outliers_iqr(data, column):
    """
    IQR Method: Finds outliers using the 25th and 75th percentiles
    
    Formula:
    - Q1 = 25th percentile
    - Q3 = 75th percentile
    - IQR = Q3 - Q1
    - Lower Bound = Q1 - 1.5 × IQR
    - Upper Bound = Q3 + 1.5 × IQR
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Find outliers
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    print(f"\n📊 Analyzing: {column}")
    print(f"   Q1 (25th percentile): {Q1}")
    print(f"   Q3 (75th percentile): {Q3}")
    print(f"   IQR: {IQR}")
    print(f"   Lower Bound: {lower_bound}")
    print(f"   Upper Bound: {upper_bound}")
    print(f"   Outliers found: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"\n   🚨 Outlier values:")
        print(outliers[[column]])
    
    return outliers, lower_bound, upper_bound

# Detect outliers in Age column
outliers_age, lb_age, ub_age = detect_outliers_iqr(df, 'Age')

# Detect outliers in Salary column
outliers_salary, lb_salary, ub_salary = detect_outliers_iqr(df, 'Salary')

# ============================================================================
# METHOD 2: Z-Score Method
# ============================================================================
print("\n" + "="*70)
print("METHOD 2: Z-Score Method")
print("="*70)
print("Best for: Normally distributed data, when you know standard deviation\n")

def detect_outliers_zscore(data, column, threshold=3):
    """
    Z-Score Method: Measures how many standard deviations away from mean
    
    Formula:
    Z = (X - μ) / σ
    where X = value, μ = mean, σ = standard deviation
    
    Typical threshold: 3 (values beyond ±3 standard deviations)
    """
    mean = data[column].mean()
    std = data[column].std()
    
    # Calculate z-scores
    z_scores = np.abs((data[column] - mean) / std)
    
    # Find outliers
    outliers = data[z_scores > threshold]
    
    print(f"\n📊 Analyzing: {column}")
    print(f"   Mean: {mean:.2f}")
    print(f"   Standard Deviation: {std:.2f}")
    print(f"   Z-Score Threshold: {threshold}")
    print(f"   Outliers found: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"\n   🚨 Outlier values and their Z-scores:")
        for idx in outliers.index:
            value = data.loc[idx, column]
            z = abs((value - mean) / std)
            print(f"      {value} (Z-score: {z:.2f})")
    
    return outliers

outliers_zscore_age = detect_outliers_zscore(df, 'Age')
outliers_zscore_salary = detect_outliers_zscore(df, 'Salary')

# ============================================================================
# METHOD 3: Modified Z-Score (MAD - Median Absolute Deviation)
# ============================================================================
print("\n" + "="*70)
print("METHOD 3: Modified Z-Score (MAD)")
print("="*70)
print("Best for: Data with extreme outliers, more robust than Z-score\n")

def detect_outliers_mad(data, column, threshold=3.5):
    """
    MAD Method: Uses median instead of mean (more robust)
    
    Formula:
    MAD = median(|Xi - median(X)|)
    Modified Z-score = 0.6745 * (Xi - median(X)) / MAD
    """
    median = data[column].median()
    mad = np.median(np.abs(data[column] - median))
    
    # Calculate modified z-scores
    modified_z_scores = 0.6745 * (data[column] - median) / mad
    
    # Find outliers
    outliers = data[np.abs(modified_z_scores) > threshold]
    
    print(f"\n📊 Analyzing: {column}")
    print(f"   Median: {median}")
    print(f"   MAD: {mad:.2f}")
    print(f"   Threshold: {threshold}")
    print(f"   Outliers found: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"\n   🚨 Outlier values:")
        print(outliers[[column]])
    
    return outliers

outliers_mad_age = detect_outliers_mad(df, 'Age')

# ============================================================================
# METHOD 4: Percentile Method
# ============================================================================
print("\n" + "="*70)
print("METHOD 4: Percentile Method")
print("="*70)
print("Best for: Quick analysis, defining outliers by extreme percentages\n")

def detect_outliers_percentile(data, column, lower_percentile=5, upper_percentile=95):
    """
    Percentile Method: Values outside specified percentiles are outliers
    
    Common thresholds:
    - 5th and 95th percentile (10% outliers)
    - 1st and 99th percentile (2% outliers)
    """
    lower_bound = data[column].quantile(lower_percentile / 100)
    upper_bound = data[column].quantile(upper_percentile / 100)
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    print(f"\n📊 Analyzing: {column}")
    print(f"   Lower Percentile ({lower_percentile}%): {lower_bound}")
    print(f"   Upper Percentile ({upper_percentile}%): {upper_bound}")
    print(f"   Outliers found: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"\n   🚨 Outlier values:")
        print(outliers[[column]])
    
    return outliers, lower_bound, upper_bound

outliers_percentile = detect_outliers_percentile(df, 'Salary', 5, 95)

# ============================================================================
# METHOD 5: Isolation Forest (Machine Learning)
# ============================================================================
print("\n" + "="*70)
print("METHOD 5: Isolation Forest (Machine Learning)")
print("="*70)
print("Best for: Multi-dimensional data, complex patterns\n")

from sklearn.ensemble import IsolationForest

def detect_outliers_isolation_forest(data, columns, contamination=0.1):
    """
    Isolation Forest: ML algorithm that isolates anomalies
    
    contamination: expected proportion of outliers (0.1 = 10%)
    """
    # Select numeric columns
    X = data[columns]
    
    # Train model
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso_forest.fit_predict(X)
    
    # -1 indicates outlier, 1 indicates normal
    outlier_mask = predictions == -1
    outliers = data[outlier_mask]
    
    print(f"\n📊 Analyzing columns: {columns}")
    print(f"   Contamination (expected outliers): {contamination*100}%")
    print(f"   Outliers found: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"\n   🚨 Outlier rows:")
        print(outliers[columns])
    
    return outliers

outliers_ml = detect_outliers_isolation_forest(df, ['Age', 'Salary', 'Experience'])

# ============================================================================
# VISUALIZATION: Compare All Methods
# ============================================================================
print("\n" + "="*70)
print("CREATING VISUALIZATIONS")
print("="*70)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Outlier Detection Methods Comparison', fontsize=16, fontweight='bold')

# 1. Box Plot (shows IQR method visually)
axes[0, 0].boxplot(df['Age'])
axes[0, 0].set_title('Box Plot - Age\n(IQR Method Visualization)')
axes[0, 0].set_ylabel('Age')
axes[0, 0].grid(True, alpha=0.3)

# 2. Scatter plot with IQR bounds
axes[0, 1].scatter(range(len(df)), df['Age'], c='blue', alpha=0.6)
axes[0, 1].axhline(y=lb_age, color='r', linestyle='--', label='Lower Bound')
axes[0, 1].axhline(y=ub_age, color='r', linestyle='--', label='Upper Bound')
axes[0, 1].set_title('IQR Method - Age')
axes[0, 1].set_xlabel('Index')
axes[0, 1].set_ylabel('Age')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. Distribution with Z-score
axes[0, 2].hist(df['Age'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
mean_age = df['Age'].mean()
std_age = df['Age'].std()
axes[0, 2].axvline(mean_age, color='green', linestyle='-', linewidth=2, label='Mean')
axes[0, 2].axvline(mean_age + 3*std_age, color='red', linestyle='--', label='±3 SD')
axes[0, 2].axvline(mean_age - 3*std_age, color='red', linestyle='--')
axes[0, 2].set_title('Z-Score Method - Age')
axes[0, 2].set_xlabel('Age')
axes[0, 2].set_ylabel('Frequency')
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

# 4. Salary Box Plot
axes[1, 0].boxplot(df['Salary'])
axes[1, 0].set_title('Box Plot - Salary')
axes[1, 0].set_ylabel('Salary ($)')
axes[1, 0].grid(True, alpha=0.3)

# 5. Salary Scatter with IQR
axes[1, 1].scatter(range(len(df)), df['Salary'], c='green', alpha=0.6)
axes[1, 1].axhline(y=lb_salary, color='r', linestyle='--', label='Lower Bound')
axes[1, 1].axhline(y=ub_salary, color='r', linestyle='--', label='Upper Bound')
axes[1, 1].set_title('IQR Method - Salary')
axes[1, 1].set_xlabel('Index')
axes[1, 1].set_ylabel('Salary ($)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# 6. Summary comparison
summary_text = f"""
OUTLIER DETECTION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━

Dataset: {len(df)} rows

AGE Column:
• IQR Method: {len(outliers_age)} outliers
• Z-Score: {len(outliers_zscore_age)} outliers
• MAD: {len(outliers_mad_age)} outliers

SALARY Column:
• IQR Method: {len(outliers_salary)} outliers
• Z-Score: {len(outliers_zscore_salary)} outliers

Multi-Column (ML):
• Isolation Forest: {len(outliers_ml)} outliers

RECOMMENDATION:
✓ Use IQR for general purpose
✓ Use Z-Score for normal data
✓ Use MAD for robust detection
✓ Use ML for complex patterns
"""
axes[1, 2].text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
               verticalalignment='center')
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig('outlier_detection_comparison.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved: outlier_detection_comparison.png")
plt.show()

# ============================================================================
# PRACTICAL GUIDE: Which Method to Use?
# ============================================================================
print("\n" + "="*70)
print("WHICH METHOD SHOULD YOU USE?")
print("="*70)
print("""
┌─────────────────────┬──────────────────────────────────────────┐
│ Method              │ Best Used When...                        │
├─────────────────────┼──────────────────────────────────────────┤
│ IQR                 │ • General purpose (MOST COMMON)          │
│                     │ • Quick analysis                         │
│                     │ • Don't know data distribution           │
├─────────────────────┼──────────────────────────────────────────┤
│ Z-Score             │ • Data is normally distributed           │
│                     │ • Need standard deviation info           │
│                     │ • Statistical analysis                   │
├─────────────────────┼──────────────────────────────────────────┤
│ MAD (Modified Z)    │ • Data has extreme outliers              │
│                     │ • Need robust method                     │
│                     │ • Mean is skewed                         │
├─────────────────────┼──────────────────────────────────────────┤
│ Percentile          │ • Need custom thresholds                 │
│                     │ • Business rules apply                   │
│                     │ • Simple interpretation                  │
├─────────────────────┼──────────────────────────────────────────┤
│ Isolation Forest    │ • Multiple columns (multivariate)        │
│                     │ • Complex patterns                       │
│                     │ • Large datasets                         │
└─────────────────────┴──────────────────────────────────────────┘

💡 PRO TIP: Use multiple methods and compare results!
""")

# ============================================================================
# EXAMPLE: Apply to Your CSV
# ============================================================================
print("\n" + "="*70)
print("APPLYING TO YOUR CSV FILE")
print("="*70)
print("""
# To use with your CSV file:

import pandas as pd

# Load your data
df = pd.read_csv('your_file.csv')

# Method 1: IQR (Recommended for beginners)
Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df['Age'] < lower) | (df['Age'] > upper)]
print(f"Outliers found: {len(outliers)}")
print(outliers)

# Remove outliers (if needed)
df_clean = df[(df['Age'] >= lower) & (df['Age'] <= upper)]

# Or flag them instead of removing
df['is_outlier'] = (df['Age'] < lower) | (df['Age'] > upper)
""")