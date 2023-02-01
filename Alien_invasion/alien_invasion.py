import pygame
from setting import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Buttton
from scoreboard import Scoreboard

def run_game():
    ''' 初始化游戏并创建一个屏幕对象 '''
    pygame.init()  # 初始化背景设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 定义了一个显示窗口，所有的东西都在这个窗口显示
    pygame.display.set_caption('Alien Invasion')  # 设置窗口的名称
    play_button = Buttton(ai_settings, screen, "PLAY")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    bg_color = (255, 255, 255)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
