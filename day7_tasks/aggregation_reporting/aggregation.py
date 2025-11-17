import pandas as pd

# Load cleaned CSV
df = pd.read_csv("cleaned_data.csv")

# Ensure Salary is numeric
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')  # invalid entries become NaN

# Optional: fill missing salaries (NaN) with 0 or median
df['Salary'] = df['Salary'].fillna(0)  # or df['Salary'].median()

# Aggregation functions

def summary_statistics(df):
    return df.describe()

def total_salary(df):
    return df['Salary'].sum()

def average_salary(df):
    return df['Salary'].mean()

def count_per_city(df):
    return df['City'].value_counts()

def max_salary_employee(df):
    return df[df['Salary'] == df['Salary'].max()]

def min_salary_employee(df):
    return df[df['Salary'] == df['Salary'].min()]

def salary_by_city(df):
    return df.groupby('City')['Salary'].mean().reset_index()

# Reporting
print("===== SUMMARY STATISTICS =====")
print(summary_statistics(df))
print("\n===== TOTAL SALARY =====")
print(total_salary(df))
print("\n===== AVERAGE SALARY =====")
print(average_salary(df))
print("\n===== COUNT PER CITY =====")
print(count_per_city(df))
print("\n===== MAX SALARY EMPLOYEE =====")
print(max_salary_employee(df))
print("\n===== MIN SALARY EMPLOYEE =====")
print(min_salary_employee(df))
print("\n===== AVERAGE SALARY BY CITY =====")
print(salary_by_city(df))
