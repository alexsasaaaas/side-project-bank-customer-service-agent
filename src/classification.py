from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .config import CLASSIFICATION_PROMPT_TEMPLATE

def build_classification_chain(llm):
    """
    建置分類chain
    """
    prompt = PromptTemplate.from_template(CLASSIFICATION_PROMPT_TEMPLATE)
    return prompt | llm | JsonOutputParser()