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
        message = glm.Content(role=role, parts=[glm.Part(text=text,)])
        self._context.append(message)
    
    def get_context(self):
        return self._context
    
    