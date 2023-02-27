"""
list of MineCraft type
"""
import enum
import math
import time

class Vector3:
    """
    class to create a Vector in 3D

    Attributes
    ----------
    x : float
        The X coordinate.
    y : float
        The Y coordinate.
    z : float
        The z coordinate. 
    """
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_Vec3(cls, vec3: "Vec3") -> "Vector3":
        """
        create a Vector3 from Vec3, javascript type

        Parameters
        ----------
        vec3 : javascript.Vec3
            Vector3 javascript

        Returns
        -------
        Vector3 
            new Vector3
        """
        if vec3 is None:
            return None
        return Vector3(vec3.x, vec3.y, vec3.z)

    def distance(self, vector: "Vector3") -> float:
        """
        calcul carthesian distance (norm 2) between two Vector3
        
        Parameters
        ----------
        vector : Vector3

        Returns
        -------
        float 
            carthesian distance

        """
        return math.sqrt((vector.x-self.x)**2 + (vector.y-self.y)**2 + (vector.z-self.z)**2)

    def __str__(self):
        """
        Returns
        -------
        str 
            string of Vector3 (x: <x>, y: <y>, z: <z>)
        """
        return f"(x: {self.x : .3f}, y: {self.y : .3f}, z: {self.z : .3f})"

    def update_from_Vec3(self, vec3: "Vec3") -> None:
        """
        update Vector3.x,  Vector3.y,  Vector3.z from Vec3
        
        Parameters
        ----------
        vec3 : Vec3
            Vector3 to update

        Returns
        -------
        None
        """
        self.update(x=vec3.x, y=vec3.y, z=vec3.z)

    def update(self, x: float = None, y: float = None, z: float = None) -> None:
        """
        update Vector3.x,  Vector3.y,  Vector3.z from x, y, z
        
        Parameters
        ----------
        x : float
            The X coordinate.
        y : float
            The Y coordinate.
        z : float
            The Z coordinate. 

        Returns
        -------
        None
        """
        if not x is None:
            self.x = x
        if not y is None:
            self.y = y
        if not z is None:
            self.z = z


class TypeEntity(enum.Enum):
    """
    Enum for type Entity in MineCraft
    """
    PLAYER = "PLAYER"
    """Player type"""
    BOT = "BOT"
    """BOT type only for this bot"""
    MOB = "MOB"
    """MOB type only"""
    HOSTILE = "HOSTILE"
    """HOSTILE type only"""
    ANIMAL = "ANIMAL"
    """ANIMAL type"""
    OTHER = "OTHER"  # ITEM
    """OTHER type, like ITEM"""
    PASSIVE = "PASSIVE" # villager
    """PASSIVE type, like villager"""


class Entity:
    """
    Attributes
    ----------
    name : str
        the entity name
    position : Vector3
        the entity position
    type : TypeEntity
        The entity type
    velocity : Vector3
        entity velocity
    orientation : Vector3
        entity orientation
            - yaw
            - pitch
            - roll TBD
    size : Vector3
        entity size:
            - height
            - width
            - depth TBD
    on_ground : bool
        if the entity is on ground
    is_valid : bool
        if the entity is valid TBD
    is_in_lava : bool
        if the entity is in lava
    is_in_water : bool
        if the entity is in water
    _raw_entity : javascript.Entity
        entity in javascript format
    id : Union[int, str]
        entity_id
    last_update : float
        last time when the entity has been update
    """
    def __init__(self, name: str, entity_type: TypeEntity, entity_id: int = None):
        self.name = name
        self.type = entity_type
        self.position = Vector3()
        self.velocity = Vector3()
        self.orientation = Vector3()
        self.size = Vector3()
        self.on_ground = None
        self.is_valid = None
        self.is_in_lava = None
        self.is_in_water = None
        self._raw_entity = None
        self.id = entity_id
        self.last_update = None

    def update_from_js_entity(self, entity: "javascript.proxy.Proxy") -> None:
        """
        update entity from javascript entity
        update all Vector3: position, velocity, orientation, size and other bool

        Parameters
        ----------
        entity : javascript.proxy.Proxy
            entity from javascript

        Returns
        -------
        None
        """
        if entity is None:
            self.is_valid = False
            return None

        self.last_update = time.time()
        self._raw_entity = entity
        self.position.update_from_Vec3(entity.position)
        self.velocity.update_from_Vec3(entity.velocity)
        self.orientation.update(
            x=entity.yaw,
            y=entity.pitch,
            z=entity.roll or 0  # TODO confirm
            )
        self.on_ground = entity.onGround
        self.is_valid = entity.isValid
        self.size.update(
                x=entity.height,
                y=entity.width,
                z=entity.depth or 0,  # TODO confirm
            )
        self.is_in_lava = entity.isInLava
        self.is_in_water =entity.isInWater

        # TODO ADD equipment, heldItem,

    @classmethod
    def from_js_entity(self, entity: "javascript.proxy.Proxy") -> "Entity":
        """
        create Entity from javascript entity

        Parameters
        ----------
        entity : javascript.proxy.Proxy
            entity from javascript

        Returns
        -------
        Entity
            new entity
        """
        entity_type = entity.type
        name = entity.username or f"{entity.name}_{entity.id}"

        if entity_type.upper() == "PLAYER":
            entity_type = TypeEntity.PLAYER
        elif entity_type.upper() == "HOSTILE":
            entity_type = TypeEntity.HOSTILE
        elif entity_type.upper() == "ANIMAL":
            entity_type = TypeEntity.ANIMAL
        elif entity_type.upper() == "MOB":
            entity_type = TypeEntity.MOB
        else:
            print(f"ERROR WITH entity_type {entity_type} \n{entity}") # TODO raise

        myentity = Entity(name, entity_type, entity_id = entity.id)
        myentity.update_from_js_entity(entity)
        return myentity
        
        
class Mob(Entity):
    def __init__(self, mob_type: str, _id:str = None):
        name = mob_type + (_id or "")
        super().__init__(name, TypeEntity.MOB)
        self.mob_type = mob_type