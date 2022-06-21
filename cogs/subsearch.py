from discord.ext import commands, tasks
from here_fishy_fishy.main import config
import discord
import asyncpraw
import re

reddit = asyncpraw.Reddit(
    client_id=config.get('keys').get('reddit_client_id'),
    client_secret=config.get('keys').get('reddit_client_secret'),
    user_agent=config.get('keys').get('reddit_user_agent'),
)


class Fish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fish_subs_to_watch = config.get('subsearch').get('reddit_subs_to_watch').keys()
        self.ping_owner_status = config.get('guild').get('ping_owner')
        self.cog_load()

    def fish_channel(self, sub):
        return self.bot.config.get('subsearch').get('reddit_subs_to_watch').get(sub).get('discord_out_channel')

    def fish_regex(self, sub):
        return self.bot.config.get('subsearch').get('reddit_subs_to_watch').get(sub).get('regex')

    def cog_load(self):
        self.sub_crawl.start()

    def cog_unload(self):
        self.sub_crawl.cancel()

    @tasks.loop(reconnect=True)
    async def sub_crawl(self):
        for sub in self.fish_subs_to_watch:
            subreddit = await reddit.subreddit(sub)
            async for submission in subreddit.stream.submissions():
                subreddit_title_regex = self.fish_regex(sub)
                output_channel = self.fish_channel(sub)
                get_matches = re.search(subreddit_title_regex, submission.title.lower())
                if get_matches:
                    guild = self.bot.get_guild(self.bot.config.get("guild").get("guild_id"))
                    channel = discord.utils.get(guild.channels, id=output_channel)
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

    @sub_crawl.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def add(self, subreddit: str, ctx):
        if subreddit not in self.fish_subs_to_watch:
            self.fish_subs_to_watch.append(subreddit)


def setup(bot):
    bot.add_cog(Fish(bot))
