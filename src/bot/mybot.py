import random
import time
from typing import Union, List, Callable, Tuple, Any
import math
import threading

import javascript

mineflayer = javascript.require("mineflayer")
pathfinder = javascript.require('mineflayer-pathfinder')
Vec3 = javascript.require('vec3').Vec3

class MyBot:
    def __init__(self, name: str, host: str, port: Union[str, int]):
        self.name = name
        self.host = host
        self.port = port
        self.bot = None
        self._mc_data = None
        self.event_list = []
        """List[Tuple[str, Callable[[Tuple[Any]], None]]]"""
        self._movement = None
        
    def create(self):
        self.bot = mineflayer.createBot({
            "host":self.host,
            "port":self.port, 
            "username":self.name,
            "hideErrors":False
        })
        javascript.once(self.bot, "login")
        
        self.bot.loadPlugin(pathfinder.pathfinder)
        self._mc_data = javascript.require("minecraft-data")(self.bot.version)
        self._movement = pathfinder.Movements(self.bot, self._mc_data)
        
        
        self.load_event()
        
    def print(self, *args):
        msg = " ".join(args)
        self.bot.chat(msg)
        print(self.name, *args)
        
    def load_event(self):
        for event, event_function in self.event_list:
            @javascript.On(self.bot, event)
            def function(*args):
                return event_function(*args)
    
    def go_to(self, x: float, y: float, z: float):
        RANGE_GOAL = 1
        self.bot.pathfinder.setMovements(self._movement)
        goal = pathfinder.goals.GoalNear(x, y, z, RANGE_GOAL)
        self.bot.pathfinder.setGoal(goal)
        
    def got_to_pos(self, position: Vec3):
        return self.go_to(position.x, position.y, position.z)
    
    @property
    def position(self):
        return self.bot.entity.position
    
    @property
    def x(self):
        return self.position.x 
    
    @property
    def y(self):
        return self.position.y
    
    @property
    def z(self):
        return self.position.z
    
    def get_nearest_entity(self, type_entity: List[str]):
        """
        return the nearest entity in the list type_entity
        :param List[str] type_entity: list of entity type like ["hostile", "animal", "mob"]
        """
        nearest_entity = None
        nearest_distance = 1000
        for entity_id in self.bot.entities:
            entity = self.bot.entities[entity_id]
            if entity:
                if entity.type:
                    if entity.type.lower() in type_entity:
                        d = self.distance_pos(entity.position)
                        if nearest_distance > d:
                            nearest_distance = d
                            nearest_entity = entity
        return nearest_entity
                
    def distance(self, x: float, y: float, z: float) -> float:
        """calcul distance between self and (x, y, z)"""
        return math.sqrt((x-self.x)**2 + (z-self.z)**2 + (z-self.z)**2)
    
    def distance_pos(self, position: Vec3) -> float:
        """calcul distance between self and position
        :param Vec3 position: 
        """
        return self.distance(position.x, position.y, position.z)
            
    
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
        

if __name__ == "__main__":
    for i in range(3):
        mybot = FirstBot(f"bot_{i}", "host", "port", "user_id")
        
        mybot.create()
        mybot.print("hello world")
        mybot.start()
        
    