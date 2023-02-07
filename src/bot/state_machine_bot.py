import random
import time
import threading
from typing import Union, List, Callable, Tuple, Any

try:
    from mybot import MyBot
except:
    from bot.mybot import MyBot

class FirstBot(MyBot, threading.Thread):
    """FirstBot
    herited from :py:class:`MyBot` and :py:class:`threading.Thread`.
    
    This bot use a state machine: :py:meth:`state_machine`.
    
    """
    def __init__(self, name: str, host: str, port: Union[str, int], player_name: str):
        """__init__ _summary_

        :param str name: bot name
        :param str host: server host
        :param str/int port: server port
        :param str player_name: bot master name
        """
        threading.Thread.__init__(self)
        MyBot.__init__(self, name=name, host=host, port=port)
        
        self.master = player_name
        self.event_list.append(("chat", self.on_msg))
        
        self.__current_state = None
        self.current_goal = None
        self.current_objectif = None
    
    def state_machine(self):
        """
        1. find target
        2. go to target position
        3. kill target entity
        => find target
        """
        if self.current_state is None:
            self.current_state = "find_target"
        
        if self.current_state == "find_target":
            self.current_objectif = self.get_entity(["hostile", "animal", "mob"])
            
            if self.current_objectif:
                self.current_goal = self.current_objectif.position
                self.current_state = "go"
            else:
                self.current_state = "find_target"
        
        if self.current_state == "go":
            if self.distance_pos(self.current_goal) < 2:
                self.current_state = "kill"
            else:
                self.got_to_pos(self.current_goal)
        
        if self.current_state == "kill":
            if not self.current_objectif.isValid:
                self.current_state = "find_target"
            else:
                if self.distance_pos(self.current_goal) < 2:
                    self.bot.attack(self.current_objectif)
                    time.sleep(random.random()*2)
                else:
                    self.current_state = "go"
    
    def run(self):
        while True:
            self.state_machine()
            time.sleep(0.3)
    
    def print(self, *args):
        super().print(self.master, *args)
    
    def on_msg(self, this, sender, message, *args):
        """event message javascript
        this event handler is set by :py:meth:`MyBot.load_event`
        """
        if sender == self.name:
            return 
        if sender == self.master:
            if message == "come":
                entity = self.bot.players[sender].entity
                if not entity:
                    self.print("where are you ?")
                    return
                self.print("I come")
                return self.got_to_pos(entity.position)
            
            if message == 'stop' or message == 'quit':
                self.bot.quit()
                exit(0)

            self.print("you say", message)

    @property
    def current_state(self):
        return self.__current_state
    
    @current_state.setter
    def current_state(self, value):
        if value != self.current_state:
            msg = f"change state to {value}"
            if value == "go":
                msg += f" on {self.current_goal.toString()} at {self.distance_pos(self.current_goal) : 0.1f} blocks"
            if value == "kill":
                msg += f" {self.current_objectif.name}"
            self.print(msg)
        self.__current_state = value
        
