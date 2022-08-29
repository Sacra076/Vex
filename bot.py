import discord
from discord.ext import commands, tasks
from typing import Optional
import aiohttp


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
WELCOME_CHANNEL_ID = 1012846152028266617
LEAVE_CHANNEL_ID = 1012846152028266617
YOUTUBE_ANNOUNCEMENT_CHANNEL_ID = 1012822073506283670
TWITCH_ANNOUNCEMENT_CHANNEL_ID = 1012822073506283670
WELCOME_ROLE_ID = 1012819099920904272


@bot.command()
@commands.is_owner()
async def RankMenu(ctx):
    buttons = (
        (
            ("<:RankAscendant:1013132018390929468>", 1013130054391316490,),
            ("<:RankDiamond:1013131982848393276>", 1013130139179167806,),
            ("<:RankPlatinum:1013131962984177810>", 1013130184779644959,),
            ("<:RankGold:1013131931774361700>", 1013130255818559530,),
            ("<:RankSilver:1013131899788591256>", 1013130288664170667,),
        ),
        (
            ("<:RankBronze:1013131873339326565>", 1013130344716836895,),
            ("<:RankIron:1013131851226947786>", 1013130378153828453,),
        )
    )
    components = discord.ui.MessageComponents(*[
        discord.ui.ActionRow(*[
            discord.ui.Button(
                custom_id=f"ROLEMENU {role_id}",
                style=discord.ButtonStyle.secondary,
                emoji=emoji,
            )
            for emoji, role_id in row
        ])
        for row in buttons
    ])
    embed = discord.Embed(title="Valorant Ranks", colour=0x9b00ff)
    await ctx.send(
        embeds=[embed],
        components=components)


@bot.command()
@commands.is_owner()
async def PronounMenu(ctx):
    buttons = (
        (
            ("He/Him", 1013150596737536151,),
            ("She/Her", 1013150700806606979,),
            ("They/Them", 1013150749200502947,),
        ),
    )
    components = discord.ui.MessageComponents(*[
        discord.ui.ActionRow(*[
            discord.ui.Button(
                custom_id=f"ROLEMENU {role_id}",
                style=discord.ButtonStyle.secondary,
                label=label
            )
            for label, role_id in row
        ])
        for row in buttons
    ])
    embed = discord.Embed(title="Pronouns", colour=0x9b00ff)
    await ctx.send(
        embeds=[embed],
        components=components)


@bot.command()
@commands.is_owner()
async def RegionMenu(ctx):
    buttons = (
        (
            ("EU", 1013155362439966740,),
            ("NA", 1013155413660799127,),
            ("LATAM", 1013155460947386398,),
        ),
        (
            ("APAC", 1013155510482128956,),
            ("KOREA", 1013155566467690597,),
            ("BRAZIL", 1013155619538210929,),
        )
    )
    components = discord.ui.MessageComponents(*[
        discord.ui.ActionRow(*[
            discord.ui.Button(
                custom_id=f"ROLEMENU {role_id}",
                style=discord.ButtonStyle.secondary,
                label=label
            )
            for label, role_id in row
        ])
        for row in buttons
    ])
    embed = discord.Embed(title="Regions", colour=0x9b00ff)
    await ctx.send(
        embeds=[embed],
        components=components)


@bot.command()
@commands.is_owner()
async def pingmenu(ctx):
    buttons = (
        (
            ("Video Pings", 1013173789753872404,),
            ("Stream Pings", 1013173931508776991,),
            ("Announcement Pings", 1013173922184835132,),
            ("Event Pings", 1013173955915432129,),
        ),
    )
    components = discord.ui.MessageComponents(*[
        discord.ui.ActionRow(*[
            discord.ui.Button(
                custom_id=f"ROLEMENU {role_id}",
                style=discord.ButtonStyle.secondary,
                label=label
            )
            for label, role_id in row
        ])
        for row in buttons
    ])
    embed = discord.Embed(title="Notifications", colour=0x9b00ff)
    await ctx.send(
        embeds=[embed],
        components=components)


#youtube link
@bot.command()
async def youtube(ctx):
    await ctx.send("https://www.youtube.com/channel/UC3HndKaXUGM4Fygo1T5kwuA")

#twitch link
@bot.command()
async def twitch(ctx):
    await ctx.send("https://www.twitch.tv/sacra076")


