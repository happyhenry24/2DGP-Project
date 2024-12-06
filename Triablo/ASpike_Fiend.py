import pico2d
import random

direction_order_8 = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']

def get_spike_fiend_data():
    return {
        "name": "Spike Fiend",
        "hp": 10,
        "attack_damage": 5,
        "chase_distance": 200,
        "attack_distance": 50,
        "image_paths": {
            "idle": "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Idle/",
            "walk": "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Walk/",
            "hit": "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Get_hit/",
            "attack": "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Attack/",
            "death": "C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Death/",
        },
        "frame_counts": {
            "idle": 8,
            "walk": 9,
            "hit": 6,
            "attack": 16,
            "death": 14,
        },
    }
