from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


search = TavilySearchResults(max_results=2)


loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()


retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",  # noqa: E501
)

tools = [search, retriever_tool]


model = init_chat_model("gpt-4", model_provider="openai")


model_with_tools = model.bind_tools(tools)


# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")


agent = create_tool_calling_agent(model, tools, prompt)


agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke(
    {"input": "Which team do you think will win in 2024-25 Final in NBA?"}
)

print(result)
