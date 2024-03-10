import asyncio

import pandas as pd
import matplotlib.pyplot as plt

from src.services.db_service import fetch_player_answers, fetch_players_stats, fetch_connection_stats


async def draw_username_winrate(username, ax=None):
    """
    Plots a winrate statistics for given player.
    
    Parameters:
    -----------
    username : string from table Players.username
        Username of given player.
    
    ax : matplotlib axes object, default None
        An axes of the current figure
    """
    info = await fetch_player_answers(username)
    bins = pd.DataFrame([[info['LW'], info['LL']], 
                         [info['FW'], info['FL']], 
                         [info['HC'] + info['HW'], info['HD'] + info['HL']]], 
                        columns=['Wins', 'Loses'], 
                        index=['Liberal', 'Fascist', 'Hitler']).transpose()
    
    bins.plot(kind='bar', stacked=True, color=['deepskyblue', 'orangered', 'darkred'], rot='horizontal', ax=ax)