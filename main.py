import discord
from discord.ext import commands
from discord import app_commands
import cloudscraper
import json
import random
import asyncio
import os
from fake_useragent import UserAgent
from dotenv import load_dotenv

# .env inladen
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
server = os.getenv("DISCORD_SERVER")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Proxy gegevens
COUNTRY = 'US'
PROXY = f"http://customer-{username}-cc-{COUNTRY}:{password}@pr.oxylabs.io:7777"

# User agents, headers etc.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
]

ACCEPT_HEADERS = [
    "application/json, text/plain, */*",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
]

LANGUAGE_HEADERS = ["en-US,en;q=0.9", "en-GB,en;q=0.8"]

ENCODING_HEADERS = ["gzip, deflate, br", "identity"]

# Locatie json file
if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

# Deze functie slaat koppelt je epic-username aan je Discord-ID
def save_user_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# Deze functie laad de namen in uit de JSON file
def load_registered_names():
    if os.path.exists('user_data.json'):
        try:
            with open('user_data.json', 'r') as file:
                data = json.load(file)
                return list(data.values())
        except(FileNotFoundError, json.JSONDecodeError):
            return []
    return []

# Deze functie zorgt voor variatie in de headers
def get_random_headers():
    """
    Genereert random headers voor HTTP-verzoeken.
    """
    ua = UserAgent()
    return {
        "User-Agent": random.choice(USER_AGENTS + [ua.random]),  # Gebruik fake_useragent als extra variatie
        "Accept": random.choice(ACCEPT_HEADERS),
        "Accept-Language": random.choice(LANGUAGE_HEADERS),
        "Accept-Encoding": random.choice(ENCODING_HEADERS),
        "Connection": "keep-alive",
        "Referer": "https://rocketleague.tracker.network/",
        "Origin": "https://rocketleague.tracker.network",
        "DNT": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Cache-Control": "no-cache"
    }

# Deze functie haalt de standaard Rocket League ranks op
async def get_rocket_league_ranks(epic_username):
    headers = get_random_headers()
    
    sleep_time = random.uniform(1, 2)
    print(f"⏳ Wachten {sleep_time:.2f} seconden voordat we de API aanroepen...")
    await asyncio.sleep(sleep_time)

    scraper = cloudscraper.create_scraper()
    proxies = {
        "http": PROXY,
        "https": PROXY
    }
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/epic/{epic_username}"

    try:
        print(f"🔄 Using Oxylabs Proxy: {PROXY}")
        response = scraper.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an error for HTTP failures (403, 500, etc.)
        
        data = response.json()
        
    except json.JSONDecodeError:
        print("❌ JSON Decode Error: Invalid response from API")
        return None
    except Exception as e:
        print(f"❌ API Request Error: {e}")
        return None

    target_modes = ["Ranked Duel 1v1", "Ranked Doubles 2v2", "Ranked Standard 3v3"]
    ranks = []

    try:
        stats = data["data"]["segments"]

        for segment in stats:
            if segment["type"] == "playlist":
                gamemode = segment["metadata"]["name"]

                if gamemode in target_modes:
                    rank = segment["stats"]["tier"]["metadata"]["name"]
                    mmr = segment["stats"]["rating"]["value"]
                    division = segment["stats"]["division"]["metadata"]["name"]

                    ranks.append({
                        "playlist": gamemode,
                        "rank": rank,
                        "mmr": mmr,
                        "division": division
                    })

    except KeyError:
        return None
    
    return ranks if ranks else None

