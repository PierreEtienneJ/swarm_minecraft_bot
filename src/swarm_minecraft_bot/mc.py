"""
list of MineCraft type
"""
import enum
import math

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
        return Vector3(vec3.x, vec3.y, vec3.z)

    def distance(self, v: "Vector3") -> float:
        return math.sqrt((v.x-self.x)**2 + (v.y-self.y)**2 + (v.z-self.z)**2)


class TypeEntity(enum.Enum):
    PLAYER = "PLAYER"
    BOT = "BOT"


class Entity:
    """
    :ivar str name:
    :ivar Vector3 position:
    :ivar TypeEntity type:
    """
    def __init__(self, name: str, entity_type: TypeEntity):
        self.name = name
        self.type = entity_type
        #self.position = Vector3()