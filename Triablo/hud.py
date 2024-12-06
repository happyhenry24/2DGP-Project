import pico2d

HUD_PATH = "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/HUD/"
FILTER_PATH = "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/user interface/filter/"

class HUD:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.hud_images = {
            "FilterVignette": pico2d.load_image(FILTER_PATH + "filter_vignette.png"),
            "HUD-Back": pico2d.load_image(HUD_PATH + "HUD-Back.png"),
            "HPBarVar1": pico2d.load_image(HUD_PATH + "HPBarVar1.png"),
            "ManaBarVar1": pico2d.load_image(HUD_PATH + "ManaBarVar1.png"),
            "SkillSlotsWithButtons": pico2d.load_image(HUD_PATH + "SkillSlotsWithButtons.png"),
            "HUD-Front": pico2d.load_image(HUD_PATH + "HUD-Front.png"),
            "LeftDemon": pico2d.load_image(HUD_PATH + "LeftDemon.png"),
            "RightAngel": pico2d.load_image(HUD_PATH + "RightAngel.png"),
            "HP_Potion_Small": pico2d.load_image(HUD_PATH + "HP_Potion_Small.png"),
            "HP_Potion_Big": pico2d.load_image(HUD_PATH + "HP_Potion_Big.png"),
            "Mana_Potion_Small": pico2d.load_image(HUD_PATH + "Mana_Potion_Small.png"),
            "Mana_Potion_Big": pico2d.load_image(HUD_PATH + "Mana_Potion_Big.png"),

        }

        self.hp_images = self.load_images([f"HP/HPBarVar1_{i:02}.png" for i in range(63)])
        self.mana_images = self.load_images([f"Mana/ManaBarVar1_{i:02}.png" for i in range(63)])
        self.skill_images = self.load_images({
            'Magic_Arrow': "Magic_Arrow.png",
            'Magic_Arrow_Off': "Magic_Arrow_Off.png",
            'Fire_Arrow': "Fire_Arrow.png",
            'Fire_Arrow_Off': "Fire_Arrow_Off.png",
            'Multiple_Arrow': "Multiple_Arrow.png",
            'Multiple_Arrow_Off': "Multiple_Arrow_Off.png",
            'Exploding_Arrow': "Exploding_Arrow.png",
            'Exploding_Arrow_Off': "Exploding_Arrow_Off.png",
        })

        self.scale_x = screen_width / self.hud_images["HUD-Back"].w
        self.hud_center_x = screen_width // 2
        self.hud_bottom_y = self.hud_images["HUD-Back"].h * self.scale_x / 2

    def draw_potions(self):
        skill_slots = self.hud_images["SkillSlotsWithButtons"]
        potion_images = ["HP_Potion_Small", "HP_Potion_Big", "Mana_Potion_Small", "Mana_Potion_Big"]
        for potion in potion_images:
            if potion in self.hud_images:
                potion_image = self.hud_images[potion]
                potion_image.draw(
                    self.hud_center_x,
                    self.hud_bottom_y,
                    skill_slots.w * self.scale_x,
                    skill_slots.h * self.scale_x
                )

    def remove_potion(self, potion_name):
        if potion_name in self.hud_images:
            del self.hud_images[potion_name]

    def add_potion(self, potion_name):
        if potion_name not in self.hud_images:
            self.hud_images[potion_name] = pico2d.load_image(
                f"C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/HUD/{potion_name}.png"
            )

    def load_images(self, paths):
        if isinstance(paths, dict):
            return {key: pico2d.load_image(HUD_PATH + path) for key, path in paths.items()}
        return [pico2d.load_image(HUD_PATH + path) for path in paths]

    def draw_mana_bar(self, current_mana):
        mana_image = self.mana_images[max(0, min(62, current_mana))]
        self.draw_image(mana_image)

    def draw(self, current_hp, current_mana, current_mode):
        self.hud_images["FilterVignette"].draw(self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

        back = self.hud_images["HUD-Back"]
        front = self.hud_images["HUD-Front"]
        left_demon = self.hud_images["LeftDemon"]
        right_angel = self.hud_images["RightAngel"]
        skill_slots = self.hud_images["SkillSlotsWithButtons"]
        hp_bar = self.hud_images["HPBarVar1"]
        mana_bar = self.hud_images["ManaBarVar1"]

        back.draw(self.hud_center_x, self.hud_bottom_y, self.screen_width, back.h * self.scale_x)
        self.draw_hp_bar(current_hp, hp_bar)
        self.draw_mana_bar(current_mana)

        skill_slots.draw(self.hud_center_x, self.hud_bottom_y, skill_slots.w * self.scale_x,
                         skill_slots.h * self.scale_x)
        self.draw_image(left_demon, x_offset=0, y_offset=0)
        self.draw_image(right_angel, x_offset=0, y_offset=0, right_align=True)

        front.draw(self.hud_center_x, self.hud_bottom_y, front.w * self.scale_x, front.h * self.scale_x)
        self.draw_skills(current_mode)
        self.draw_potions()

    def draw_hp_bar(self, current_hp, hp_bar):
        hp_image = self.hp_images[max(0, min(62, current_hp))]
        self.draw_image(hp_image)

    def draw_skills(self, current_mode):
        skill_x = self.hud_center_x
        skill_y = self.hud_bottom_y

        for skill in ['Magic_Arrow', 'Fire_Arrow', 'Multiple_Arrow', 'Exploding_Arrow']:
            image_key = skill if current_mode == skill else f"{skill}_Off"
            image = self.skill_images[image_key]
            image.draw(skill_x, skill_y, image.w * self.scale_x, image.h * self.scale_x)

    def draw_image(self, image, x_offset=0, y_offset=0, right_align=False):
        if right_align:
            x = self.screen_width - (image.w * self.scale_x / 2) + x_offset
        else:
            x = self.hud_center_x + x_offset
        y = (image.h * self.scale_x / 2) + y_offset
        image.draw(x, y, image.w * self.scale_x, image.h * self.scale_x)


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
