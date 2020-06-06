import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"


class FirstGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Hello", 20, 60, arcade.csscolor.SEA_GREEN)
        arcade.draw_line(20, 50, 80, 50, arcade.csscolor.SEA_GREEN)


def main():
    game = FirstGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
