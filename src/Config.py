class MovingDirection:
    LEFT = (-1, 0),
    RIGHT = (1, 0),
    UP = (0, -1),
    DOWN = (0, 1),
    IDLE = (0, 0)


MISSILE_SPEED = {'default': 500,
                 'launcher': 250,
                 'minigun': 2500}

WINDOW_SIZE = (400, 525)
GAME_SPACE = (400, 500)
UPDATE_PERIOD_MS = 5
DRAW_PERIOD_MS = 5

SPRITE_DIRECTORY = "sprite/"

BUNKER_SPRITE = "bunker.png"
BUNKER_POSITIONS = [
    ((GAME_SPACE[0] // 18) + (GAME_SPACE[0] // 9 * 1), GAME_SPACE[1] * 8 // 10),
    ((GAME_SPACE[0] // 18) + (GAME_SPACE[0] // 9 * 3), GAME_SPACE[1] * 8 // 10),
    ((GAME_SPACE[0] // 18) + (GAME_SPACE[0] // 9 * 5), GAME_SPACE[1] * 8 // 10),
    ((GAME_SPACE[0] // 18) + (GAME_SPACE[0] // 9 * 7), GAME_SPACE[1] * 8 // 10)
]
BUNKER_DESTRUCTION_PROBABILITY = 0.7
LASER_BUNKER_EXPLOSION_RADIUS = 7
MISSILE_BUNKER_EXPLOSION_RADIUS = 4

STARTING_LIFE_COUNT = 3
LIFE_COUNT_POS = (GAME_SPACE[0] // 20, GAME_SPACE[1] + 3)
LIFE_POS = (GAME_SPACE[0] // 10, GAME_SPACE[1] + 3)
LIFE_POS_SHIFT = (3, 0)

SPACESHIP_SPRITE = "spaceship.png"
SPACESHIP_EXPLOSION_SPRITE = "spaceship_explosion.png"
SPACESHIP_STARTING_POSITION = (GAME_SPACE[0] // 2, GAME_SPACE[1] * 9 // 10)
SPACESHIP_SPEED_PIXEL_PER_SECOND = 100
SPACESHIP_EXPLOSION_DURATION_MS = 1000

MISSILE_EXPLOSION_SPRITE = "missile_explosion.png"
MISSILE_RECT_DIM = (2, 6)
MISSILE_RECT_COLOR = (0, 255, 0)
MISSILE_SPEED_PIXEL_PER_SECOND = 500
MINIGUN_MISSILE_SPEED_PIXEL_PER_SECOND = 1000

INVADER_SPRITES = [
    ["invader1_frame1.png", "invader1_frame2.png"],
    ["invader2_frame1.png", "invader2_frame2.png"],
    ["invader3_frame1.png", "invader3_frame2.png"]
]
INVADER_EXPLOSION_SPRITE = "invader_explosion.png"
INVADER_FORMATION = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
INVADER_FORMATION_WIDTH_PIXELS = 344
INVADER_SPEED_PIXEL_PER_SECOND = 10
INVADER_FIRING_PERIOD_MS = 1000
INVADER_SPRITE_SHIFT_PERIOD_MS = 500
INVADER_STARTING_POS_Y = GAME_SPACE[1] * 3 // 10
INVADER_EXPLOSION_DURATION_MS = 250

MYSTERY_SHIP_SPRITE = "mystery_ship.png"
MYSTERY_SHIP_EXPLOSION_SPRITE = "mystery_ship_explosion.png"
MYSTERY_SHIP_SPEED_PIXEL_PER_SECOND = 100
MYSTERY_SHIP_STARTING_POS_Y = GAME_SPACE[1] * 2 // 10
MYSTERY_SHIP_APPEAR_PERIOD_SECONDS = 30
MYSTERY_SHIP_EXPLOSION_DURATION_MS = 1000

LASER_SPRITES = [
    ["laser1_frame1.png", "laser1_frame2.png", "laser1_frame3.png", "laser1_frame4.png"],
    ["laser2_frame1.png", "laser2_frame2.png", "laser2_frame3.png", "laser2_frame4.png"],
    ["laser3_frame1.png", "laser3_frame2.png", "laser3_frame3.png", "laser3_frame4.png"]
]
LASER_EXPLOSION_SPRITE = "laser_explosion.png"
LASER_RECT_DIM = (2, 12)
LASER_SPEED_PIXEL_PER_SECOND = 100

SCORE_SPRITE = "score.png"
HIGH_SCORE_SPRITE = "high_score.png"
SCORE_DIGIT_COUNT = 4
SCORE_BETWEEN_DIGIT_SPACE_PIXELS = 4
SCORE_POS = (GAME_SPACE[0] // 10, GAME_SPACE[1] // 10)
HIGH_SCORE_POS = (GAME_SPACE[0] // 10 * 5, GAME_SPACE[1] // 10)

GAME_OVER_SPRITE = "game_over.png"

SOUND_DIRECTORY = "sound/"

SPACESHIP_SHOOT_SOUND = "spaceship_shoot.wav"
SPACESHIP_DESTRUCTION_SOUND = "spaceship_destroyed.wav"
INVADER_DESTRUCTION_SOUND = "invader_destroyed.wav"
INVADERS_MOVE_SOUNDS = [
    "invader_movements1.wav",
    "invader_movements2.wav",
    "invader_movements3.wav",
    "invader_movements4.wav",
    "invader_movements5.wav",
    "invader_movements6.wav"
]

MYSTERY_SHIP_SOUND = "mystery_ship.wav"
MYSTERY_SHIP_DESTRUCTION_SOUND = "mystery_ship_destroyed.wav"
EXTRA_LIFE_SOUND = "extra_life.wav"
