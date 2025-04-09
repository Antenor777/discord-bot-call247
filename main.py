import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_ID = 123456789012345678  # Substituído pelo seu ID real

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    for guild in bot.guilds:
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect()
                print(f"🎧 Conectado automaticamente ao canal: {channel.name}")
            except:
                print("⚠️ Já conectado ou falha ao conectar.")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        await ctx.send(f"✅ Entrei no canal: {channel.name}")
    else:
        await ctx.send("❌ Você precisa estar em um canal de voz para usar este comando.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Saí do canal de voz.")
    else:
        await ctx.send("❌ Não estou em nenhum canal de voz.")

@bot.command(name="mute")
async def mute(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("🔇 Bot mutado.")
    else:
        await ctx.send("❌ Nada está sendo reproduzido.")

@bot.command(name="unmute")
async def unmute(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("🔊 Bot desmutado.")
    else:
        await ctx.send("❌ Nada está pausado.")

@bot.command(name="forcejoin")
@commands.has_permissions(administrator=True)
async def forcejoin(ctx):
    channel = ctx.guild.get_channel(VOICE_CHANNEL_ID)
    if channel:
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"✅ Conectado ao canal de voz: {channel.name}")
    else:
        await ctx.send("❌ Canal não encontrado.")

bot.run(os.getenv("DISCORD_TOKEN"))
