import pico2d

HUD_PATH = "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/HUD/"

def load_hud_images():
    hud_back = pico2d.load_image(HUD_PATH + "HUD-Back.png")
    hp_bar = pico2d.load_image(HUD_PATH + "HPBarVar1.png")
    mana_bar = pico2d.load_image(HUD_PATH + "ManaBarVar1.png")
    skill_slots = pico2d.load_image(HUD_PATH + "SkillSlotsWithButtons.png")
    hud_front = pico2d.load_image(HUD_PATH + "HUD-Front.png")
    left_demon = pico2d.load_image(HUD_PATH + "LeftDemon.png")
    right_angel = pico2d.load_image(HUD_PATH + "RightAngel.png")

    return hud_back, hp_bar, mana_bar, skill_slots, hud_front, left_demon, right_angel

class HUD:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.hud_back, self.hp_bar, self.mana_bar, self.skill_slots, \
        self.hud_front, self.left_demon, self.right_angel = load_hud_images()

        self.scale_x = screen_width / self.hud_back.w
        self.hud_center_x = screen_width // 2
        self.hud_bottom_y = self.hud_back.h * self.scale_x / 2

    def draw(self):
        self.hud_back.draw(self.hud_center_x, self.hud_bottom_y, self.screen_width, self.hud_back.h * self.scale_x)

        hp_x = self.hp_bar.w * self.scale_x / 2
        hp_y = self.hp_bar.h * self.scale_x / 2
        self.hp_bar.draw(hp_x, hp_y, self.hp_bar.w * self.scale_x, self.hp_bar.h * self.scale_x)

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

        self.hud_front.draw(self.hud_center_x, self.hud_bottom_y, self.hud_front.w * self.scale_x, self.hud_front.h * self.scale_x)

def create_hud(screen_width, screen_height):
    return HUD(screen_width, screen_height)