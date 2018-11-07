import sys
import pygame

from setting import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    # 创建一个设置实例
    ai_settings = Settings()
    # 创建一个屏幕
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # 创建一个Play键
    play_button = Button(ai_settings,screen,'Play')
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建一艘飞船
    ship = Ship(ai_settings,screen)
    # 创建以个用于储存子弹的编组
    bullets = Group()  # Group 是创建一个类似列表的，里面可以装子弹的实例
    # 创建一个外星人
    alien = Alien(ai_settings,screen)
    # 创建一个外星人编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    while True:
        # 导入game_function的检查函数函数
        gf.check_events(ai_settings,screen,stats,play_button,ship,bullets)
        if stats.game_active:
            # 更新飞船最新位置
            ship.update()
            # 更新子弹最新位置,并删除过期子弹
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            # 更新外星人的位置
            gf.update_alien(ai_settings, stats,screen,ship, aliens,bullets)
            # 调用gf的update_screen方法，在屏幕绘出图像
        gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button)



run_game()