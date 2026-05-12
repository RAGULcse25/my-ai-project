# backend/agents/planner.py
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

class PlannerAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)

    def run(self, idea: str):
        prompt = PromptTemplate.from_template("""
        You are a senior software architect.
        Given this project idea: {idea}
        Generate:
        1. Tech stack
        2. File list with descriptions
        3. Step-by-step build plan
        Return as JSON.
        """)
        chain = prompt | self.llm
        return chain.invoke({"idea": idea})