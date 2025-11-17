import json

print("\n========== STEP 1: READING JSON FILE ==========\n")

# Replace with your filename
json_file = "students.json"

# Read JSON file
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print("JSON Loaded Successfully!")
print("Total Records:", len(data))
print("Example Row:")
print(data[0])   # print first student record


# -------------------------------------------------------------
print("\n========== STEP 2: PRINT ALL STUDENT NAMES ==========\n")

names = [student["Name"] for student in data]

print("Total Names:", len(names))
print("Names:", names)


# -------------------------------------------------------------
print("\n========== STEP 3: FILTER STUDENTS BY CLASS ==========\n")

# Example: students in class "10th"
tenth_class = [s for s in data if s["Class"] == "10th"]

print("Students in 10th Class:", len(tenth_class))
print("List of Names:", [s["Name"] for s in tenth_class])

# Save to new JSON
with open("class_10_students.json", "w", encoding="utf-8") as f:
    json.dump(tenth_class, f, indent=4)

print("File Created: class_10_students.json")


# -------------------------------------------------------------
print("\n========== STEP 4: FILTER STUDENTS WITH MARKS > 90 ==========\n")

high_scorers = [s for s in data if s["Marks"] > 90]

print("Students with Marks > 90:", len(high_scorers))
print("Names:", [s["Name"] for s in high_scorers])

# Save to new JSON
with open("top_students.json", "w", encoding="utf-8") as f:
    json.dump(high_scorers, f, indent=4)

print("File Created: top_students.json")


# -------------------------------------------------------------
print("\n========== STEP 5: FIND AVERAGE MARKS ==========\n")

total_marks = sum([s["Marks"] for s in data])
avg_marks = total_marks / len(data)

print("Total Marks of All Students:", total_marks)
print("Average Marks:", avg_marks)


# -------------------------------------------------------------
print("\n========== STEP 6: SAVE FIRST 2 STUDENTS TO NEW JSON ==========\n")

first_two = data[:2]  # slicing

with open("first_two_students.json", "w", encoding="utf-8") as f:
    json.dump(first_two, f, indent=4)

print("File Created: first_two_students.json")

# -------------------------------------------------------------
print("\n========== DONE ==========\n")
