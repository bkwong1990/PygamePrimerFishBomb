class Session:
    def __init__(self, screen, config_info):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.config_info = config_info
