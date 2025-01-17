from . import ui


class MainMenuScene(ui.Scene):
    def redraw(self, screen):
        screen.clear_screen(screen.RGB(0x888888))