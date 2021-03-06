import math

import pygame

import main
import tiles
from position import Vector2, Position
from interface import graphics, user_interface, pictures, building_popup
from mobs import mob


def render_image_game(interface, image, game_position, centered, relative_time):
    corner_draw = graphics.get_pixel_pos(game_position, interface)
    img_new_size = (math.ceil(graphics.PIXEL_PER_ZOOM * interface.half_zoom),) * 2
    n_scale = image.final_scale
    img_new_size = (img_new_size[0] * n_scale[0], img_new_size[1] * n_scale[1])
    
    if centered:
        corner_draw -= Vector2(img_new_size[0] / 2, img_new_size[1] / 2)

    corner_draw = corner_draw.to_tuple()
    
    graphics.draw_image(interface.screen, corner_draw, image, img_new_size)
    
    rect = pygame.rect.Rect(*(corner_draw + img_new_size))
    return rect


def render_game(interface, game_, time, last_frame, relative_time):
    elapsed_time = max(0.001, (time - last_frame))
    
    for tile in game_.level.tiles:
        render_image_game(interface, tile.get_render(relative_time), tile.position, False, relative_time)
        if isinstance(tile, tiles.CastleTile):
            bar_nb = max(0, tile.tower.health * 13 // tile.tower.max_health)
            bar_img = pictures.get("health" + str(int(bar_nb)))
            bar_img.final_scaled(0.8)
            bar_img.smoothscaling = False
            
            render_image_game(interface, bar_img, tile.position.middle() + Position(0, 0.6), True, relative_time)
        
    for entity in game_.entities:
        if entity.is_dead():
            continue
        
        pos = user_interface.lerp(entity.last_position, entity.position, relative_time)
        
        mob_img = entity.get_render(relative_time)
        
        if isinstance(entity, mob.Mob) and entity.health != entity.max_health:
            bar_nb = entity.health * 13 // entity.max_health
            bar_img = pictures.get("health" + str(int(bar_nb)))
            bar_img = bar_img.final_scaled(bar_img.get_width() / 128 * 1.5)
            bar_img.smoothscaling = False
            
            if (entity.ticks_lived + relative_time) * 0.05 < 1:
                bar_img.faded(((entity.ticks_lived + relative_time) * 0.05) ** 3)
            
            render_image_game(interface, bar_img, pos + Position(0, mob_img.final_scale[1] * 0.8), True, relative_time)

        if isinstance(entity, mob.Mob) and (entity.ticks_lived + relative_time) * 0.05 < 1:
            mob_img.faded(((entity.ticks_lived + relative_time) * 0.05) ** 3)
        
        render_image_game(interface, mob_img, pos, True, relative_time)
    
    text_img1 = graphics.WAVE_FONT.render("VAGUE " + str(game_.wave + 1), True, (170, 50, 50))
    interface.screen.blit(text_img1, ((main.SCREEN_WIDTH - text_img1.get_width()) / 2, 10))

    if game_.btwn_waves:
        next_wave_text = "Vague suivante \u2022 " + str(int((game_.next_wave_date - game_.game_tick) * main.TICK_REAL_TIME + 1))
        
        text_img2 = pictures.MyImage(graphics.NEXT_WAVE_FONT.render(next_wave_text, True, (150, 40, 40)))
        text_img2_hover = pictures.MyImage(graphics.NEXT_WAVE_FONT.render(next_wave_text, True, (200, 60, 60)))
        
        button_pos = ((main.SCREEN_WIDTH - text_img2.get_width()) / 2, 10 + text_img1.get_height())
        
        def next_wave_action():
            game_.next_wave_date = game_.game_tick - 1
        
        next_wave_button = user_interface.Button(interface, next_wave_action, button_pos, text_img2, text_img2_hover, "next_wave")
        interface.add_button(next_wave_button)

    money_text_img = graphics.PRICES_FONT.render(str(game_.money) + "  ", True, (200, 200, 150))
    interface.screen.blit(money_text_img, (main.SCREEN_WIDTH - money_text_img.get_width(), 10))
    
    if interface.popup_tile:
        interface.popup_rect = building_popup.render_popup(interface, game_, time, last_frame, relative_time)
