import asyncio
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring

import cairosvg
from telegram import Update
from telegram.ext import ContextTypes

import os
from collections import namedtuple
import tempfile
import cairosvg
import telegram
from telegram import Update
from telegram.ext import ContextTypes
import requests
from src import db
from src.data_models.Record import Record

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from collections import namedtuple

from src.data_models.Player import Player
from src.data_models.Record import Record

LIBERAL_COLOR = "#61C8D9"
LIBERAL_COLOR_STROKE = "#38586D"
FASCIST_COLOR = "#E66443"
FASCIST_COLOR_STROKE = "#7A1E16"

STROKE_SIZE = str(12)


def save_svg(svg_string, file_path):
    with open(file_path, "w") as file:
        file.write(svg_string)


def svg2png(svg_string) -> bytes:
    return cairosvg.svg2png(
        bytestring=svg_string,
        scale=1,
        output_width=1338 // 2,
        output_height=926 // 2,
        unsafe=True,
    )


def create_background(color):
    svg = Element(
        "svg",
        width="1338",
        height="926",
        viewBox="0 0 1338 926",
        fill=color,
        rx="6",
        id="background",
        xmlns="http://www.w3.org/2000/svg",
    )
    # background = SubElement(svg, 'rect', id="Shape", width="1338", height="926", rx="6", fill=color)
    return svg


def create_board(svg, board_type, players):
    if board_type == "Fascist":
        board = SubElement(svg, "g", id="F_BOARD_GROUP")
        x, y, width, height = "56", "518", "1226", "360"
        fill, stroke, stroke_width = FASCIST_COLOR, FASCIST_COLOR_STROKE, STROKE_SIZE
    else:  # Liberal
        board = SubElement(svg, "g", id="L_BOARD_GROUP")
        x, y, width, height = "56", "48", "1226", "360"
        fill, stroke, stroke_width = LIBERAL_COLOR, LIBERAL_COLOR_STROKE, STROKE_SIZE

    board_rect = SubElement(
        board,
        "rect",
        id=f"{board_type.upper()}_BOARD",
        x=x,
        y=y,
        width=width,
        height=height,
        rx="6",
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )

    name_rect = SubElement(
        board,
        "rect",
        id=f"{board_type.upper()}_BOARD_NAME",
        x=x,
        y=y,
        width=width,
        height="110",
        fill=fill,
        stroke=stroke,
        stroke_width=str(int(stroke_width) / 2),
        fill_opacity="0.6",
    )
    board_name_text = SubElement(
        board,
        "text",
        x=str(int(x) + int(width) / 2),
        y=str(int(y) + 55),
        font_size="60",
        fill="black",
        text_anchor="middle",
        dominant_baseline="middle",
    )
    board_name_text.text = board_type
    player_x = (
        int(x) + int(width) // 2 - (len(players) * 170 + (len(players) - 1) * 30) // 2
    )
    for i, player in enumerate(players):
        user_pic = SubElement(
            board,
            "image",
            href=player["user_profile_photo"],
            x=str(player_x),
            y=str(int(y) + 117),
            stroke=stroke,
            stroke_width=str(int(stroke_width) // 2),
            height="170",
            width="170",
        )
        username_rect = SubElement(
            board,
            "rect",
            id=f"username_{i}",
            x=str(player_x),
            y=str(int(y) + 288),
            stroke=stroke,
            stroke_width=str(int(stroke_width) // 2),
            width="170",
            height="55",
            fill="white",
        )
        username_text = SubElement(
            board,
            "text",
            x=str(player_x + 170 / 2),
            y=str(int(y) + 288 + 55 / 2),
            font_size="20",
            fill="black",
            text_anchor="middle",
            dominant_baseline="middle",
        )

        username_text.text = player["name"]
        player_x += 200  # Width 170 + 30 space


def create_result(svg, outcome):
    x, y, width, height = "56", "414", "1226", "98"
    result = SubElement(
        svg,
        "rect",
        id="RESULT",
        x=x,
        y=y,
        width=width,
        height=height,
        fill="white",
        fill_opacity="0.3",
    )
    result_text = SubElement(
        svg,
        "text",
        x=str(int(x) + int(width) / 2),
        y=str(int(y) + 55),
        fill="black",
        font_size="60",
        text_anchor="middle",
        dominant_baseline="middle",
    )
    result_text.text = outcome


def fix_python_wrong_svg_string(svg_string):
    """Fixes SVG string for compatibility and prettifies it."""
    replacements = {
        "text_anchor": "text-anchor",
        "dominant_baseline": "dominant-baseline",
        "font_size": "font-size",
        "stroke_width": "stroke-width",
    }
    for wrong, correct in replacements.items():
        svg_string = svg_string.replace(wrong, correct)
    return parseString(svg_string).toprettyxml()


def draw_game_result(players: tuple[dict], outcome: str):
    fascist_players = tuple(player for player in players if player["team"] == "Fascist")
    liberal_players = tuple(player for player in players if player["team"] == "Liberal")

    svg = create_background("#363835")
    create_board(svg=svg, board_type="Liberal", players=liberal_players)
    create_board(svg=svg, board_type="Fascist", players=fascist_players)
    create_result(svg=svg, outcome=outcome)

    svg = parseString(tostring(svg))
    svg = svg.toprettyxml()
    svg = fix_python_wrong_svg_string(svg)
    return svg


async def get_user_profile_photo(context, player_id) -> str:
    photo_objects = (
        await context.bot.get_user_profile_photos(player_id, limit=1, offset=0)
    ).photos[0]
    return (await context.bot.get_file(photo_objects[-1])).file_path


async def get_player(context, record: Record):
    """Get the player from the record"""
    return {
        "name": (
            await db.fetch_one(
                """SELECT full_name FROM players WHERE id = (?)""", [record.player_id]
            )
        )["full_name"],
        "role": record.role,
        "team": record.get_team(),
        "user_profile_photo": await get_user_profile_photo(context, record.player_id),
    }


async def draw_result_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    records: list[Record],
    result: str,
) -> bytes:
    """Send the result of the game to the chat"""
    # player = namedtuple("Player", ["name", "role", "team", "user_profile_photo"])
    players = tuple(
        await asyncio.gather(
            *[get_player(context=context, record=record) for record in records]
        )
    )
    svg = draw_game_result(players, result)
    return svg2png(svg)
