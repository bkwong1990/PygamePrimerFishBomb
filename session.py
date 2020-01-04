class Session:
    def __init__(self, screen, config_dict):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config_dict = config_dict
