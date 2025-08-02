from Model_File import create_model

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser


def file_type_detector(input_text):
    identifying_llm = create_model()

    system_message = SystemMessagePromptTemplate.from_template(
        "You are a strict classifier that returns only the type of data source in one word: PDF, CSV, EXCEL, TEXT, or LINK. "
        "If the input is a pure web link then return LINK. "
        "If the input is a web link but is ending with extensions like .csv, .xlsx, etc., then return the extension."
        "Do not return BLOG, ARTICLE, or any other type. Return only: PDF, CSV, EXCEL, TEXT, or LINK."
    )
    human_message = HumanMessagePromptTemplate.from_template("{input}")
    
    prompt_to_identify = ChatPromptTemplate.from_messages([system_message, human_message])
    
    parser_to_identify = StrOutputParser()
    
    identifying_agent = prompt_to_identify | identifying_llm | parser_to_identify

    file_type = identifying_agent.invoke({"input": input_text})

    return file_type


