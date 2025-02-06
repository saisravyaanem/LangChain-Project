import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)


def lookup(name : str)->str:
    llm=ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo",
                   openai_api_key="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")
    template="""given the URL{name_of_person} I want to get it me a latest stocks she bought.
    Analyse her stock buying process"""
    
    prompt_template=PromptTemplate(template=template,input_variables=["name_of_person"])
    tools_for_agent=[
        Tool(
            name="Crawl Google 4 Stocks Bought pages",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Stocks bought",
        )
    ]
    
    react_prompt=hub.pull("hwchase17/react")
    agent=create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor=AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True,handle_parsing_errors=True)
    
    result=agent_executor.invoke(
        input={"input":prompt_template.format_prompt(name_of_person=name)}
    )
    linked_profile_url=result
    return linked_profile_url



if __name__ == "__main__":
    print(lookup(name="https://www.quiverquant.com/congresstrading/politician/Nancy%20Pelosi-P000197"))
    
    