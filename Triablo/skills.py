import pico2d

class SkillsManager:
    def __init__(self):
        self.current_mode = None

    def handle_input(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_1:
                    self.switch_mode('Magic_Arrow')
                elif event.key == pico2d.SDLK_2:
                    self.switch_mode('Fire_Arrow')
                elif event.key == pico2d.SDLK_3:
                    self.switch_mode('Multiple_Arrow')
                elif event.key == pico2d.SDLK_4:
                    self.switch_mode('Exploding_Arrow')

    def switch_mode(self, new_mode):
        self.current_mode = new_mode if self.current_mode != new_mode else None

    def get_current_mode(self):
        return self.current_mode or "None"

