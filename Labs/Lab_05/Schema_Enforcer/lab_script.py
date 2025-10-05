import csv
import json 
import pandas as pd 

# create csv: messy so we can clean later
data = [
    {"student_id": 101, "major": "Commerce", "GPA": 3.0, "is_cs_major": False, "credits_taken": 10.5},
    {"student_id": 102, "major": "Computer Science", "GPA": 4, "is_cs_major": "Yes", "credits_taken": '11.5'}, 
    {"student_id": 103, "major": "Psychology", "GPA": 2.5, "is_cs_major": "No", "credits_taken": 12.5}, 
    {"student_id": 104, "major": "Computer Science", "GPA": 2, "is_cs_major": True, "credits_taken": 13.0}, 
    {"student_id": 105, "major": "Computer Science", "GPA": 3.5, "is_cs_major": True, "credits_taken": '9.5'},  
]

# Write data to CSV
with open("raw_survey_data.csv", mode ="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
    writer.writeheader()
    writer.writerows(data)

# Task two: json file creation 
data = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
        {"name": "Austin Rivera", "role": "Primary"}, 
        {"name": "Heywood Williams-Tracy", "role": "TA"} 
        ]
    },
    {
        "course_id": "CS3130",
        "title": "Computer Systems and Organization 2",
        "level": 300,
        "instructors": [
        {"name": "Charles Reiss", "role": "Primary"}
        ]
    },
    {
        "course_id": "MATH3350",
        "title": "Linear Algebra",
        "level": 300,
        "instructors": [
        {"name": "Jeff Holt", "role": "Primary"}
        ]
    }
]

# write to JSON file 
with open("raw_course_catalog.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4) #format nicely 

# load csv file 
df = pd.read_csv("raw_survey_data.csv")


# convert GPA/credits_taken to float 
df = df.astype({
    "GPA": "float64", 
    "credits_taken": "float64"
})

# convert is_cs_major to boolean
df["is_cs_major"] = df["is_cs_major"].replace({
    "Yes": True, 
    "No": False, 
}).astype(bool)

# save the cleaned dataframe into a new csv
df.to_csv("clean_survey_data.csv", index = False); #exclude index 

#load json file 
with open("raw_course_catalog.json", "r") as f:
    data = json.load(f)

#normalize nested instructors list
df = pd.json_normalize(
    data, 
    record_path=["instructors"], #expands each instructor entry 
    meta=["course_id", "title", "level"] #keep as columns
)

# save cleaned json into csv
df.to_csv("clean_course_catalog.csv", index=False)

# Part 3: the schema contract
