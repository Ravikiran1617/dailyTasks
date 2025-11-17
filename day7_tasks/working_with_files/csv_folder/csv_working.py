import csv

print("\n========== STEP 1: READING CSV FILE ==========\n")

csv_file = "customers.csv"   # put your CSV name here

# Reading the CSV file
with open(csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)   # reads header row automatically
    rows = list(reader)          # convert to list

print("Total Rows:", len(rows))
print("First Row (example):")
print(rows[0])   # show first row so you understand the structure


# -------------------------------------------------------------
print("\n========== STEP 2: GET CUSTOMER NAMES ==========\n")

# Get full names
full_names = [r["First Name"] + " " + r["Last Name"] for r in rows]

print("Total Names:", len(full_names))
print("Sample Names:", full_names[:5])   # print only first 5


# -------------------------------------------------------------
print("\n========== STEP 3: FILTER CUSTOMERS BY COUNTRY ==========\n")

# Example: all customers from India
vietnam_customers = [r for r in rows if r["Country"] == "Vietnam"]

print("Customers from Vietnam:", len(vietnam_customers))

# Save them to a new CSV
with open("customers_from_Vietnam.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(vietnam_customers)

print("File Created: customers_from_Vietnam.csv")


# -------------------------------------------------------------
print("\n========== STEP 4: CUSTOMERS WHO HAVE A WEBSITE ==========\n")

has_website = [r for r in rows if r["Website"].strip() != ""]

print("Customers with Website:", len(has_website))

# Save to new CSV
with open("customers_with_website.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(has_website)

print("File Created: customers_with_website.csv")


# -------------------------------------------------------------
print("\n========== STEP 5: COUNT CUSTOMERS BY CITY ==========\n")

city_count = {}

for r in rows:
    city = r["City"]
    if city not in city_count:
        city_count[city] = 1
    else:
        city_count[city] += 1

print("Total Unique Cities:", len(city_count))
print("Some City Counts:", list(city_count.items())[:5])


# -------------------------------------------------------------
print("\n========== STEP 6: SAVE FIRST 10 ROWS TO NEW CSV ==========\n")

first_10 = rows[:10]   # slicing

with open("first_10_customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(first_10)

print("File Created: first_10_customers.csv")


# -------------------------------------------------------------
print("\n========== DONE ==========\n")
