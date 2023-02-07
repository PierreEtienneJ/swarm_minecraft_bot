# swarm_minecraft_bot
/!\ In development

## Installation:

Go to https://github.com/PrismarineJS/mineflayer

## how to use

```python
from bot.state_machine_bot import FirstBot

for i in range(3):
    mybot = FirstBot(f"test_{i}", "mc_server_host","mc_port", "player_master")
    
    mybot.create()
    mybot.print("hello world")
    mybot.start()
```
