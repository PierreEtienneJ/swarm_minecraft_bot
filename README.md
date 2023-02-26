# swarm_minecraft_bot
/!\ In development

## Installation:

Go to https://github.com/PrismarineJS/mineflayer

- nodejs >= 14
```sudo apt install nodejs```
- install mineflayer
```npm install mineflayer```


## how to use

```python
from swarm_minecraft_bot.state_machine_bot import StateBot

for i in range(3):
    mybot = StateBot(f"test_{i}", "mc_server_host","mc_port", "player_master")
    
    mybot.create()
    mybot.print("hello world")
    mybot.start()
```
