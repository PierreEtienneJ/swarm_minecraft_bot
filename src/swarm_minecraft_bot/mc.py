"""
list of MineCraft type
"""
import enum
import math
import time

class Vector3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
    
    @classmethod
    def from_Vec3(cls, vec3: "Vec3") -> "Vec3":
        """
        from Vec3, javascript type
        :param Vec3 vec3:
        """
        if vec3 == None:
            return None
        return Vector3(vec3.x, vec3.y, vec3.z)

    def distance(self, v: "Vector3") -> float:
        return math.sqrt((v.x-self.x)**2 + (v.y-self.y)**2 + (v.z-self.z)**2)

    def __str__(self):
        return f"x: {self.x : .3f}, y: {self.y : .3f}, z: {self.z : .3f}"

    def update_from_Vec3(self, vec3: "Vec3") -> "Vec3":
        self.x = vec3.x
        self.y = vec3.z
        self.y = vec3.z
    
    def update(self, x: float = None, y: float = None, z: float = None):
        if not x is None:
            self.x = x
        if not y is None:
            self.y = y
        if not z is None:
            self.z = z

class TypeEntity(enum.Enum):
    PLAYER = "PLAYER"
    BOT = "BOT"
    MOB = "MOB"
    HOSTILE = "HOSTILE"
    ANIMAL = "ANIMAL"
    OTHER = "OTHER"  # ITEM
    PASSIVE = "PASSIVE" # villager

class Entity:
    """
    :ivar str name:
    :ivar Vector3 position:
    :ivar TypeEntity type:
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

    def update_from_js_entity(self, entity:"javascript.proxy.Proxy"):
        """

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
    def from_js_entity(self, entity:"javascript.proxy.Proxy") -> "Entity":
        """
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
            print(f"ERROR WITH entity_type {entity_type} \n{entity}")

        myentity = Entity(name, entity_type, entity_id = entity.id)
        myentity.update_from_js_entity(entity)
        return myentity
        
        
class Mob(Entity):
    def __init__(self, mob_type: str, _id:str = None):
        name = mob_type + (_id or "")
        super().__init__(name, TypeEntity.MOB)
        self.mob_type = mob_type