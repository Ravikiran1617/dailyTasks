import pandas as pd

print("\n========== STEP 1: READING EXCEL FILE ==========\n")

file = "employees.xlsx"

# Read the Excel sheet
df = pd.read_excel(file)

print("Excel File Loaded Successfully!")
print("\nTotal Rows:", len(df))
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 Rows:")
print(df.head())


# -------------------------------------------------------------
print("\n========== STEP 2: FILTER BY DEPARTMENT (IT) ==========\n")

it_dept = df[df["Department"] == "IT"]
print("Employees in IT Department:", len(it_dept))
print(it_dept)

# Save IT employees to a new Excel file
it_dept.to_excel("it_employees.xlsx", index=False)
print("File Created: it_employees.xlsx")


# -------------------------------------------------------------
print("\n========== STEP 3: FILTER SALARY > 60000 ==========\n")

high_salary = df[df["Salary"] > 60000]
print("Employees with Salary > 60,000:", len(high_salary))
print(high_salary)

high_salary.to_excel("high_salary_employees.xlsx", index=False)
print("File Created: high_salary_employees.xlsx")


# -------------------------------------------------------------
print("\n========== STEP 4: SORT EMPLOYEES BY SALARY DESC ==========\n")

sorted_salary = df.sort_values(by="Salary", ascending=False)
print("Top 5 Highest Paid Employees:")
print(sorted_salary.head())

sorted_salary.to_excel("employees_sorted_by_salary.xlsx", index=False)
print("File Created: employees_sorted_by_salary.xlsx")


# -------------------------------------------------------------
print("\n========== STEP 5: DEPARTMENT-WISE EMPLOYEE COUNT ==========\n")

dept_count = df["Department"].value_counts()
print("Employee Count by Department:")
print(dept_count)

# Save counts to Excel
dept_count.to_excel("department_count.xlsx")
print("File Created: department_count.xlsx")


# -------------------------------------------------------------
print("\n========== STEP 6: CALCULATE AVG, MIN, MAX SALARY ==========\n")

avg_salary = df["Salary"].mean()
max_salary = df["Salary"].max()
min_salary = df["Salary"].min()

print("Average Salary:", avg_salary)
print("Highest Salary:", max_salary)
print("Lowest Salary:", min_salary)


# -------------------------------------------------------------
print("\n========== STEP 7: SAVE FIRST 3 ROWS TO NEW EXCEL ==========\n")

first_three = df.head(3)
first_three.to_excel("first_three_employees.xlsx", index=False)

print("File Created: first_three_employees.xlsx")

# -------------------------------------------------------------
print("\n========== DONE ==========\n")
