import subprocess, threading, discord, httpx, json, time

def run_worker(amount, type, channel):
    subprocess.run(['features', f"{amount}", f"{type}", f"{channel}"])

with open("config.json") as jsoned_file:
     jsoned_file = json.loads(jsoned_file.read())

def fetch_id(channel_name):
        data = {"operationName": "GetUserID","variables": {"login": channel_name,"lookupType": "ACTIVE"},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "bf6c594605caa0c63522f690156aa04bd434870bf963deb76668c381d16fcaa5"}}}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, json=data)
        try:
            target_id = response.json()["data"]["user"]["id"]
            return target_id
        except:
             return "Invalid_user"

class X():
    def __init__(x) -> None:
        x.bot = discord.Client(command_prefix="/", intents=discord.Intents.all())
        x.tree = discord.app_commands.CommandTree(x.bot)
        x.z = jsoned_file
        x.channel_id = x.z["bot"]["channel_id"]
        x.cooldown = []
    
    def cooldowned(x, id):
         time.sleep(120)
         x.cooldown.remove(id)
        
        
    def check_(x, interaction: discord.Interaction):
        x.z = 35
        if discord.utils.get(interaction.guild.roles, name="Shrum") in interaction.user.roles:
             x.z += 10000
        if discord.utils.get(interaction.guild.roles, name="Premium") in interaction.user.roles:
             x.z += 1000
        if discord.utils.get(interaction.guild.roles, name="Diamond") in interaction.user.roles:
             x.z += 750
        if discord.utils.get(interaction.guild.roles, name="Gold") in interaction.user.roles:
             x.z += 500
        if discord.utils.get(interaction.guild.roles, name="Silver") in interaction.user.roles:
             x.z += 250


    def botter(x):
        @x.bot.event
        async def on_ready():
            await x.tree.sync()
            print(" (+) Bot ready")
        
        @x.tree.command(name="tfollow", description="Sends [TWITCH] Followers to [CHANNEL]")
        async def tfollow(interaction: discord.Interaction, channel_name: str):
            if interaction.channel_id == x.channel_id:
                if interaction.user.id in x.cooldown:
                     embed = discord.Embed(title="(-) Negative", description="You are on cooldown!", color=discord.Color.red())
                     await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="Checking Id..", description="The bot is performing ID check, Please wait..\nThis will take 2-5 seconds max!", color=discord.Color.green())
                    await interaction.response.send_message(embed=embed)

                    x.check_(interaction)
                    target_id = fetch_id(channel_name)

                    if target_id != "Invalid_user":
                        embed = discord.Embed(title="(+) Positive", description=f"Sending `{x.z}` followers to `{channel_name}`!", color=discord.Color.green())
                        await interaction.edit_original_response(embed=embed)
                        x.cooldown.append(interaction.user.id)
                        threading.Thread(target=x.cooldowned, args=(interaction.user.id,)).start()
                        threading.Thread(target=run_worker, args=(x.z, "follow", channel_name,)).start()
                    else:
                        embed = discord.Embed(title="(-) Negative", description="The channel you entered is invalid!\nDouble check your spellings and try again!", color=discord.Color.red())
                        await interaction.edit_original_response(embed=embed)
            else:
                 embed = discord.Embed(title="(-) Negative", description="Use commands in proper channel!", color=discord.Color.red())
                 await interaction.response.send_message(embed=embed)

        @x.tree.command(name="tunfollow", description="Removes [TWITCH] Followers from [CHANNEL]")
        async def tunfollow(interaction: discord.Interaction, channel_name: str):
            if interaction.channel_id == x.channel_id:
                if interaction.user.id in x.cooldown:
                     embed = discord.Embed(title="(-) Negative", description="You are on cooldown!", color=discord.Color.red())
                     await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="Checking Id..", description="The bot is performing ID check, Please wait..\nThis will take 2-5 seconds max!", color=discord.Color.green())
                    await interaction.response.send_message(embed=embed)

                    x.check_(interaction)
                    target_id = fetch_id(channel_name)

                    if target_id != "Invalid_user":
                        embed = discord.Embed(title="(+) Positive", description=f"Removing `{x.z}` followers from `{channel_name}`!", color=discord.Color.green())
                        await interaction.edit_original_response(embed=embed)
                        x.cooldown.append(interaction.user.id)
                        threading.Thread(target=x.cooldowned, args=(interaction.user.id,)).start()
                        threading.Thread(target=run_worker, args=(x.z, "unfollow", channel_name,)).start()
                    else:
                        embed = discord.Embed(title="(-) Negative", description="The channel you entered is invalid!\nDouble check your spellings and try again!", color=discord.Color.red())
                        await interaction.edit_original_response(embed=embed)
            else:
                 embed = discord.Embed(title="(-) Negative", description="Use commands in proper channel!", color=discord.Color.red())
                 await interaction.response.send_message(embed=embed)
        
        x.bot.run(x.z["bot"]["token"])


X().botter()
