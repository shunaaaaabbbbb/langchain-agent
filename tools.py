from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.tools import ToolException
from nba_api.stats.endpoints import LeagueGameLog
from pydantic import BaseModel, Field


class GameDateInput(BaseModel):
    date: str = Field(
        description="試合日(YYYY-MM-DD形式、例: 2025-06-13)。指定がない場合は最新の試合データを返します。",  # noqa: E501
        default=None,
    )


class FetchRSGameDataEngine(BaseTool):
    name: str = "get_nba_rs_game_data"
    description: str = """NBAのレギュラーシーズンの試合情報を取得します。
    日付を指定すると、その日の試合データを返します。
    日付を指定しない場合は、最新の試合データを返します。
    返り値には以下の情報が含まれます：
    - 試合日(GAME_DATE)
    - チーム名(TEAM_NAME)
    - 対戦相手(MATCHUP)
    - 勝敗(WL)
    - 得点(PTS)
    - その他の統計データ
    """
    args_schema: Type[BaseModel] = GameDateInput

    def _run(self, date: Optional[str] = None) -> str:
        try:
            df = LeagueGameLog(season_type_all_star="Regular Season").get_data_frames()[
                0
            ]

            if date:
                # 日付でフィルタリング
                game_data = df[df["GAME_DATE"] == date]
                if game_data.empty:
                    return f"{date}の試合データは見つかりませんでした。"
            else:
                # 最新の試合データを取得
                game_data = df.iloc[-1:]

            # データを整形して返す
            result = []
            for _, row in game_data.iterrows():
                game_info = (
                    f"試合日: {row['GAME_DATE']}\n"
                    f"チーム: {row['TEAM_NAME']}\n"
                    f"対戦: {row['MATCHUP']}\n"
                    f"勝敗: {row['WL']}\n"
                    f"得点: {row['PTS']}\n"
                    f"FG: {row['FGM']}/{row['FGA']} ({row['FG_PCT']:.3f})\n"
                    f"3P: {row['FG3M']}/{row['FG3A']} ({row['FG3_PCT']:.3f})\n"
                    f"FT: {row['FTM']}/{row['FTA']} ({row['FT_PCT']:.3f})\n"
                    f"リバウンド: {row['REB']} (オフェンス: {row['OREB']}, ディフェンス: {row['DREB']})\n"  # noqa: E501
                    f"アシスト: {row['AST']}\n"
                    f"スティール: {row['STL']}\n"
                    f"ブロック: {row['BLK']}\n"
                    f"ターンオーバー: {row['TOV']}\n"
                    f"ファウル: {row['PF']}\n"
                    f"プラスマイナス: {row['PLUS_MINUS']}"
                )
                result.append(game_info)

            return "\n\n".join(result)

        except Exception as e:
            raise ToolException(f"Failed to fetch game data: {e}")

    async def _arun(self, date: Optional[str] = None) -> str:
        return self._run(date)


class FetchPOGameDataEngine(BaseTool):
    name: str = "get_nba_po_game_data"
    description: str = """NBAのプレイオフの試合情報を取得します。
    日付を指定すると、その日の試合データを返します。
    日付を指定しない場合は、最新の試合データを返します。
    返り値には以下の情報が含まれます：
    - 試合日(GAME_DATE)
    - チーム名(TEAM_NAME)
    - 対戦相手(MATCHUP)
    - 勝敗(WL)
    - 得点(PTS)
    - その他の統計データ
    """
    args_schema: Type[BaseModel] = GameDateInput

    def _run(self, date: Optional[str] = None) -> str:
        try:
            df = LeagueGameLog(season_type_all_star="Playoffs").get_data_frames()[0]

            if date:
                # 日付でフィルタリング
                game_data = df[df["GAME_DATE"] == date]
                if game_data.empty:
                    return f"{date}の試合データは見つかりませんでした。"
            else:
                # 最新の試合データを取得
                game_data = df.iloc[-1:]

            # データを整形して返す
            result = []
            for _, row in game_data.iterrows():
                game_info = (
                    f"試合日: {row['GAME_DATE']}\n"
                    f"チーム: {row['TEAM_NAME']}\n"
                    f"対戦: {row['MATCHUP']}\n"
                    f"勝敗: {row['WL']}\n"
                    f"得点: {row['PTS']}\n"
                    f"FG: {row['FGM']}/{row['FGA']} ({row['FG_PCT']:.3f})\n"
                    f"3P: {row['FG3M']}/{row['FG3A']} ({row['FG3_PCT']:.3f})\n"
                    f"FT: {row['FTM']}/{row['FTA']} ({row['FT_PCT']:.3f})\n"
                    f"リバウンド: {row['REB']} (オフェンス: {row['OREB']}, ディフェンス: {row['DREB']})\n"  # noqa: E501
                    f"アシスト: {row['AST']}\n"
                    f"スティール: {row['STL']}\n"
                    f"ブロック: {row['BLK']}\n"
                    f"ターンオーバー: {row['TOV']}\n"
                    f"ファウル: {row['PF']}\n"
                    f"プラスマイナス: {row['PLUS_MINUS']}"
                )
                result.append(game_info)

            return "\n\n".join(result)

        except Exception as e:
            raise ToolException(f"Failed to fetch game data: {e}")

    async def _arun(self, date: Optional[str] = None) -> str:
        return self._run(date)


def get_custom_tools():
    return [
        FetchRSGameDataEngine(),
        FetchPOGameDataEngine(),
    ]
