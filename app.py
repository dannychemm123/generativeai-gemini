from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai


load_dotenv()
env_var = os.getenv('GOOGLE_API_KEY')
if env_var is None:
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables.")
genai.configure(api_key=env_var)

def get_gemini_response(question, prompt):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate content using the model
        response = model.generate_content(prompt + question)
        
        # Return the response text
        return response.text
    
    except genai.api_core.exceptions.GoogleAPICallError as e:
        print(f"A Google API call error occurred: {e}")
        return None
    except genai.api_core.exceptions.RetryError as e:
        print(f"A retry error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Function to retrieve query from database
def read_sql_query(sql, db):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        rows = []
    finally:
        if con:
            con.close()
        return rows

prompt = """
You are an expert in converting complex English questions to SQL queries!
The SQL database has the name STUDENTS and has the following columns - NAME, CLASS, LEVEL, MARKS.

For example,

Example 1 - How many entries of records are present?
The SQL command will be something like this: SELECT COUNT(*) FROM STUDENTS;

Example 2 - List all student names.
The SQL command will be something like this: SELECT NAME FROM STUDENTS;

Example 3 - Find the number of students in each class.
The SQL command will be something like this: SELECT CLASS, COUNT(*) FROM STUDENTS GROUP BY CLASS;

Example 4 - Retrieve all information for students in level 'LEVEL 100'.
The SQL command will be something like this: SELECT * FROM STUDENTS WHERE LEVEL = 'LEVEL 100';

Example 5 - Get the names of students in class 'AI'.
The SQL command will be something like this: SELECT NAME FROM STUDENTS WHERE CLASS = 'AI';

Example 6 - Count the number of students in level 'LEVEL 300'.
The SQL command will be something like this: SELECT COUNT(*) FROM STUDENTS WHERE LEVEL = 'LEVEL 300';

Example 7 - Find the average marks of students in each class.
The SQL command will be something like this: SELECT CLASS, AVG(MARKS) FROM STUDENTS GROUP BY CLASS;

Example 8 - Retrieve the names and marks of students who have marks greater than 90.
The SQL command will be something like this: SELECT NAME, MARKS FROM STUDENTS WHERE MARKS > 90;

Example 9 - List the names of students in 'Data Science' class and 'Level 100'.
The SQL command will be something like this: SELECT NAME FROM STUDENTS WHERE CLASS = 'Data Science' AND LEVEL = 'Level 100';

Example 10 - Find the student with the highest marks.
The SQL command will be something like this: SELECT NAME, MARKS FROM STUDENTS WHERE MARKS = (SELECT MAX(MARKS) FROM STUDENTS);

also the sql code should not have ``` in beginning or end and sql word in output
"""

st.set_page_config(page_title="I Can Retrieve Any SQL Query")
st.header("Gemini App To Retrieve SQL Data")

# App description
st.write("""
Welcome to the Gemini SQL Query Generator! This app leverages the power of Google's Generative AI to convert your natural language questions into SQL queries.
Simply input your question in plain English, and our AI model will generate the corresponding SQL query, execute it on the student database, and return the results.
This tool is perfect for those who want to interact with databases without needing to write SQL queries manually.
""")

question = st.text_input("Input your question related to the student database:", key="input")
submit = st.button("Ask the Question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    if response:
        print(response)
        try:
            response = read_sql_query(response, "students.db")
            st.subheader("The Response is:")
            for row in response:
                print(row)
                st.write(row)
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            st.error(f"A database error occurred: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while executing the SQL query: {e}")
    else:
        st.error("Failed to generate a valid SQL query.")