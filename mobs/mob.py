import math
from abc import ABC, abstractmethod

import pygame

from entity import Entity
from position import Position, TilePosition, Direction
from copy import copy
from interface import pictures
import random
import game
import tiles


class Mob(Entity, ABC):
    def __init__(self, game_, position: Position, attributes: dict, health):
        super().__init__(game_, position)

        # on copie le dictionnaire pour pouvoir le modifier au besoin
        attributes = attributes.copy()
        
        self._game = game_
        
        self._attributes = attributes
        self._attributes["resistances"][game.DAMAGE_TYPE_ABSOLUTE] = 1
        self._max_health = health * self._attributes["health_mul"]
        self._health = self.max_health
    
    @property
    def max_health(self) -> float:
        return self._max_health
    
    @property
    def health(self) -> float:
        return self._health
    
    @property
    def speed(self) -> float:
        """
            la vitesse est exprimé en tuiles/ticks
        """
        return float(self._attributes["speed"])
        
    def advance(self):
        # avancer en fonction de la direction de la tuile
        tile = self._game.level.tile_at(self._position)
        
        if isinstance(tile, tiles.PathTile):
            if tile.from_ and tile.direction != -tile.from_:
                corner = tile.position.middle() + (tile.direction + tile.from_) / 2
                corner_angle = ((tile.direction + tile.from_).angle() + 3 * math.pi / 4) % (2 * math.pi) - math.pi
                rel_pos = self.position - corner
                
                clockwise = tile.direction.angle(tile.from_) <= 0
                
                new_angle = rel_pos.angle() + (self.speed / rel_pos.length()) * (-1 if clockwise else 1)
                
                new_pos = corner + Direction(math.cos(new_angle), math.sin(new_angle)) * rel_pos.length()
                
                self.teleport(new_pos)
            else:
                dir_ = tile.direction
                self.move(dir_ * self.speed)
            
        elif isinstance(tile, tiles.CastleTile):
            dmg = max(10., self.max_health / 10)
            tile.tower.damage(dmg / self.max_health * self._attributes["damage"], self)
            # la tour renvoie les dégats
            self.damage(dmg, game.DAMAGE_TYPE_ABSOLUTE)
    
    def move(self, direction: Direction):
        self.teleport(self.position + direction)
    
    def teleport(self, position: Position):
        self._position = position
    
    def damage(self, damage: float, type_):
        self._health -= damage / self._attributes["resistances"][type_]
    
    def is_dead(self):
        return self._health <= 0
