import os
import asyncio
import disnake
import yt_dlp as youtube_dl
from disnake.ext import commands

from playlist import Playlist
playlist = Playlist()

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

FFMPEG_PATH = "./ffmpeg/ffmpeg/bin/ffmpeg.exe"
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    'executable': FFMPEG_PATH  # Use the local FFmpeg binary
}

youtube_dl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True
}

@bot.event
async def on_ready():
    print(f'{bot.user} is READY!')
    await bot.change_presence(activity=disnake.Game("running some shit ass code"))

@bot.event
async def on_message(message):
    if message.content.startswith("!"):
        return

    if message.author == bot.user:
        return
    
    sounds = os.listdir("sounds")
    for sound in sounds:
        if sound.split(".mp3")[0] == message.content:
            sound_path = os.path.join("sounds", sound)
            source = disnake.FFmpegPCMAudio(sound_path, executable=FFMPEG_PATH, options=FFMPEG_OPTIONS)
            
            if message.author.voice:
                channel = message.author.voice.channel
                voice_client = disnake.utils.get(bot.voice_clients, channel=channel)
                if voice_client is None:
                    voice_client = await channel.connect()
                    voice_client.play(source)
            else:
                await message.reply("You're not in a voice channel!")


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()

@bot.command()
async def leave(ctx):
    if ctx.author.id == 172810582230040577:
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        else:
            ctx.send(f"You're not in a voice channel!")

@bot.command()
async def get_out(ctx):
    source = disnake.FFmpegPCMAudio("get out.mp3", executable=FFMPEG_PATH, options=FFMPEG_OPTIONS)
    ctx.voice_client.play(source)

@bot.command()
async def play(ctx, url: str):
    """Play a YouTube video's audio in the voice channel."""
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You need to join a voice channel first.")
            return
        
        song_data = get_video_data(url)
        if not ctx.voice_client.is_playing():
            source = disnake.FFmpegPCMAudio(song_data["audio_url"], executable=FFMPEG_PATH, options=FFMPEG_OPTIONS)
            ctx.voice_client.play(source)
            await ctx.send(f"Now playing: [{song_data["video_title"]}]({song_data["video_url"]})")
            await ctx.send(f"Requested by: {ctx.author}")
        else:
            playlist.add_to_queue(ctx.author, song_data["video_title"], song_data["video_url"], song_data["audio_url"])

# def after_play():
#     if playlist.get_queue_length() > 0:


@bot.command()
async def stop(ctx):
    """Stop the currently playing audio."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Stopped playing.")
    else:
        await ctx.send("There is no audio playing.")

@bot.command()
async def queue(ctx):
    """Get the current queue"""

def get_video_data(url):
    with youtube_dl.YoutubeDL(youtube_dl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', None)

        for ydl_format in info['formats']:
            if ydl_format['format_id'] == '251':
                audio_url = ydl_format['url']
                data = {
                    'video_url': url,
                    'audio_url': audio_url,
                    'video_title': video_title
                }
                return data

TOKEN = "MTA5MDkzMDk3OTUxNTkzNjc4OA.GP7n3G.4FA0Flwrk-I14Vzzih99e0ZbkVyPVR83zh4JU0"
bot.run(TOKEN)