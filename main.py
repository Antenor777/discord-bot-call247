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

# ID do canal de voz onde o bot deve sempre entrar
VOICE_CHANNEL_ID = 123456789012345678  # <--- substitua pelo ID do seu canal

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

    # Tenta conectar no canal de voz automaticamente
    for guild in bot.guilds:
        channel = guild.get_channel(1359032707379630191)
        if channel:
            try:
                await channel.connect()
                print(f"🎧 Conectado automaticamente no canal: {channel.name}")
            except Exception as e:
                print(f"❌ Erro ao conectar no canal de voz: {e}")

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

@bot.command(name="mute")
async def mute(ctx):
    if ctx.voice_client:
        await ctx.guild.change_voice_state(channel=ctx.voice_client.channel, self_mute=True)
        await ctx.send("🔇 Bot mutado.")
    else:
        await ctx.send("❌ O bot não está em call.")

@bot.command(name="unmute")
async def unmute(ctx):
    if ctx.voice_client:
        await ctx.guild.change_voice_state(channel=ctx.voice_client.channel, self_mute=False)
        await ctx.send("🔊 Bot desmutado.")
    else:
        await ctx.send("❌ O bot não está em call.")

# Se for desconectado da call, tenta voltar
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != bot.user.id:
        return

    if before.channel and after.channel is None:
        channel = member.guild.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                await channel.connect()
                print(f"🔁 Bot reconectado automaticamente ao canal: {channel.name}")
            except Exception as e:
                print(f"❌ Erro ao reconectar: {e}")

# Inicia o bot
bot.run(os.getenv("DISCORD_TOKEN"))
