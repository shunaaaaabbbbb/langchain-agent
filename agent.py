from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults

from tools import get_custom_tools
from utils import get_prompt


def create_agent():
    # 検索ツールの設定
    search = TavilySearchResults(max_results=2)

    # カスタムツールの取得
    custom_tools = get_custom_tools()

    # すべてのツールを結合
    tools = [search] + custom_tools

    # モデルの初期化
    model = init_chat_model("gpt-4", model_provider="openai")

    # プロンプトの取得（ツールを渡す）
    prompt = get_prompt(tools)

    # エージェントの作成
    agent = create_tool_calling_agent(llm=model, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    return agent_executor


def get_agent_response(agent_executor, query):
    try:
        result = agent_executor.invoke({"input": query})
        # エージェントの出力を整形
        if "output" in result:
            # ツールの出力がそのまま返されている場合は、そのまま返す
            if isinstance(result["output"], str) and not result["output"].startswith(
                "Thought:"
            ):
                return result["output"]

            # エージェントの思考プロセスを含む場合は、最終的な回答のみを抽出
            output_lines = result["output"].split("\n")
            final_answer = None
            for line in reversed(output_lines):
                if line.startswith("Final Answer:"):
                    final_answer = line.replace("Final Answer:", "").strip()
                    break

            return final_answer if final_answer else result["output"]
        return "エージェントからの応答を取得できませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"
