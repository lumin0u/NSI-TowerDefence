from interface import pictures, graphics
import mobs.mob as mob
from position import Position
import main
import game

pictures.load_picture("robuste", "mobs/")


class RobusteMob(mob.Mob):
    def __init__(self, game_, position: Position, health_multiplier):
        attributes = {
            
            # la vie maximum
            "health": 10,
            
            # la vitesse, en tuiles/ticks
            # TICK_REAL_TIME devrait toujours etre 0.1 (secondes) mais il faut toujours utiliser la variable
            # mettre TICK_REAL_TIME comme speed revient a dire que le mob avancera d'une tuile par seconde
            # ici TICK_REAL_TIME / 2 veut dire qu'il mettra 2 secondes a traverser une tuile
            "speed": main.TICK_REAL_TIME / 4,
            
            # les resistances du mob, pour chaque type d'attaque
            "resistances": {
                # une résistance de 2 indique que le mob prendra 2x moins de dégats de feu
                game.DAMAGE_TYPE_FIRE: 0.5,
                
                # une résistance de 0.5 indique que le mob prendra 2x plus de dégats de glace
                game.DAMAGE_TYPE_ICE: 0.5,
                
                # résistance de 1: pas d'altération
                game.DAMAGE_TYPE_RAW: 0.5,
                game.DAMAGE_TYPE_MAGIC: 1.5,
                
                # le type DAMAGE_TYPE_ABSOLUTE est renseigné par défaut dans mob.py
            },
        }
        super().__init__(game_, position, attributes, health_multiplier)
    
    def tick(self, current_tick):
        # a chaque tick
        
        # le mob avance
        self.advance()
    
    def get_render(self, time):
        return graphics.scaled(pictures.PICTURES["robuste"].get_img(time), 0.3)
