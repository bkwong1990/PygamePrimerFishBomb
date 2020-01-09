import pygame

from pygame.locals import (
KEYDOWN,
QUIT,
K_UP,
K_DOWN,
RLEACCEL
)

SHADOW_OFFSET = 3

# A menu item that can contain its own functionality
class MenuItem:
    '''
    Makes a new menu item
    Parameters:
        self: the object being created
        text: the text to represent the menu item
        menu_fun: a function to be called if the menu item is selected while receiving keyboard input
    '''
    def __init__(self, text, menu_fun = None):
        self.text = text
        #function that takes a key parameter
        self.menu_fun = menu_fun


# A menu of vertical items
class VerticalMenu:

    '''
    Creates a new vertica menu
    Parameters:
        self: the object being created
        font: the font to be used for the menu text
        font_color: the color of the font
        shadow_font_color: the color of the text shadow
        menu_color: the color of the menu's containing rectangle
        selection_color: the color to be used for the selection rectangle
        midtop: the coordinates of the middle of the menu's top side
    '''
    def __init__(self, font, font_color, shadow_font_color, menu_color, selection_color, midtop):
        self.items = []
        self.font = font
        self.font_color = font_color
        self.shadow_font_color = shadow_font_color
        self.menu_color = menu_color
        self.selection_color = selection_color
        self.midtop = midtop
        self.current_index = None

        self.surf_rect_list = []
        self.menu_width = 0

        self.ready_to_draw = False

    '''
    Adds a new item to the menu
    Parameters:
        self: the calling object
        text: the text representing the item
        menu_fun: the function to be called when interacting with the item
    '''
    def add(self, text, menu_fun = None):
        self.items.append( MenuItem( text, menu_fun ) )
        if len(self.items) > 0:
            self.current_index = 0
        self.ready_to_draw = False

    '''
    Sets the text of the current selection
    Parameters:
        self: the calling object
        text: the new text
    '''
    def set_text_current_selection(self, text):
        self.items[self.current_index].text = text
        self.ready_to_draw = False

    '''
    Processes key input. Up and down changes the current selection, other keys
    are sent to the item to be processed
    Parameters:
        self: the calling object
        key: the key being pressed
    '''
    def process_input(self, key):

        if key == K_UP :
            self.current_index = (self.current_index - 1) % len(self.items)
        elif key == K_DOWN :
            self.current_index = (self.current_index + 1) % len(self.items)
        # It's possible the selected item has no function
        elif self.items[self.current_index].menu_fun:
            self.items[self.current_index].menu_fun(key)

    '''
    Initializes a list of surfaces and rectangles to be drawn to screen.
    Parameters:
        self: the calling object
    '''
    def init_surf_rect_list(self):
        font_size = self.font.get_height()
        self.surf_rect_list = []
        for i in range(len( self.items ) ):
            text = self.items[i].text
            text_surface = self.font.render(text, True, self.font_color)
            text_rect = text_surface.get_rect(center = self.midtop)
            text_rect.move_ip(0, font_size * (2*i + 1))
            #Shadow should be drawn
            shadow_surface = self.font.render(text, True, self.shadow_font_color)
            shadow_rect = shadow_surface.get_rect(center = text_rect.center)
            shadow_rect.move_ip(SHADOW_OFFSET, SHADOW_OFFSET)

            self.surf_rect_list.append({
            "surf": shadow_surface,
            "rect": shadow_rect
            })

            self.surf_rect_list.append({
            "surf": text_surface,
            "rect": text_rect
            })
            # Determine how wide the menu needs to be, including margins
            self.menu_width = max(self.menu_width, text_rect.width + 2 * font_size)
        self.ready_to_draw = True

    '''
    Draws the menu to the screen
    Parameters:
        self: the calling object
        screen: the surface of the window
    '''
    def draw(self, screen):
        # if the list of surfaces is not already initialized or the item list changed in any way
        if not(self.ready_to_draw):
            self.init_surf_rect_list()

        font_size = self.font.get_height()
        # Makes the menu tall enough for all items
        menu_height = font_size * (2 * len(self.items) )
        menu_rect = pygame.Rect(0, 0, self.menu_width, menu_height )
        menu_rect.midtop = self.midtop

        menu_surf = pygame.Surface(menu_rect.size)
        menu_surf.fill(self.menu_color)
        menu_surf.set_alpha(255//2, RLEACCEL)



        selection_rect = self.surf_rect_list[self.current_index * 2]["rect"].copy()
        selection_center = selection_rect.center

        # Margin for the selection rectangle
        selection_rect.width += 10
        selection_rect.height += 5
        # Center is reassigned just in case
        selection_rect.center = selection_center

        selection_surf = pygame.Surface(selection_rect.size)
        selection_surf.fill(self.selection_color)
        selection_surf.set_alpha(255//2, RLEACCEL)
        
        screen.blit(menu_surf, menu_rect)
        screen.blit(selection_surf, selection_rect)
        for drawable in self.surf_rect_list:
            screen.blit(drawable["surf"], drawable["rect"])
