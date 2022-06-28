# here fishy fishy
This is the first iteration of my asynchronous project: here fishy fishy.<br>
Currently it crawls up to at least one subreddit(s) using regex you supply and notifies you of new postings.<br>
The rough idea of this bot is to stream /r/AquaSwap for posts in my state, and post them to a channel - while pinging me if its tagged `[GA]` or Giving Away.
<br><br>

# To Use
Navigate to the main directory and fill out the `config.json`. (It's partially filled out)<br>
Followed by `python3 -m main.py` to get it running.

# Example usage
![](https://github.com/SobieskiCodes/here-fishy-fishy/blob/main/docs/pictures/J5L7qno.png?raw=true)

# Requirements
It works on my computer.
```
python 3.10
discord.py 1.7.3
asyncpraw 7.5.0
```




# Current todo:<br>
```
- [x] add <sub> <string>
- [ ] add <sub> <regex> <string>
- [ ] add <sub> <channel> <string>
- [ ] remove <sub> <string>
- [ ] remove <sub> <regex> <string>
- [ ] remove <sub> <channel> <string>
- [ ] allow for ignored users
- [ ] check different paths based on OS.
- [ ] check if files/folders exist.
- [ ] error handling and testing.
- [ ] switch to aiosqlite
```

# After v1...
Once it's reached a v1.0 (all the above and probably then some) status in my head I'll reach to create a github autoupdater.<br>
(When I push a changed to gitbub, the server will restart the script)<br>
