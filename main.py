import discord
from discord.ext import commands
import re  # Mengimpor modul regular expression
from config import BOT_TOKEN, PREFIX
from animemanga import fetch_anime_data, fetch_manga_data, format_date, rgb_to_int

# Mengatur intents agar bot dapat membaca konten pesan
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Fungsi untuk membersihkan HTML tags
def clean_html(text):
    """Membersihkan tag HTML seperti <br>, <i>, <b> dan simbol seperti '*'."""
    text = re.sub(r'<br\s*/?>', '\n', text)  # Mengganti <br> dengan newline
    text = re.sub(r'<i>', '', text)          # Menghapus tag <i>
    text = re.sub(r'</i>', '', text)         # Menghapus tag </i>
    text = re.sub(r'<b>', '', text)          # Menghapus tag <b>
    text = re.sub(r'</b>', '', text)         # Menghapus tag </b>
    text = re.sub(r'\*', '', text)           # Menghapus simbol *
    text = re.sub(r'\n+', '\n', text)        # Mengganti multiple newlines dengan satu newline
    return text

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def anime(ctx, *, title: str):
    data = fetch_anime_data(title)
    if not data:
        await ctx.send("Anime tidak ditemukan.")
        return
    
    format_type = data['type'].capitalize() if data['type'] else "-"
    start_date = format_date(data['startDate'])
    end_date = format_date(data['endDate'])
    date = f"{start_date} - {end_date}"
    
    # Menentukan status
    status = data.get('status', 'Unknown').capitalize()
    if status == 'Finished airing':
        status = 'Finished'
    elif status == 'Currently airing':
        status = 'Releasing'
    
    # Menangani kemungkinan deskripsi None
    description = clean_html(data['description']) if data['description'] else "No description available."
    
    # Menentukan jumlah episode yang sudah ditayangkan
    total_episodes = data['episodes'] or '-'
    if status == 'Releasing' and 'episodesAired' in data:
        total_episodes = data['episodesAired']
    
    embed = discord.Embed(title=data['title']['romaji'], color=discord.Color(rgb_to_int(data['dominantColor'])))
    embed.set_thumbnail(url=data.get('coverImage', {}).get('large', ''))
    
    # Menambahkan deskripsi tanpa judul, hanya isinya
    embed.add_field(name="Format", value=format_type, inline=True)
    embed.add_field(name="Total Episode", value=total_episodes, inline=True)
    embed.add_field(name="Status", value=status, inline=True)  # Status di atas Date
    embed.add_field(name="Date", value=date, inline=True)  # Date di bawah Status
    embed.add_field(name="Genre", value=", ".join(data['genres']), inline=False)
    embed.add_field(name="Average Score", value=data['averageScore'], inline=True)
    embed.add_field(name="Ranking", value=data['rankings'][0]['rank'] if data['rankings'] else "-", inline=True)
    
    # Menambahkan deskripsi sebagai field dengan hanya kontennya
    embed.description = description
    
    await ctx.send(embed=embed)

@bot.command()
async def manga(ctx, *, title: str):
    data = fetch_manga_data(title)
    if not data:
        await ctx.send("Manga tidak ditemukan.")
        return
    
    format_type = data['type'].capitalize() if data['type'] else "-"
    start_date = format_date(data['startDate'])
    end_date = format_date(data['endDate'])
    date = f"{start_date} - {end_date}"
    
    # Menentukan status
    status = data.get('status', 'Unknown').capitalize()
    if status == 'Finished':
        status = 'Finished'
    elif status == 'Publishing':
        status = 'Releasing'
    
    # Menangani kemungkinan deskripsi None
    description = clean_html(data['description']) if data['description'] else "No description available."
    
    embed = discord.Embed(title=data['title']['romaji'], color=discord.Color(rgb_to_int(data['dominantColor'])))
    embed.set_thumbnail(url=data.get('coverImage', {}).get('large', ''))
    
    # Menambahkan deskripsi tanpa judul, hanya isinya
    embed.add_field(name="Format", value=format_type, inline=True)
    embed.add_field(name="Total Chapters", value=data['chapters'] or "-", inline=True)
    embed.add_field(name="Status", value=status, inline=True)  # Status di atas Date
    embed.add_field(name="Date", value=date, inline=True)  # Date di bawah Status
    embed.add_field(name="Genre", value=", ".join(data['genres']), inline=False)
    embed.add_field(name="Average Score", value=data['averageScore'], inline=True)
    embed.add_field(name="Ranking", value=data['rankings'][0]['rank'] if data['rankings'] else "-", inline=True)
    
    # Menambahkan deskripsi sebagai field dengan hanya kontennya
    embed.description = description
    
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
