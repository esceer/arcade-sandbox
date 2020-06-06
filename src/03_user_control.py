import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CHARACTER_SCALING = 0.75
COIN_SCALING = 0.5
TILE_SCALING = 0.5

COIN_COUNT = 10
GROUND_CENTER_Y = 32

PLAYER_MOVEMENT_SPEED = 5


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        print(arcade.__version__)

        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        self.player = None

        self.physics_engine = None

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self._setup_players()
        self._setup_coins()
        self._setup_walls()

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def _setup_players(self):
        self.player = arcade.Sprite("static/player_stand.png", CHARACTER_SCALING)
        self.player.center_x = random.randrange(SCREEN_WIDTH)
        self.player.center_y = max(random.randrange(SCREEN_HEIGHT), 2.5 * GROUND_CENTER_Y)
        self.player_list.append(self.player)

    def _setup_coins(self):
        for i in range(10):
            coin = arcade.Sprite("static/coinGold.png", COIN_SCALING)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = max(random.randrange(SCREEN_HEIGHT), 2.5 * GROUND_CENTER_Y)
            self.coin_list.append(coin)

    def _setup_walls(self):
        for i in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = i
            wall.center_y = GROUND_CENTER_Y
            self.wall_list.append(wall)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        arcade.play_sound(self.collect_coin_sound)
        if symbol == arcade.key.UP:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.player.change_y = 0
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.LEFT:
            self.player.change_x = 0

    def update(self, delta_time: float):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_hit_list:
            coin.kill()
            arcade.play_sound(self.collect_coin_sound)


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
