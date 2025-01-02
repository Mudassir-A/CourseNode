from generating_embeddings.user_embedding import user_syllabus_embedding
from generating_embeddings.course_embedding import course_embedding
from user_syllabus_processing.extract_from_pdf import extract_module_content
from user_syllabus_processing.syllabus_preprocessing import preprocess_text
from similarity.matching import computing_similarity
from similarity.rating import rate_courses
from similarity.get_course import get_course_info
from similarity.get_course import load_csv
import csv
import json

file_name = "backend/artifacts/similarity.json"

pdf_path = "backend/artifacts/syllabus.pdf"
module_content = extract_module_content(pdf_path)
content = preprocess_text(module_content)#user pdf syllabus

content = user_syllabus_embedding(content)
with open("backend/data_scrape/cleaned_scraped.json" , 'r') as file:
  data = json.load(file) # nptel course data 

course_syllabus_embedding = course_embedding(data)

print(f" Course syllabus Embedding: {course_syllabus_embedding}")
print(f" User syllabus Embedding: {content}")

# computing similarity matching score of "user syllabus" with "all available nptel courses"
similarity_score = computing_similarity(content, course_syllabus_embedding)
print(similarity_score)
with open(file_name, "w") as f:
    f.write("")  # This clears the file

with open(file_name, "w") as f:
    json.dump(similarity_score, f, indent=4)  # Write new data with pretty formatting

print(f"Cleared and wrote new data to {file_name}")
top_8 = rate_courses(similarity_score)
print(f"Top 8 relevant courses: {top_8}")

course_data = load_csv("backend/data/processed/final_data.csv")

for course in top_8:
  course_id = course["course_id"]
  course_info = get_course_info(course_data, course_id)

  if course_info:
      print(f"Course Info: {course_info}")
  else:
      print(f"No course found with ID: {searched_course_id}")