#join messages
@bot.event
async def on_member_join(member):
    #add role
    role = discord.Object(WELCOME_ROLE_ID)
    await member.add_roles(
        role,
        reason="Member joined",
    )

    #welcome message
    channel = bot.get_partial_messageable(WELCOME_CHANNEL_ID)
    await channel.send(f"Welcome to the server, {member.mention}! You are member #{len(member.guild.members)}.",allowed_mentions=discord.AllowedMentions.none())


@bot.event
async def on_member_remove(member):
    channel = bot.get_partial_messageable(LEAVE_CHANNEL_ID)
    await channel.send(f"{member} has left the server.")


@bot.event
async def on_component_interaction(interaction):
    if not interaction.custom_id.startswith("ROLEMENU"):
        return

    await interaction.response.defer(ephemeral=True)
    
    role_id_str = interaction.custom_id[9:]
    role_id = int(role_id_str)
    
    all_buttons = []
    for action_row in interaction.message.components.components:
        all_buttons.extend(action_row.components)

    roles_to_remove = [
        discord.Object(int(button.custom_id[9:]))
        for button in all_buttons
    ]

    role_to_add = discord.Object(role_id)
    await interaction.user.add_roles(
        role_to_add,
        reason="Role picker"
    )
    roles_to_remove.remove(role_to_add)
    await interaction.user.remove_roles(
        *roles_to_remove,
        reason="Role Picker",
    )

    await interaction.followup.send("Given Role",
    ephemeral=True)


@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="__Server Rules__", colour=0x9b00ff,
    description="""**1.** Don't break Discord's terms of service (https://discord.com/terms) and follow their guidelines (https://discord.com/guidelines).

**2.** Don't break Riot's terms of service (https://www.riotgames.com/en/terms-of-service)

**3.** No sensitive topics. Talking about subjects like politics or religion is not allowed

**4.** No advertising of any kind outside of <#1012823922087051405>

**5.** No spamming or repetitive sending of identical or similar messages (this includes pings or emojis)

**6.** English only, our staff team can almost only moderate issues in english so only english may be spoken within the server

**7.** No harassment of any kind. This includes: begging, impersonation, racism, bullying or any form of antisocial behaviour

**8.** No sharing of NSFW media, this includes videos images or gifs of nudity or gore

**9** Do not share any kind of sensitive info. This includes keeping yourself safe along with making sure not to doxx anyone else

**10.** Accessing and using this server means that you've read and understand the rules. You cannot feign ignorance to avoid punishment.*""")
    await ctx.send(
        embeds=[embed])



@bot.command()
async def serverroles(ctx):
    embed = discord.Embed(title="__Role Descriptions__", colour=0x9b00ff,
    description="""<@&1012759255666933781> - Sacra
<@&1012765888753188875> - Server Manager
<@&1012795625328365628> - Server Admin
<@&1012795658996031518> - Server Moderator
<@&1012826319869980682> - Twitch Moderator
<@&1012820628853756026> - Event Hosts and Managers
<@&1012819126915444796> - Twitch Subscriber:
Tier 3 - Archmage
Tier 2 - Magii
Tier 1 - Scribe
<@&1012853856465588294> - Nitro Booster
__Cerberus Activity Roles__
<@&1012796005370048532> - 800xp
<@&1012795966589505537> - 550xp
<@&1012795931315404882> - 350xp
<@&1012795900067840120> - 200xp
<@&1012795861983567903> - 100xp
<@&1012819099920904272> - Server Member
<@&1012796068829855804> - Discord Bot""")
    await ctx.send(
        embeds=[embed])


async def get_sacra_game_name() -> Optional[str]:
    url = "https://api.twitch.tv/helix/streams"
    params = {"user_login": "briandavidgilbert"}
    headers= {'Authorization': 'Bearer rp1wpyz7gu74rslenqkknd2whfyfxq', 'Client-Id': '46hatcnjlaem81nn1cqhgv2em7dq8w'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as site:
            data = await site.json()
    if data['data']:
        return data['data'][0]['game_name']
    return None


pinged_stream_announcements: bool = False

@tasks.loop(seconds=60)
async def check_live_loop():
    game_name = await get_sacra_game_name()
    if game_name:
        if pinged_stream_announcements is False:
            channel = bot.get_partial_messageable(TWITCH_ANNOUNCEMENT_CHANNEL_ID)
            await channel.send(f"Sacra is now streaming {game_name}, https://www.twitch.tv/sacra076 ")
            pinged_stream_announcements = True
    
    else: pinged_stream_announcements = False

check_live_loop.start()
























bot.run("MTAxMzEzMzc4MzI4Mjc2NTgyNQ.GunQi2.EnS5mc4RzLxWyTTpECLqRwJJySsguvsZMrZLd4")