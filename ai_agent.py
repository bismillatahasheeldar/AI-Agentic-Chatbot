# step1:setup api keys for grog openai and tavily
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

#step2 setup LLM and TOOLS
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_tavily import TavilySearchResults

from langchain_community.tools.tavily_search import TavilySearchResults


openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearchResults(max_results=2)   

#Step3 setup ai agent with search tool functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)    

    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent=create_react_agent(
        model=llm,
        tools=tools,
        # state_modifier=system_prompt
    )

    # query="tell me about the trends in crypto markets"
    state={"messages":query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message,AIMessage)]
    return ai_messages[-1]
