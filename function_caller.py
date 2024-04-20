import google.generativeai as genai
from dotenv import load_dotenv
import os
from gemini_context_manager import GeminiContextManager
import re
from functions import *
import ast

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
model = genai.GenerativeModel("gemini-pro",safety_settings=safety_settings)

function_list = {
    "generate_schedule": {"description": """this function generates a schedule based on the input list of classes.
                          How to call: generate_schedule([~list of classes~])""",
                          "function": generate_schedule}
}


context_manager = GeminiContextManager()
context_manager.add_context("user",f"""

[SYSTEM PRPMPT]
You are a function caller that parses natural language queries and calls the appropriate function.

The available functions are: {function_list.keys()}

The description of the functions are: {[f"{func}: {function_list[func]['description']}" for func in function_list.keys()]}

response format:
{{ "function": ~name of the function~, "args": [~list of arguments for the function here separated by comma~] }}

example:
{{ "function": "generate_schedule", "args": [["CMSC330", "CMSC351", "ENGL101"]] }}

!!IMPORTANT!! MAKE SURE TO FOLLOW THE FORMAT EXACTLY AS SHOWN ABOVE
!!IMPORTANT!! DO NOT RESPOND SAYING YOU CANNOT HELP. JUST RESPOND WITH THE FUNCTION CALL.
""")

context_manager.add_context("model","Certainly, I can help with calling functions")

def parse_query(input_text):
    chat = model.start_chat(history=context_manager.get_context())
    response = chat.send_message(input_text).text
    print(response)
    response_dict = ast.literal_eval(response)
    print(response_dict["args"])
    response = function_list[response_dict["function"]]["function"](*response_dict["args"])
    return response

if __name__ == "__main__":
    test_input = "make me a schedule from these classes: [CMSC330, CMSC351, ENGL101]"
    response = parse_query(test_input)
    response_dict = ast.literal_eval(response)
    print(response)
    function_list[response_dict["function"]]["function"](*response_dict["args"])

