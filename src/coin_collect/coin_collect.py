import arcade
import random

# Window
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Scaling
CHARACTER_SCALING = 0.75
COIN_SCALING = 0.5
MIN_BOX_SCALING = 0.25
MAX_BOX_SCALING = 0.35
TILE_SCALING = 0.5

# Map properties
COIN_COUNT = 15
BOX_COUNT = 5
GROUND_CENTER_Y = 32
TILE_SIZE = 64

# Engine
PLAYER_MOVEMENT_SPEED = 5

# Resources
COLLECT_COIN_WAV = ":resources:sounds/coin2.wav"
PLAYER_TEXTURE = "static/player_stand.png"
COIN_TEXTURE = "static/coinGold.png"
FRAME_TEXTURE = ":resources:images/tiles/brickGrey.png"
GROUND_TEXTURE = ":resources:images/tiles/grassMid.png"
WATER_TEXTURE = ":resources:images/tiles/water.png"
COAST_TEXTURE = ":resources:images/tiles/grassHill_left.png"
BOX_TEXTURE = ":resources:images/tiles/boxCrate_double.png"
COMPLETED_TEXT = "Nyert\u00e9l!!"

GRAVITY = 0.02


class Game(arcade.Window):

    def __init__(self):
        # Window configurations
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        # Player
        self.player = None

        # Game properties
        self.score = 0
        self.level_completed = False

        # Physics engine
        self.physics_engine = None

        # Sounds
        self.collect_coin_sound = arcade.load_sound(COLLECT_COIN_WAV)

    def setup(self):
        self.score = 0
        self.level_completed = False

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self._setup_players()
        self._setup_coins()
        self._setup_walls()

        # self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY)


    def _setup_players(self):
        self.player = arcade.Sprite(PLAYER_TEXTURE, CHARACTER_SCALING)
        self.player.center_x = random.randrange(SCREEN_WIDTH - TILE_SIZE)
        self.player.center_y = max(random.randrange(SCREEN_HEIGHT), 3 * GROUND_CENTER_Y)
        self.player_list.append(self.player)

    def _setup_coins(self):
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(COIN_TEXTURE, COIN_SCALING)
            coin.center_x = random.randrange(SCREEN_WIDTH - TILE_SIZE)
            coin.center_y = max(random.randrange(SCREEN_HEIGHT), 2.5 * GROUND_CENTER_Y)
            self.coin_list.append(coin)

    def _setup_walls(self):
        # Window frame
        for i in range(0, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
            top_frame = arcade.Sprite(FRAME_TEXTURE, TILE_SCALING)
            top_frame.center_x = i
            top_frame.center_y = SCREEN_HEIGHT + (TILE_SIZE / 2)
            self.wall_list.append(top_frame)

            bottom_frame = arcade.Sprite(FRAME_TEXTURE, TILE_SCALING)
            bottom_frame.center_x = i
            bottom_frame.center_y = -(TILE_SIZE / 2)
            self.wall_list.append(bottom_frame)

        for i in range(0, SCREEN_HEIGHT + TILE_SIZE, TILE_SIZE):
            right_frame = arcade.Sprite(FRAME_TEXTURE, TILE_SCALING)
            right_frame.center_x = SCREEN_WIDTH + (TILE_SIZE / 2)
            right_frame.center_y = i
            self.wall_list.append(right_frame)

            left_frame = arcade.Sprite(FRAME_TEXTURE, TILE_SCALING)
            left_frame.center_x = -(TILE_SIZE / 2)
            left_frame.center_y = i
            self.wall_list.append(left_frame)

        # Grass tiles
        for i in range(0, SCREEN_WIDTH - (2 * TILE_SIZE), TILE_SIZE):
            wall = arcade.Sprite(GROUND_TEXTURE, TILE_SCALING)
            wall.center_x = i
            wall.center_y = GROUND_CENTER_Y
            self.wall_list.append(wall)

        # Water tiles
        for i in range(SCREEN_WIDTH - (2 * TILE_SIZE), SCREEN_WIDTH + TILE_SIZE, TILE_SIZE):
            water = arcade.Sprite(WATER_TEXTURE, TILE_SCALING)
            water.center_x = i
            water.center_y = GROUND_CENTER_Y
            self.wall_list.append(water)

        # Transition between ground and water
        coast = arcade.Sprite(COAST_TEXTURE, TILE_SCALING)
        coast.center_x = SCREEN_WIDTH - (2 * TILE_SIZE)
        coast.center_y = GROUND_CENTER_Y
        self.wall_list.append(coast)

        # Random box tiles
        for i in range(BOX_COUNT):
            box = arcade.Sprite(BOX_TEXTURE, random.uniform(MIN_BOX_SCALING, MAX_BOX_SCALING))
            box.center_x = random.randrange(SCREEN_WIDTH - TILE_SIZE)
            box.center_y = max(random.randrange(SCREEN_HEIGHT), 2.5 * GROUND_CENTER_Y)
            self.wall_list.append(box)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        arcade.draw_text(f"Score: {self.score}/{COIN_COUNT}", 10, SCREEN_HEIGHT - 50, arcade.csscolor.WHITE, 18)

        if self.level_completed:
            arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3,
                                         arcade.csscolor.MIDNIGHT_BLUE)
            arcade.draw_text(COMPLETED_TEXT, SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20,
                             arcade.csscolor.WHITE, 40)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif symbol in (arcade.key.NUM_ENTER, arcade.key.ENTER):
            self.restart_level()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif symbol in (arcade.key.RIGHT, arcade.key.LEFT):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        self.score = COIN_COUNT - len(self.coin_list)
        if self.score == COIN_COUNT:
            self.level_completed = True

    def restart_level(self):
        self.setup()


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
