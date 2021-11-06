import random
from copy import deepcopy

import main
import mobs.mob as mob
import position
import pricing
import tiles
from mobs import boss_mob

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4

GAME_INSTANCE = None


class Game:
    def __init__(self, level_, current_tick):
        global GAME_INSTANCE
        GAME_INSTANCE = self
        
        self._entities = []
        self._level = deepcopy(level_)
        self.money = level_.money
        self._id_inc = 0
        self._wave = 0
        self._btwn_waves = True
        self._next_wave_date = self.current_wave().preparation
    
    @property
    def level(self):
        return self._level
    
    @property
    def wave(self):
        return self._wave
    
    @property
    def btwn_waves(self):
        return self._btwn_waves
    
    @property
    def next_wave_date(self):
        return self._next_wave_date
    
    @next_wave_date.setter
    def next_wave_date(self, value):
        self._next_wave_date = value
    
    def add_entity(self, entity):
        self._entities.append(entity)
    
    def remove_entity(self, entity):
        self._entities.remove(entity)
    
    def current_wave(self):
        return self.level.waves[self._wave % len(self.level.waves)]
    
    def tick(self, current_tick):
        if self._btwn_waves:
            if self._next_wave_date <= current_tick:
                self._btwn_waves = False
                self.current_wave().start(current_tick)
        
        elif self.current_wave().is_ended(current_tick - 1):
            self._btwn_waves = True
            self._wave += 1
            self._next_wave_date = current_tick + self.current_wave().preparation
            
        if not self._btwn_waves:
            count_mult = self._wave // len(self.level.waves)
            for mob_type in self.current_wave().next_mobs(current_tick) * (1 + count_mult):
                health = 5 + self._wave * self._wave
                if mob_type is boss_mob.BossMob:
                    health = self.current_wave().boss_health
                shift = position.Position((random.random() - 0.5) * random.random() * 0.7, (random.random() - 0.5) * random.random() * 0.7)
                self.add_entity(mob_type(self, self.level.spawner.position.middle() + shift, health))
        
        for entity in self._entities:
            if entity.is_dead():
                self.remove_entity(entity)
            else:
                entity.tick(current_tick, self)
        for tower in (tile.tower for tile in self.level.tiles if isinstance(tile, tiles.BuildingTile) and not tile.is_empty()):
            tower.tick(current_tick, self)
        
    @property
    def entities(self):
        return self._entities.copy()
    
    @property
    def mobs(self):
        return [amob for amob in self._entities if isinstance(amob, mob.Mob)]
        
    def next_id(self):
        self._id_inc += 1
        return self._id_inc
