import sqlite3


#Connect to SQLite database

connection = sqlite3.connect("students.db")

# Create a cursor object to insert records

cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE STUDENTS(NAME VARCHAR(30), CLASS VARCHAR(30), LEVEL VARCHAR(30),MARKS INT)
"""

cursor.execute(table_info)

try:
    cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, LEVEL, MARKS) VALUES (?, ?, ?, ?)", ('Daniel', 'Data Science', 'Level 100', 90))
    cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, LEVEL, MARKS) VALUES (?, ?, ?, ?)", ('Erica', 'Statistics', 'Level 300', 89))
    cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, LEVEL, MARKS) VALUES (?, ?, ?, ?)", ('Conti', 'Data Science', 'Level 400', 87))
    cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, LEVEL, MARKS) VALUES (?, ?, ?, ?)", ('KayBoat', 'AI', 'Level 100', 100))
    cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, LEVEL, MARKS) VALUES (?, ?, ?, ?)", ('Dan', 'Data Science', 'Level 200', 99))
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    connection.commit()

connection.commit()
print("The Inserted Records are : ")
data = cursor.execute("""SELECT * FROM STUDENTS""")
for row in data:
    print("{}".format(row))
    
connection.close()

# from dotenv import load_dotenv
# load_dotenv()
# import streamlit as st
# import os 
# import sqlite3
# import google.generativeai as genai

# # Configure api key
# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# # fuction to load google generativeai model

# def get_gemini_response(question, prompt):
#     try:
#         # Initialize the generative model
#         model = genai.GenerativeModel("gemini-pro")
        
#         # Generate content using the model
#         response = model.generate_content(prompt, question)
        
#         # Return the response text
#         return response.text
    
#     except Exception as e:
#         # Handle any exceptions that occur
#         print(f"An error occurred: {e}")
#         return None



# # fuction to retrieve query from database

# def read_sql_query(sql,db):
#     con = sqlite3.connect(db)
#     cur = con.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)
#     return rows


# prompt = """
# You are an expert in converting English questions to SQL query!
# The SQL database has the name STUDENT and has the following columns - NAME, CLASS, LEVEL.
# For example,

# Example 1 - How many entries of records are present?
# The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

# Example 2 - List all student names.
# The SQL command will be something like this: SELECT NAME FROM STUDENT;

# Example 3 - Find the number of students in each class.
# The SQL command will be something like this: SELECT CLASS, COUNT(*) FROM STUDENT GROUP BY CLASS;

# Example 4 - Retrieve all information for students in level 'LEVEL 100'.
# The SQL command will be something like this: SELECT * FROM STUDENT WHERE LEVEL = 'LEVEL 100';

# Example 5 - Get the names of students in class 'AI'.
# The SQL command will be something like this: SELECT NAME FROM STUDENT WHERE CLASS = 'AI';

# Example 6 - Count the number of students in level 'LEVEL 300'.
# The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT WHERE LEVEL = 'LEVEL 300';

# also the sql code should not have ``` in beginning or end and sql word in output
# """

# st.set_page_config(page_title = "I Can Retrive Any SQL Query")
# st.header("Gemini App To Retrive SQL Data")

# question = st.text_input("Input: ",key = "input")
# submit = st.button("Ask the Question")

# # If submit is clicked
# if submit:
#     response = get_gemini_response(question,prompt)
#     print(response)
#     response = read_sql_query(response,"students.db")
#     st.subheader("The Response is")
#     for row in response:
#         print(row)
#         st.header(row)