# Deze functie toont de extra ranks (Hoops, Rumble, Dropshot, Snow Day)
async def get_extra_rocket_league_ranks(epic_username):
    headers = get_random_headers()
    
    sleep_time = random.uniform(1, 2)
    print(f"⏳ Wachten {sleep_time:.2f} seconden voordat we de API aanroepen...")
    await asyncio.sleep(sleep_time)

    scraper = cloudscraper.create_scraper()
    proxies = {
        "http": PROXY,
        "https": PROXY
    }
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/epic/{epic_username}"

    try:
        print(f"🔄 Using Oxylabs Proxy: {PROXY}")
        response = scraper.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an error for HTTP failures (403, 500, etc.)
        
        data = response.json()
        
    except json.JSONDecodeError:
        print("❌ JSON Decode Error: Invalid response from API")
        return None
    except Exception as e:
        print(f"❌ API Request Error: {e}")
        return None

    target_modes = ["Hoops", "Rumble", "Dropshot", "Snow Day"]
    ranks = []

    try:
        stats = data["data"]["segments"]

        for segment in stats:
            if segment["type"] == "playlist":
                gamemode = segment["metadata"]["name"]

                if gamemode in target_modes:
                    rank = segment["stats"]["tier"]["metadata"]["name"]
                    mmr = segment["stats"]["rating"]["value"]
                    division = segment["stats"]["division"]["metadata"]["name"]

                    ranks.append({
                        "playlist": gamemode,
                        "rank": rank,
                        "mmr": mmr,
                        "division": division
                    })

    except KeyError:
        return None
    
    return ranks if ranks else None

# Deze functie haalt de statistieken op
async def get_player_statistics(epic_username):
    headers = get_random_headers()
    
    sleep_time = random.uniform(1, 2)
    print(f"⏳ Wachten {sleep_time:.2f} seconden voordat we de API aanroepen...")
    await asyncio.sleep(sleep_time)

    scraper = cloudscraper.create_scraper()
    proxies = {
        "http": PROXY,
        "https": PROXY
    }
    url = f"https://api.tracker.gg/api/v2/rocket-league/standard/profile/epic/{epic_username}"

    try:
        print(f"🔄 Using Oxylabs Proxy: {PROXY}")
        response = scraper.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an error for HTTP failures (403, 500, etc.)
        
        data = response.json()
        
    except json.JSONDecodeError:
        print("❌ JSON Decode Error: Invalid response from API")
        return None
    except Exception as e:
        print(f"❌ API Request Error: {e}")
        return None

    stats = {}

    try:

        for segment in data["data"]["segments"]:
                if segment["type"] == "overview":  # Algemene statistieken
                    stats = {
                        "goals": segment["stats"]["goals"]["value"],
                        "assists": segment["stats"]["assists"]["value"],
                        "mvps": segment["stats"]["mVPs"]["value"],
                        "saves": segment["stats"]["saves"]["value"],
                        "shots": segment["stats"]["shots"]["value"]
                    }

    except KeyError:
        return None
    
    return stats if stats else None

# Hiermee start de Discord bot
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object('824736705265270815')
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

# /commands syncen met discord
@client.event
async def on_ready():
    await client.tree.sync()  
    print(f'Bot is ready and synced globally!')

# Dit stuurt de bot wanneer hij een nieuwe server binnengaat
@client.event
async def on_guild_join(guild):
    channel = guild.system_channel or next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

    if channel:
        embed = discord.Embed(
            title="👋 Hallo Rocket League-spelers!",
            description=(
                "Ik ben **FlipReStat**, jouw persoonlijke Rocket League stat-tracker! 🚀\n"
                "Gebruik `/register` om je Epic-gebruikersnaam te koppelen.\n"
                "Gebruik `/rank-me` om je 1v1, 2v2 en 3v3 ranks te bekijken.\n"
                "Gebruik `/rank-player` om de ranks van een andere speler op te vragen.\n"
                "Gebruik `/rank-player-extra` voor extra modi: Hoops, Rumble, Dropshot & Snowday.\n"
                "Gebruik `/stats-player` om statistieken zoals goals, assists en saves te bekijken.\n"
                "Gebruik `/player-list` om de geregistreerde spelers in de server te zien.\n"
                "Type `/help` voor een overzicht van alle commands!"
            )
,
            color=0xf1c40f
        )
        embed.set_footer(text="✨ Ontwikkeld door Skywalker")

        with open("logo.png", "rb") as file:
            image_file = discord.File(file, filename='logo.png')
            embed.set_thumbnail(url="attachment://logo.png")

        await channel.send(embed=embed, file=image_file)

