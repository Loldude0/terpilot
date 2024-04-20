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
        
model = genai.GenerativeModel("gemini-pro")

function_list = {
    "generate_schedule": {"description": """this function generates a schedule based on the input list of classes.
                          How to call: generate_schedule([~list of classes~])""",
                          "function": generate_schedule},
    "general_chat": {"description": """this function is a general chat function that can be used to chat with the model.
                    This function will be called when the user request deos not match any of the available functions.
                    How to call: general_chat(~message~)""",
                    "function": general_chat}
}

class FunctionCaller:
    def __init__(self):
        self.context_manager = GeminiContextManager()
        self.systemprompt = f"""

[SYSTEM PRPMPT]
You are a function caller that parses natural language queries and calls the appropriate function to help the user.
Your job is to call the function, and each function will do the rest of the work.

The available functions are: {function_list.keys()}

The description of the functions are: {[f"{func}: {function_list[func]['description']}" for func in function_list.keys()]}

RESPONSE FORMAT:
{{ "function": ~name of the function~, "args": [~list of arguments for the function here separated by comma~] }}

example:
{{ "function": "generate_schedule", "args": [["CMSC330", "CMSC351", "ENGL101"]] }}

!!IMPORTANT!! MAKE SURE TO FOLLOW THE FORMAT EXACTLY AS SHOWN ABOVE
!!YOU MUST USE THE RESPONSE FORMAT ABOVE TO CALL THE FUNCTION. DO NOT RESPOND WITH NATURAL LANGUAGE!
!!IMPORTANT!! DO NOT RESPOND SAYING YOU CANNOT HELP. JUST RESPOND WITH THE FUNCTION CALL.
"""
        self.systemprompt_response = "Certainly, I can help with calling functions"
        
        self.context_manager.add_context("user",self.systemprompt)
        self.context_manager.add_context("model",self.systemprompt_response)

    def parse_query(self,input_text):
        self.context_manager.swap_system_message(self.systemprompt,self.systemprompt_response)
        #print(self.context_manager.get_context())
        chat = model.start_chat(history=self.context_manager.get_context())
        response = chat.send_message(input_text).text
        #print(response)
        response_dict = ast.literal_eval(response)
        #print(response_dict["args"])
        response,message = function_list[response_dict["function"]]["function"](*response_dict["args"],self.context_manager)
        
        self.context_manager.add_context("user",input_text)
        self.context_manager.add_context("model",message)
        
        return response

if __name__ == "__main__":
    test_input = "hi, what can you do?"
    fc = FunctionCaller()
    print(fc.parse_query("can you help me with making a ldcass schedule? I want to take CMSC330, CMSC420, and ENGL101 next semester"))
    print(fc.parse_query("how are you doing?"))
    

