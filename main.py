import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Intents necessários
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

# Prefixo e inicialização do bot
bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_NAME = "🔧 • suporte"

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    for guild in bot.guilds:
        channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)
        if channel:
            try:
                await channel.connect()
                print(f"🎧 Conectado automaticamente no canal: {channel.name}")
            except:
                print("⚠️ Já conectado ou falha ao conectar.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Saí do canal de voz.")
    else:
        await ctx.send("❌ Não estou em nenhum canal de voz.")

@bot.command(name="mute")
async def mute(ctx):
    if ctx.voice_client:
        ctx.voice_client.pause()
        await ctx.send("🔇 Bot mutado.")
    else:
        await ctx.send("❌ Não estou em um canal de voz.")

@bot.command(name="unmute")
async def unmute(ctx):
    if ctx.voice_client:
        ctx.voice_client.resume()
        await ctx.send("🔊 Bot desmutado.")
    else:
        await ctx.send("❌ Não estou em um canal de voz.")

@bot.command(name="forcejoin")
@commands.has_permissions(administrator=True)
async def forcejoin(ctx):
    guild = ctx.guild
    channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)

    if channel:
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"✅ Conectado ao canal de voz: {channel.name}")
    else:
        await ctx.send("❌ Canal não encontrado.")

# Inicia o bot
bot.run(os.getenv("DISCORD_TOKEN"))
