from interface import pictures
import mobs.mob as mob
from position import Position
import game


class RobusteMob(mob.Mob):
    def __init__(self, game_, position: Position, health):
        attributes = {
    
            # les dégats maximums que le mob pourra infliger
            "damage": 2,
            
            # la vie maximum
            "health_mul": 4,
            
            # la vitesse, en tuiles/ticks
            "speed": 0.0125,
            
            # les resistances du mob, pour chaque type d'attaque
            "resistances": {
                game.DAMAGE_TYPE_FIRE: 5/3,
                game.DAMAGE_TYPE_ICE: 1,
                game.DAMAGE_TYPE_RAW: 1,
                game.DAMAGE_TYPE_MAGIC: 0.5,
                
                # le type DAMAGE_TYPE_ABSOLUTE est renseigné par défaut dans mob.py
            },
        }
        super().__init__(game_, position, attributes, health, "robuste_break")
    
    def tick(self, current_tick, game_):
        super().tick(current_tick, game_)
        # a chaque tick
        
        # le mob avance
        self.advance()
    
    def get_render(self, relative_time):
        return pictures.get("robuste").final_scaled(0.3)
