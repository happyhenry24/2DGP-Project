import pico2d

HUD_PATH = "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/HUD/"

class HUD:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.hud_back, self.hp_bar, self.mana_bar, self.skill_slots, self.hud_front, self.left_demon, self.right_angel = self.load_hud_images()
        self.hp_images = self.load_hp_images()

        self.skill_images = {
            'Magic_Arrow': pico2d.load_image(HUD_PATH + "Magic_Arrow.png"),
            'Magic_Arrow_Off': pico2d.load_image(HUD_PATH + "Magic_Arrow_Off.png"),
            'Fire_Arrow': pico2d.load_image(HUD_PATH + "Fire_Arrow.png"),
            'Fire_Arrow_Off': pico2d.load_image(HUD_PATH + "Fire_Arrow_Off.png"),
            'Multiple_Arrow': pico2d.load_image(HUD_PATH + "Multiple_Arrow.png"),
            'Multiple_Arrow_Off': pico2d.load_image(HUD_PATH + "Multiple_Arrow_Off.png"),
            'Exploding_Arrow': pico2d.load_image(HUD_PATH + "Exploding_Arrow.png"),
            'Exploding_Arrow_Off': pico2d.load_image(HUD_PATH + "Exploding_Arrow_Off.png")
        }

        self.current_active_skill = None

        self.scale_x = screen_width / self.hud_back.w
        self.hud_center_x = screen_width // 2
        self.hud_bottom_y = self.hud_back.h * self.scale_x / 2

    def load_hud_images(self):
        hud_back = pico2d.load_image(HUD_PATH + "HUD-Back.png")
        hp_bar = pico2d.load_image(HUD_PATH + "HPBarVar1.png")
        mana_bar = pico2d.load_image(HUD_PATH + "ManaBarVar1.png")
        skill_slots = pico2d.load_image(HUD_PATH + "SkillSlotsWithButtons.png")
        hud_front = pico2d.load_image(HUD_PATH + "HUD-Front.png")
        left_demon = pico2d.load_image(HUD_PATH + "LeftDemon.png")
        right_angel = pico2d.load_image(HUD_PATH + "RightAngel.png")
        return hud_back, hp_bar, mana_bar, skill_slots, hud_front, left_demon, right_angel

    def load_hp_images(self):
        return [pico2d.load_image(f"{HUD_PATH}HP/HPBarVar1_{i:02}.png") for i in range(63)]

    def draw_hp_bar(self, current_hp):
        hp_index = max(0, min(62, current_hp))
        hp_image = self.hp_images[hp_index]
        hp_x = hp_image.w * self.scale_x / 2
        hp_y = hp_image.h * self.scale_x / 2
        hp_image.draw(hp_x, hp_y, hp_image.w * self.scale_x, hp_image.h * self.scale_x)

    def draw(self, current_hp):
        self.hud_back.draw(self.hud_center_x, self.hud_bottom_y, self.screen_width, self.hud_back.h * self.scale_x)
        self.draw_hp_bar(current_hp)

        mana_x = self.screen_width - (self.mana_bar.w * self.scale_x / 2)
        mana_y = self.mana_bar.h * self.scale_x / 2
        self.mana_bar.draw(mana_x, mana_y, self.mana_bar.w * self.scale_x, self.mana_bar.h * self.scale_x)

        skill_x = self.hud_center_x
        skill_y = self.hud_bottom_y
        self.skill_slots.draw(skill_x, skill_y, self.skill_slots.w * self.scale_x, self.skill_slots.h * self.scale_x)

        demon_x = self.left_demon.w * self.scale_x / 2
        demon_y = self.left_demon.h * self.scale_x / 2
        self.left_demon.draw(demon_x, demon_y, self.left_demon.w * self.scale_x, self.left_demon.h * self.scale_x)

        angel_x = self.screen_width - (self.right_angel.w * self.scale_x / 2)
        angel_y = self.right_angel.h * self.scale_x / 2
        self.right_angel.draw(angel_x, angel_y, self.right_angel.w * self.scale_x, self.right_angel.h * self.scale_x)

        self.hud_front.draw(self.hud_center_x, self.hud_bottom_y, self.hud_front.w * self.scale_x,
                            self.hud_front.h * self.scale_x)

        self.draw_skills()

    def draw_skills(self):
        skill_x = self.hud_center_x
        skill_y = self.hud_bottom_y

        skills = ['Magic_Arrow', 'Fire_Arrow', 'Multiple_Arrow', 'Exploding_Arrow']
        for skill in skills:
            image = self.skill_images[skill if self.current_active_skill == skill else f"{skill}_Off"]
            image.draw(skill_x, skill_y, image.w * self.scale_x, image.h * self.scale_x)

    def toggle_skill(self, skill_name):
        self.current_active_skill = skill_name if self.current_active_skill != skill_name else None

    def handle_hud_events(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_1:
                    self.toggle_skill('Magic_Arrow')
                elif event.key == pico2d.SDLK_2:
                    self.toggle_skill('Fire_Arrow')
                elif event.key == pico2d.SDLK_3:
                    self.toggle_skill('Multiple_Arrow')
                elif event.key == pico2d.SDLK_4:
                    self.toggle_skill('Exploding_Arrow')

class MonsterHPBar:
    def __init__(self, monster):
        self.monster = monster
        self.bar_width = 20
        self.bar_height = 4
        self.hp = monster.hp
        self.red_hp = pico2d.load_image("C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/RedHP.png")
        self.white_hp = pico2d.load_image("C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/WhiteHP.png")

    def update_hp(self, hp):
        self.hp = hp

    def draw(self, camera_x, camera_y):
        filled_width = int((self.hp / self.monster.max_hp) * self.bar_width)

        for i in range(filled_width):
            self.red_hp.draw(self.monster.x - camera_x - self.bar_width // 2 + i, self.monster.y - camera_y + 40)

        for i in range(filled_width, self.bar_width):
            self.white_hp.draw(self.monster.x - camera_x - self.bar_width // 2 + i, self.monster.y - camera_y + 40)
