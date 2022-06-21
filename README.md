# here fishy fishy
This is the first iteration of my asynchronous project: here fishy fishy.<br>
Currently it crawls up to at least one subreddit(s) using regex you supply and notifies you of new postings.<br>
The rough idea of this bot is to stream /r/AquaSwap for posts in my state, and post them to a channel - while pinging me if its tagged `[GA]` or Giving Away.
<br><br>

# To Use
Navigate to the main directory and fill out the `config.json`. (It's partially filled out)<br>
Followed by `python3 -m main.py` to get it running.


# Requirements
It works on my computer.
```
python 3.10
discord.py 1.7.3
asyncpraw 7.5.0
```




#Current todo:<br>
```
add <sub> <string>
add <sub> <regex> <string>
add <sub> <channel> <string>
```

Followed with a `remove` command.<br>

Check different paths based on OS.

Check if files/folders exist.

Do some general house cleaning, error handling and testing.

At some point I'd like to add the addition of `aiosqlite`<br>
Although we will see minimal gain.<br>

After the above is complete I'd like to ensure it works on both linux and windows then mark it as v1.0.

Once it's reached a v1.0 status in my head I'll reach to create a github autoupdater.<br>
(When I push a changed to gitbub, the server will restart the script)<br>
