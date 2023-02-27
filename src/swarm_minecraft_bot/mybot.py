import random
import time
from typing import Union, List, Callable, Tuple, Any, Dict
import math
import threading

import javascript

from swarm_minecraft_bot import mc

mineflayer = javascript.require("mineflayer")
pathfinder = javascript.require('mineflayer-pathfinder')
Vec3 = javascript.require('vec3').Vec3

class MyBot(mc.Entity):
    """
    
    master class bot herited from mc.Entity:
    
    Attributes
    ----------
    host : str
        server address
    port : Union[int, str]
        server port
    event_list : List[Tuple[str, Callable[[Tuple[Any]], None]]
        list of event [(event, callbacks)]
        set with MyBot.__load_event:
        @javascript.On(self.bot, <event>)
        def function(*args):
            return <callbacks>(*args)
    bot : TBD
        javascript bot
    _mc_data : TBD
        minecraft data TBD type
        from javascript.require("minecraft-data")
    _movement : TBD
        minecraft from javascript.require('mineflayer-pathfinder')
    """
    def __init__(self, name: str, host: str, port: Union[str, int]):
        super().__init__(name = name, entity_type = mc.TypeEntity.BOT)
        self.host = host
        self.port = port
        self.bot = None
        self._mc_data = None
        self.event_list = []
        self._movement = None

    def create(self):
        """
        - connect the bot to the MC server
        - load plugins
        - create pathfinder.Movements
        - run self.__load_event
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
        print args on minecraft chat and console

        TODO: replace print by logger
        """
        msg = " ".join(args)
        print(self.name, *args)
        self.bot.chat(msg)

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
        using pathfinder

        :param float x:
        :param float y:
        :param float z:
        """
        RANGE_GOAL = 1
        self.bot.pathfinder.setMovements(self._movement)
        goal = pathfinder.goals.GoalNear(x, y, z, RANGE_GOAL)
        self.bot.pathfinder.setGoal(goal)

    def got_to_pos(self, position: mc.Vector3):
        """
        go to position
        :param mc.Vector3 position:
        """
        return self.go_to(position.x, position.y, position.z)

    @property
    def _position(self) -> mc.Vector3:
        """
        FIXME self.update_from_js_entity and return self.position

        Returns
        -------
        mc.Vector3
            bot position
        """
        self.update_from_js_entity(self.bot.entity)
        return self.position

    @property
    def x(self) -> float:
        """
        Returns
        -------
        float
            bot x position
        """
        return self._position.x 

    @property
    def y(self) -> float:
        """
        Returns
        -------
        float
            bot y position
        """
        return self._position.y

    @property
    def z(self) -> float:
        """
        Returns
        -------
        float
            bot z position
        """
        return self._position.z

    @property
    def nearest_entity(self) -> List[mc.Entity]:
        """
        Returns
        -------
        List[mc.Entity]
            list for entity near the bot
        """
        rlist = []
        for entity_id in self.bot.entities:
            entity = self.bot.entities[entity_id]
            if not entity is None:
                entity_e = mc.Entity.from_js_entity(entity)
                if not entity_e is None:
                    rlist.append(entity)  # FIXME entity_e
                else:
                    raise TypeError(f"error with entity {entity}, {entity_e}")
        return rlist

    def get_nearest_entity(self, type_entity: List[mc.TypeEntity]) -> mc.Entity:
        """
        Parameters
        ----------
        type_entity : List[str]
            list of entity type like [TypeEntity.PLAYER, TypeEntity.ANIMAL, TypeEntity.MOB]
            ["hostile", "animal", "mob"]

        Returns
        -------
        List[mc.Entity]
            list for entity near the bot and in type_entity list 
        """
        nearest_entity = None
        nearest_distance = 1e9
        for entity in self.nearest_entity:
            if entity.type in type_entity:
                dist = self.distance_pos(entity.position)
                if dist < nearest_distance:
                    nearest_distance = dist
                    nearest_entity = entity
        return nearest_entity

    def distance(self, x: float, y: float, z: float) -> float:
        """
        calcul self.position.distance with (x, y, z)
        
        Parameters
        ----------
        x : float
            The X coordinate.
        y : float
            The Y coordinate.
        z : float
            The z coordinate. 
        """
        return self._position.distance(mc.Vector3(x, y, z))

    def distance_pos(self, position: mc.Vector3) -> float:
        """
        calcul self.position.distance with (x, y, z)
        FIXME and update from js_entity 
        Parameters
        ----------
        position : mc.Vector3 
            position to calcul distance
        """
        self.update_from_js_entity(self.bot.entity)
        return self._position.distance(position)

    def __dict__(self) -> Dict[str, Any]:
        """
        this function return the log of the bot
        Returns
        -------
        Dict[str, Any]
            - position: (x, y, z)
            - entity: [{type, position}]
        """
        return dict(super())

    