
import discord
from discord.ext import commands

from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(command_prefix = 'k!', intents=intents)
client.remove_command('help')


@client.command()
async def social(ctx,member: discord.Member = None):
    embed = discord.Embed(
        title="Наши социальные сети",
        description="Все полезные ссылки вы можете найти здесь https://linktr.ee/fksis",
        url="https://linktr.ee/fksis",
        color=discord.Color.yellow()
    )
    embed.set_image(url = "attachment://dsd.png")     
       
    await ctx.send(file = discord.File("dsd.png"), embed = embed)

@client.command()
async def rules(ctx):
    embed = discord.Embed(
        title = "Правила сервера",
        description = """1.1 Запрещено деструктивное поведение и провокационные действия по отношению к сообществу.
        1.2 Запрещено мнимое присвоение полномочий представителей сообщества.
        1.3 Запрещено разведение конфликтных ситуаций и поведение не соответствующее социальным нормам. 
        1.4 Запрещены угрозы расправы и причинения какого-либо ущерба в реальной жизни, а также шантаж различного вида.
        1.5 Запрещено распространение персональных данных и сопутствующая травля характерного направления. 
        1.6 Запрещены попытки обхода полученных наказаний, функциональных ограничений и установленных правил.
        1.7 Запрещены провокационные и подталкивающие действия к нарушениям установленных правил.
        1.8 Запрещено обсуждение политических и межрасовых тематик, а также разведение межнациональных конфликтов.
        1.9 Запрещено мошенничество и умышленный ввод в заблуждение ради личной выгоды или выгоды третьего лица.
        1.10 Запрещено распространение вредоносных ссылок, файлов и программного обеспечения.
        1.11 Запрещена публикация приглашений и ссылок на сторонние сервера Discord, различные ресурсы или сервисы, не относящиеся к сообществу.
        1.12 Запрещено размещение и использование материалов экстремистской, расистской, фашистской или порнографической тематики.
        1.13 Запрещён спам, мат, дублирование своих или сторонних сообщений, а также злоупотребление верхним регистром и символами.
        
        Будьте вежливы и уважайте других!""",
        color=discord.Color.yellow()
    )
    
    await ctx.send(embed = embed)

client.run("MTEwOTA5NjE4NjA5MjIxMjMxNw.G3HIhF.t1jnqQvUP97-VhHiTNMWQ1mIemfGJ0S6bu71WQ")