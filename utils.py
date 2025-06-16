from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_prompt(tools):
    prompt = ChatPromptTemplate.from_messages(
        [
            # システムメッセージ（AIの役割を定義）
            (
                "system",
                """あなたはNBAの試合データを提供するアシスタントです。
        以下のツールを使用できます：

        {tools}

        使用可能なツール: [{tool_names}]
        """,
            ),
            # ユーザー入力
            ("human", "{input}"),
            # エージェントの思考プロセス
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # ツールの情報を事前に設定
    tool_names = ", ".join([tool.name for tool in tools])
    tool_descriptions = "\n".join(
        [f"{tool.name}: {tool.description}" for tool in tools]
    )

    return prompt.partial(tool_names=tool_names, tools=tool_descriptions)
