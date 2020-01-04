import pygame

from pygame.locals import (
K_z,
K_x,
KEYDOWN,
QUIT,
K_SPACE,
K_UP,
K_DOWN,
RLEACCEL
)

SHADOW_OFFSET = 3

class MenuItem:
    def __init__(self, text, menu_action = None):
        self.text = text
        #function that takes a key parameter, return running, session_key
        self.menu_action = menu_action



class BaseMenu:

    def __init__(self, font, font_color, shadow_font, shadow_font_color, menu_color, selection_color, midtop):
        self.items = []
        self.font = font
        self.font_color = font_color
        self.shadow_font = shadow_font
        self.shadow_font_color = shadow_font_color
        self.menu_color = menu_color
        self.selection_color = selection_color
        self.midtop = midtop
        self.current_index = None

        self.surf_rect_list = []
        self.menu_width = 0

        self.ready_to_draw = False


    def add(self, text, menu_action):
        self.items.append( MenuItem( text, menu_action ) )
        if len(self.items) > 0:
            self.current_index = 0
        self.ready_to_draw = False

    def process_input(self, key):

        if key == K_UP :
            self.current_index = (self.current_index - 1) % len(self.items)
        elif key == K_DOWN :
            self.current_index = (self.current_index + 1) % len(self.items)
        elif self.items[self.current_index].menu_action:
            self.items[self.current_index].menu_action(key)

    def init_draw_list(self):
        font_size = self.font.get_height()
        for i in range(len( self.items ) ):
            text = self.items[i].text
            text_surface = self.font.render(text, True, self.font_color)
            text_rect = text_surface.get_rect(center = self.midtop)
            text_rect.move_ip(0, font_size * (2*i + 1))

            shadow_surface = self.shadow_font.render(text, True, self.shadow_font_color)
            shadow_rect = shadow_surface.get_rect(center = self.midtop)
            shadow_rect.move_ip(SHADOW_OFFSET, font_size * (2*i + 1) + SHADOW_OFFSET)

            self.surf_rect_list.append({
            "surf": shadow_surface,
            "rect": shadow_rect
            })

            self.surf_rect_list.append({
            "surf": text_surface,
            "rect": text_rect
            })

            self.menu_width = max(self.menu_width, text_rect.width + 2 * font_size)
        self.ready_to_draw = True

    def draw(self, screen):
        if not(self.ready_to_draw):
            self.init_draw_list()

        font_size = self.font.get_height()

        menu_height = font_size * (2 * len(self.items) + 1)
        menu_rect = pygame.Rect(0, 0, self.menu_width, menu_height )
        menu_rect.midtop = self.midtop

        menu_surf = pygame.Surface(menu_rect.size)
        menu_surf.fill(self.menu_color)
        menu_surf.set_alpha(255//2, RLEACCEL)

        screen.blit(menu_surf, menu_rect)

        selection_rect = self.surf_rect_list[self.current_index * 2]["rect"].copy()
        selection_center = selection_rect.center
        selection_rect.width += 10
        selection_rect.height += 5
        selection_rect.center = selection_center

        selection_surf = pygame.Surface(selection_rect.size)
        selection_surf.fill(self.selection_color)
        selection_surf.set_alpha(255//2, RLEACCEL)

        screen.blit(selection_surf, selection_rect)
        for drawable in self.surf_rect_list:
            screen.blit(drawable["surf"], drawable["rect"])
