import io
import skimage
import asyncio
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib import image
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)#The OffsetBox is a simple container artist.
from telegram.ext import ContextTypes
from src.services.db_service import fetch_user, fetch_player_answers, fetch_players_stats, fetch_connection_stats
from src.services.draw_result_image import get_user_profile_photo, svg2png


async def draw_user_winrate_bins(user_id, ax=None, return_bins=False):
    """
    Plots a winrate statistics for given player.
    
    Parameters:
    -----------
    user_id : int from table Players.id
        Id of a given player.
    
    ax : matplotlib axes object, default None
        An axes of the current figure
        
    Returns:
    --------
        bins : pd.DataFrame
    """
    info = await fetch_player_answers(user_id)
    bins = pd.DataFrame([[info['LW'], info['LL']], 
                         [info['FW'], info['FL']], 
                         [info['HC'] + info['HW'], info['HD'] + info['HL']]], 
                        columns=['Wins', 'Loses'], 
                        index=['Liberal', 'Fascist', 'Hitler']).transpose()
    
    bins.plot(kind='bar', stacked=True, color=['deepskyblue', 'orangered', 'darkred'], rot='horizontal', ax=ax)
    if return_bins:
        return bins
    
    
    
async def draw_user_winrate(user_id, outcome=None, context=ContextTypes.DEFAULT_TYPE):
    """
    Draw a winrate statistics for given player and saves this as svg
    
    Parameters:
    -----------
    user_id : int from table Players.id
        Id of a given player.
    
    outcome: str
        Outcome file name
        Returns svg-string if this is None
    
    context : telegram.ext.CallbackContext
    """
    user = await fetch_user(id=user_id)
    
    fig, ax = plt.subplots(1, 1)
    fig.set_figwidth(8)
    fig.set_figheight(6)
    fig.suptitle(user['full_name'])
    
    # Define a logo (an avatar) position
    bins = await draw_user_winrate_bins(user_id, ax=ax, return_bins=True)
    heights = bins.sum(axis=1)
    if heights['Wins'] < 0.66*heights['Loses']:
        ab_posx = 0
    elif heights['Loses'] < 0.66*heights['Wins']:
        ab_posx = 1
    else:
        ab_posx = 0.5
    ab_posy = 0.85*heights.max()
    
    # Set a logo (an avatar)
    photo_path = await get_user_profile_photo(context=context, player_id=user_id)
    logo = skimage.io.imread(photo_path)
    zoom = 90/logo.shape[1]
    imagebox = OffsetImage(logo, zoom=zoom)
    ab = AnnotationBbox(imagebox, (ab_posx, ab_posy), frameon = True)
    ax.add_artist(ab)

    if not (outcome is None):
        fig.savefig(outcome)
    else:
        svg = io.StringIO()
        fig.savefig(svg, format='svg')
        svg = svg.getvalue()
        return svg2png(svg)