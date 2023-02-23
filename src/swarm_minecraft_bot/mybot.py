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
    """
    master class bot:

    :ivar str name:
    :ivar str host:
    :ivar str/int port:
    :ivar List[Tuple[str, Callable[[Tuple[Any]], None]] event_list: list of event [(event, callbacks)]
    :ivar bot:
    """
    def __init__(self, name: str, host: str, port: Union[str, int]):
        self.name = name
        self.host = host
        self.port = port
        self.bot = None
        self._mc_data = None
        self.event_list = []
        self._movement = None
        
    def create(self):
        """
        connect the bot to the MC server
        """
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
        
        self.__load_event()
        
    def print(self, *args):
        """
        print args on mc chat and on console
        """
        msg = " ".join(args)
        self.bot.chat(msg)
        print(self.name, *args)
        
    def __load_event(self):
        """
        load event in self.event_list
        call by MyBot.create
        """
        for event, event_function in self.event_list:
            @javascript.On(self.bot, event)
            def function(*args):
                return event_function(*args)
    
    def go_to(self, x: float, y: float, z: float):
        """
        go to x, y, z with RANGE_GOAL to 1
        :param float x:
        :param float y:
        :param float z:
        """
        RANGE_GOAL = 1
        self.bot.pathfinder.setMovements(self._movement)
        goal = pathfinder.goals.GoalNear(x, y, z, RANGE_GOAL)
        self.bot.pathfinder.setGoal(goal)
        
    def got_to_pos(self, position: Vec3):
        """
        go to position
        :param Vec3 position:
        """
        return self.go_to(position.x, position.y, position.z)
    
    @property
    def position(self):
        """
        bot position
        """
        return self.bot.entity.position
    
    @property
    def x(self):
        """
        bot x position
        """
        return self.position.x 
    
    @property
    def y(self):
        """
        bot y position
        """
        return self.position.y
    
    @property
    def z(self):
        """
        bot z position
        """
        return self.position.z
    
    def get_nearest_entity(self, type_entity: List[str]):
        """
        return the nearest entity in the list type_entity
        :param List[str] type_entity: list of entity type like ["hostile", "animal", "mob"]
        :return: nearest_entity
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
        """calcul distance between self and (x, y, z)
        :param float x:
        :param float y:
        :param float z:
        """
        return math.sqrt((x-self.x)**2 + (z-self.z)**2 + (z-self.z)**2)
    
    def distance_pos(self, position: Vec3) -> float:
        """calcul distance between self and position
        :param Vec3 position: 
        """
        return self.distance(position.x, position.y, position.z)

    