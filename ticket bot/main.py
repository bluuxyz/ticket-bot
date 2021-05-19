import discord
from discord.ext import commands
import json






token = json.load(open("data/settings.json"))["token"]
prefix = json.load(open("data/settings.json"))["prefix"]
admin = json.load(open("data/settings.json"))["admin"]
ticketmessage = json.load(open("data/settings.json"))["ticket_message"]
embedcolor = 0x00000
adminerror = json.load(open("data/settings.json"))["admin_error_message"]


bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"Online use {prefix}help for my command list")


@bot.command()
async def help(ctx):
        help = discord.Embed(color=embedcolor)
        #basic help menu lol
        help.add_field(name="Ticket", value=f"`{prefix}ticket`", inline=True)
        help.add_field(name="Close Ticket", value=f"`{prefix}close`", inline=True)
        #footer can be changed 
        help.set_footer(text="github.com/bluuxyz")

        await ctx.send(embed=help)




@bot.command()
async def ticket(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        channels = [str(x) for x in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in str(channels):
            embed = discord.Embed(color=embedcolor, description='Ticket open!')
            await ctx.send(embed=embed)
        else:
            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.id}')
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True)
            embed = discord.Embed(color=embedcolor, description=ticketmessage)
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()

@bot.command()
async def close(ctx):
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.name == f'ticket-{ctx.author.id}':
            await ctx.channel.delete()
        elif ctx.author.id in admin and 'ticket' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            embed = discord.Embed(color=embedcolor, description=adminerror)
            await ctx.send(embed=embed)

 


bot.run(token)