import discord
from discord.ext import commands
from config import token  # импорт токена из файла конфигурации

intents = discord.Intents.default()
intents.members = True  # Необходимо для работы с пользователями и их баном
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Привет! Я бот для управления чатом.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Невозможно забанить пользователя с равным или более высоким рангом.")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Пользователь {member.name} был забанен.")
    else:
        await ctx.send("Эта команда должна указывать на пользователя, которого вы хотите забанить. Пример: `!ban @пользователь`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для выполнения этой команды.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Пользователь не найден.")

bot.run(token)