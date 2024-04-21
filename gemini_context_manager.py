import google.generativeai as genai
from dotenv import load_dotenv
import google.ai.generativelanguage as glm
from google.generativeai.types.content_types import *
import os

class GeminiContextManager:
    def __init__(self):
        load_dotenv()
        self._context = []
    
    def add_context(self,role,text):
        self._context.append((role,text))
    
    def get_context(self):
        result = []
        for (role,text) in self._context:
            result.append(glm.Content(role=role, parts=[glm.Part(text=text,)]))
        return result
    
    def swap_system_message(self,systemprompt, modelresponse):
        self._context[0] = ("user",systemprompt)
        self._context[1] = ("model",modelresponse)
    
    def get_flat_context(self):
        if len(self._context) < 2:
            return []
        else:
            return self._context[2:]
    
    