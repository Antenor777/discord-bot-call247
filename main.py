import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = ctx.voice_client

        if vc is not None:
            await vc.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f"🎧 Entrei no canal de voz: {channel.name}")
    else:
        await ctx.send("❌ Você precisa estar em um canal de voz para eu entrar!")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Saí do canal de voz.")
    else:
        await ctx.send("❌ Não estou em nenhum canal de voz.")

bot.run(os.getenv("DISCORD_TOKEN"))
