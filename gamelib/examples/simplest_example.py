"""
Simplest example of the use of the library.
"""
import pygame as pg
from gamelib import get_game, scene_manager, BaseScene, SoundManager


class MyScene(BaseScene):
    pass


pg.init()
game = get_game()
mixer = SoundManager()
scene_manager.init(game, mixer)
scene_manager.spawn_scene(MyScene)


@game.frame
def frame(window: pg.Surface, delta_time: int):
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            game.stop()
        else:
            scene_manager.handle_events(ev)

    scene_manager.update(delta_time)

    window.fill((0, 0, 0))

    scene_manager.draw(window)

    pg.display.update()


def main():
    game.init()
    game.run()


if __name__ == '__main__':
    main()