@client.tree.command(name='help', description='Bekijk alle beschikbare commands')
async def help(interaction: discord.Interaction):
    
    embed = discord.Embed(
        title="Hieronder vind je alle beschikbare commands van FlipReStat! 🚀",
        description=(
            "Gebruik `/register-rank` om je Epic-gebruikersnaam te koppelen.\n"
            "Gebruik `/rank-me` om je 1v1, 2v2 en 3v3 ranks te bekijken.\n"
            "Gebruik `/rank-player` om de ranks van een andere speler op te vragen.\n"
            "Gebruik `/rank-player-extra` voor extra modi: Hoops, Rumble, Dropshot & Snowday.\n"
            "Gebruik `/stats-player` om statistieken zoals goals, assists en saves te bekijken.\n"
            "Gebruik `/player-list` om de geregistreerde spelers in de server te zien.\n"
            "Type `/help` voor een overzicht van alle commands!"
            ),

        color=0x1abc9c

        )
    embed.set_footer(text="✨ Ontwikkeld door Skywalker")

    with open("logo.png", "rb") as file:
        image_file = discord.File(file, filename='logo.png')
        embed.set_thumbnail(url="attachment://logo.png")

    await interaction.response.send_message(embed=embed, file=image_file)

# Het commando om de Epic-username van de gebruiker in te stellen
@client.tree.command(name="register", description="Verbind je Epic-account met Discord!")
async def register_rank(interaction: discord.Interaction, epic_username: str):
    user_id = str(interaction.user.id)

    # Sla de Epic-username op in de dictionary (of een database)
    user_data[user_id] = epic_username

    save_user_data()

    await interaction.response.send_message(f"Je Epic-username **{epic_username}** is gekoppeld aan je account!", ephemeral=True)

# Commando om je eigen ranks op halen die gekoppeld zijn aan je discord-ID
@client.tree.command(name="rank-me", description="Check je ranks in 1v1, 2v2 en 3v3!")
async def rank_me(interaction: discord.Interaction):
    await interaction.response.defer()  # Zorgt ervoor dat de bot wat meer tijd heeft
    user_id = str(interaction.user.id)

    epic_username = user_data.get(user_id)

    if epic_username:
        rank_data = await get_rocket_league_ranks(epic_username)

        if rank_data:
            embed = discord.Embed(
                title=f"🏆 {epic_username}'s Rank",
                description="🔹 **Dit zijn je huidige ranks:**",
                color=0x1E90FF
            )

            for rank in rank_data:
                embed.add_field(
                    name=f"{rank['playlist']}",
                    value=f"**Rank:** {rank['rank']} | {rank['division']}\n**MMR:** {rank['mmr']}",
                    inline=False
                )
            embed.set_footer(text="🚀 Data afkomstig van Rocket League Tracker Network")

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Er zijn geen ranks gevonden voor deze Epic-username.", ephemeral=True)
    else:
        await interaction.followup.send("❌ Je hebt geen Epic-username gekoppeld. Gebruik `/register-rank` om je account te koppelen.", ephemeral=True)

