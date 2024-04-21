import google.generativeai as genai
from dotenv import load_dotenv
import os
from gemini_context_manager import GeminiContextManager
import re
from functions import *
import ast
import re

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro")

function_list = {
    "generate_schedule": {
        "description": """this function generates a schedule based on the input list of classes.
                          How to call: generate_schedule([~list of classes~])""",
        "function": generate_schedule,
    },
    "get_map_data": {
        "description": """this function gets the map data for the given class.
                    How to call: get_map_data([~list of classes~])""",
        "function": get_map_data,
    },
    "generate_professor_summary": {
        "description": """this function generates a summary of the professor based on the input professor name.
                                   How to call: generate_professor_summary("~name of the professor~")""",
        "function": generate_professor_summary,
    },
    "get_course_information": {
        "description": """this function gets the course information for the given class
                    How to call: get_course_information("~course name~")""",
        "function": get_course_information,
    },
    "get_sections_for_course": {
        "description": """this function gets the sections for the given course
                    How to call: get_sections_for_course("~course name~")""",
        "function": get_sections_for_course,
    },
    "get_suggestions":{
        "description": """this function gets the suggestions for the user based on the courses taken and the geneds fulfilled.
                    How to call: get_suggestions()""",
        "function": get_suggestions,
    },
    "general_chat": {
        "description": """this function is a general chat function that can be used to chat with the model.
                    This function will be called when the user request deos not match any of the available functions.
                    How to call: general_chat(~message~)""",
        "function": general_chat,
    },
}


def clean_response(response):
    parsed_response = re.search(r"(```(json)?\n)?(\{.+\})(\n```)?", response).group(3)
    if parsed_response is None:
        return response
    return parsed_response


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
            {{ "function": "get_map_data", "args": [["CMSC330_0101", "CMSC351_0104", "ENGL101_0201"]] }}
            {{ "function": "general_chat", "args": ["hello, how are you doing?"] }}
            {{ "function": "get_course_information", "args": ["CMSC330"] }}
            {{ "function": "get_sections_for_course", "args": ["CMSC330"] }}
            {{ "function": "generate_professor_summary", "args": ["Maksym Morawski"] }}

            
            !! Some of the Chat history are stored just for the sake of the context. Only the last message is used to generate the response. 
            !!IMPORTANT!! MAKE SURE TO FOLLOW THE FORMAT EXACTLY AS SHOWN ABOVE
            !!YOU MUST USE THE RESPONSE FORMAT ABOVE TO CALL THE FUNCTION. DO NOT RESPOND WITH NATURAL LANGUAGE!
            !!IMPORTANT!! DO NOT RESPOND SAYING YOU CANNOT HELP. JUST RESPOND WITH THE FUNCTION CALL.
            
            Here are the digest of what was happening between user and you before this message:
        """
        self.systemprompt_response = "Certainly, I can help with calling functions"

        self.context_manager.add_context("user", self.systemprompt)
        self.context_manager.add_context("model", self.systemprompt_response)

    def parse_query(self, input_text):
        response_type = None
        flat_context = self.context_manager.get_flat_context()
        self.context_manager.swap_system_message(
            self.systemprompt + str(flat_context), self.systemprompt_response
        )
        # print(self.context_manager.get_context())
        # print(self.context_manager.get_context())
        chat = model.start_chat(history=self.context_manager.get_context()[:2])
        response = chat.send_message(input_text).text
        print(response)
        response_dict = ast.literal_eval(response)
        # print(response_dict["args"])
        response, message, response_type = function_list[response_dict["function"]][
            "function"
        ](*response_dict["args"], self.context_manager)

        self.context_manager.add_context("user", input_text)
        self.context_manager.add_context("model", message)

        return response, response_type


if __name__ == "__main__":
    test_input = "hi, what can you do?"
    fc = FunctionCaller()
    print(
        fc.parse_query(
            "where are the classes for CMSC330 section 0101 and , CMSC351 section 0104 and , and ENGL 401?"
        )
    )
    # print(fc.parse_query("how are you doing?"))
