import glob

from canvasapi import Canvas
from getQuizResponses import *
from getStudents import *
from writeToCSV import write_students_to_csv,  write_responses_to_csv

# initializes a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_ID)

# just for test/debugging purposes
debug_on = False
if debug_on: print(course.name)

students = get_students(course)
if students:
    write_students_to_csv(students)

responses = get_responses(course)
write_responses_to_csv(responses)