# Commando om iemand zijn extra ranks te bekijken
@client.tree.command(name="rank-player-extra", description="Check je ranks in Hoops, Rumble, Dropshot en Snowday!")
async def get_extra_rank(interaction: discord.Interaction, epic_username: str):
    await interaction.response.defer()

    ranks = await get_extra_rocket_league_ranks(epic_username)

    if not ranks:
        await interaction.followup.send('❌ Kon de ranks niet ophalen. Controleer de naam!', ephemeral=True)
        return

    embed = discord.Embed(
        title=f"🏀 {epic_username}'s Rocket League Ranks",
        description="🔹 **Hier zijn de extra ranks van de speler:**",
        color=0xe74c3c
    )

    if isinstance(ranks, list) and len(ranks) > 0:
        for rank in ranks:
            playlist = rank.get("playlist", "Onbekend")
            rank_name = rank.get("rank", "Onbekend")
            mmr = rank.get("mmr", "N/A")
            division = rank.get("division", "N/A")

            embed.add_field(
                name=f"{playlist}",
                value=f"**Rank:** {rank_name} | {division}\n**MMR:** {mmr}",
                inline=False
            )
    else:
        embed.description += "\n❌ Geen ranks gevonden voor deze speler."

    embed.set_footer(text="🚀 Data afkomstig van Rocket League Tracker Network")

    await interaction.followup.send(embed=embed)

# Commando om iemand anders zijn ranks te bekijken
@client.tree.command(name='rank-player', description='Check de ranks van iemand in 1v1, 2v2 en 3v3!')
async def get_ranks(interaction: discord.Interaction, epic_username: str):
    await interaction.response.defer()

    ranks = await get_rocket_league_ranks(epic_username)

    if not ranks:
        await interaction.followup.send('❌ Kon de ranks niet ophalen. Controleer de naam!', ephemeral=True)
        return

    embed = discord.Embed(
        title=f"🏆 {epic_username}'s Rocket League Ranks",
        description="🔹 **Hier zijn de ranks van de speler:**",
        color=0x2ecc71
    )

    if isinstance(ranks, list) and len(ranks) > 0:
        for rank in ranks:
            playlist = rank.get("playlist", "Onbekend")
            rank_name = rank.get("rank", "Onbekend")
            mmr = rank.get("mmr", "N/A")
            division = rank.get("division", "N/A")

            embed.add_field(
                name=f"{playlist}",
                value=f"**Rank:** {rank_name} | {division}\n**MMR:** {mmr}",
                inline=False
            )
    else:
        embed.description += "\n❌ Geen ranks gevonden voor deze speler."

    embed.set_footer(text="🚀 Data afkomstig van Rocket League Tracker Network")

    await interaction.followup.send(embed=embed)

# Je statistieken opvragen
@client.tree.command(name='stats-player', description='Bekijk je persoonlijke Rocket League stats!')
async def get_player(interaction: discord.Interaction, epic_username: str):
    await interaction.response.defer()

    stats = await get_player_statistics(epic_username)

    if not stats:
        await interaction.followup.send('❌ Kon de stats niet ophalen. Controleer de naam!', ephemeral=True)
        return

    embed = discord.Embed(
        title=f"{epic_username}'s Player Stats",
        description="🔹 **Hier zijn de stats:**",
        color=0x9b59b6
    )

    stats_text = (
        f"⚽ **Goals:** {stats['goals']}\n"
        f"🎯 **Assists:** {stats['assists']}\n"
        f"🏅 **MVPs:** {stats['mvps']}\n"
        f"🛑 **Saves:** {stats['saves']}\n"
        f"🎯 **Shots:** {stats['shots']}\n"
    )

    embed.add_field(name="📊 **Algemene Statistieken**", value=stats_text, inline=False)

    embed.set_footer(text="🚀 Data afkomstig van Rocket League Tracker Network")

    await interaction.followup.send(embed=embed)

# Laat een lijst van alle geregistreerde spelers zien
@client.tree.command(name='player-list', description='Bekijk alle geregistreerde spelers in de server!')
async def get_player_list(interaction: discord.Interaction):
    names = load_registered_names()

    if not names:
        await interaction.response.send_message("Geen namen gevonden.", ephemeral=True)
        return
    
    name_list = "\n".join(f"🔹 {name}" for name in names)
    embed = discord.Embed(
        title="De geregistreerde epic-usernames in de server:",
        description=name_list,
        color=0xe67e22
    )
    
    await interaction.response.send_message(embed=embed)

client.run(token)