from discord.ext import commands, tasks
from here_fishy_fishy.main import config, path_dir
import asyncprawcore
import asyncpraw
import asyncio
import discord
import json
import re

reddit = asyncpraw.Reddit(
    client_id=config.get('keys').get('reddit_client_id'),
    client_secret=config.get('keys').get('reddit_client_secret'),
    user_agent=config.get('keys').get('reddit_user_agent'),
)


class Fish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fish_subs_to_watch = self.bot.config.get('subsearch').get('reddit_subs_to_watch')
        self.ping_owner_status = self.bot.config.get('guild').get('ping_owner')
        self.cog_load()

    def save_config(self, config_data):
        with open(f'{path_dir}config.json', 'w') as f:
            json.dump(config_data, f, indent=4)
        self.sub_crawl.cancel()
        self.sub_crawl.start()

    def fish_channel(self, sub: str) -> str:
        return self.bot.config.get('subsearch').get('reddit_subs_to_watch').get(sub).get('discord_out_channel')

    def fish_regex(self, sub: str) -> str:
        return self.bot.config.get('subsearch').get('reddit_subs_to_watch').get(sub).get('regex')

    def cog_load(self):
        self.sub_crawl.start()

    def cog_unload(self):
        self.sub_crawl.cancel()

    async def check_if_sub_exists(self, sub):
        try:
            subreddit = await reddit.subreddit(sub, fetch=True)
            if subreddit:
                return True
        except asyncprawcore.Redirect:
            return False

    @tasks.loop(reconnect=True)
    async def sub_crawl(self):
        for sub in self.fish_subs_to_watch.copy().keys():
            try:
                exists = await self.check_if_sub_exists(sub)
                if exists:
                    subreddit = await reddit.subreddit(sub)
                    async for submission in subreddit.stream.submissions():
                        subreddit_title_regex = self.fish_regex(sub)
                        output_channel = self.fish_channel(sub)
                        get_matches = re.search(subreddit_title_regex, submission.title.lower())
                        if get_matches:
                            guild = self.bot.get_guild(self.bot.config.get("guild").get("guild_id"))
                            channel = discord.utils.get(guild.channels, id=output_channel)
                            check_old = [message.embeds[0].title for message in await channel.history(limit=100).flatten()
                                         if message.embeds]
                            if str(submission.title) not in check_old:
                                if not channel:
                                    channel = [channel_name for channel_name in guild.channels if 'fish' in channel_name][0]
                                description_text = submission.selftext if submission.selftext else submission.title
                                ping_owner = f'<@{guild.owner_id}>' if '[ga]' in submission.title.lower() and \
                                                                       self.ping_owner_status else '\n'
                                e = discord.Embed(title=submission.title,
                                                  description=f"[{description_text}](https://reddit.com/{submission.permalink})"
                                                              f"\n{ping_owner}",
                                                  colour=discord.Colour(0x278d89))
                                if submission.url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                                    e.set_image(url=submission.url)
                                await channel.send(embed=e)
                            else:
                                print(f"{submission.title} is already posted in {channel.name} @ {channel.id} in {guild.name}")

                else:
                    print(f'{sub} doesnt exist, its been removed')
                    self.bot.config['subsearch']['reddit_subs_to_watch'].pop(sub, None)
                    self.save_config(self.bot.config)
                    self.fish_subs_to_watch.pop(sub, None)
            except Exception as ex:
                print(ex)
                await asyncio.sleep(3600)

    @sub_crawl.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @commands.group()
    async def add(self, ctx, subreddit: str,):
        exists = await self.check_if_sub_exists(subreddit)
        if exists and subreddit not in self.fish_subs_to_watch:
            self.bot.config['subsearch']['reddit_subs_to_watch'][subreddit] = {
                                                                            "regex": "michigan|\\bmi\\b|\\[mi]",
                                                                            "discord_out_channel": 988789799324368937
                                                                              }
            self.save_config(self.bot.config)
            await ctx.send(f"{subreddit} has been added, you can now add regex and the out channel "
                           f"with <add> <sub> <regex> <regex string> or <add> <sub> <channel> <channel id/name>")


def setup(bot):
    bot.add_cog(Fish(bot))
