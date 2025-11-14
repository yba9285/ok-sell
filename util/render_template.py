import jinja2
import aiofiles
import logging
from pyrogram import Client
from util.custom_dl import ByteStreamer

# --- LEGENDARY MODIFICATION: Create a dedicated renderer for the new player page ---
async def render_player_page(bot: Client, message_id: int):
    """
    Renders the new player.html template for the watch page.
    """
    
    # --- DECREED MODIFICATION: Use bot.app_url ---
    # bot.app_url is set in bot.py's __init__ and is already stripped of trailing slashes
    file_url = f"{bot.app_url}/stream/{message_id}"
    
    try:
        async with aiofiles.open('template/player.html', 'r') as f:
            template_content = await f.read()
        template = jinja2.Template(template_content)

        return template.render(
            file_url=file_url
        )
    except FileNotFoundError:
        logging.error("FATAL: player.html template not found in /template directory!")
        return "<html><body><h1>500 Internal Server Error</h1><p>Template file not found.</p></body></html>"
    except Exception as e:
        logging.error(f"Error rendering player template: {e}", exc_info=True)
        return "<html><body><h1>500 Internal Server Error</h1><p>Could not render template.</p></body></html>"


# The old render_page function is kept in case it's used elsewhere, but the new one is primary.
async def render_page(bot: Client, message_id: int):
    """
    Naye streaming engine ka istemal karke watch page ke liye HTML template render karta hai.
    """
    streamer = ByteStreamer(bot)
    file_name = "File"

    try:
        file_id = await streamer.get_file_properties(message_id)
        if file_id and file_id.file_name:
            file_name = file_id.file_name.replace("_", " ")

    except Exception as e:
        logging.error(f"Could not get file properties for watch page (message_id {message_id}): {e}")

    # --- DECREED MODIFICATION: Use bot.app_url ---
    stream_url = f"{bot.app_url}/stream/{message_id}"
    download_url = f"{bot.app_url}/download/{message_id}"
    
    try:
        async with aiofiles.open('template/watch_page.html', 'r') as f:
            template_content = await f.read()
        template = jinja2.Template(template_content)

        return template.render(
            heading=f"Watch {file_name}",
            file_name=file_name,
            stream_url=stream_url,
            download_url=download_url
        )
    except FileNotFoundError:
        logging.error("FATAL: watch_page.html template not found in /template directory!")
        return "<html><body><h1>500 Internal Server Error</h1><p>Template file not found.</p></body></html>"
    except Exception as e:
        logging.error(f"Error rendering template: {e}", exc_info=True)
        return "<html><body><h1>500 Internal Server Error</h1><p>Could not render template.</p></body></html>"
