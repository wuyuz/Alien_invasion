import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien   # 这里需要调用alien 模块


# 鼠标事件主程序入口
def check_events(ai_settings,screen,stats,play_button,ship,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 属性返回哪种事件类型被触发
            sys.exit()
        elif event.type == pygame.KEYDOWN: # 单击按键
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:  # 松开键盘
            check_keyup_events(event,ship)

        # 开始按键
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y)


def check_play_button(stats,play_button,mouse_x,mouse_y):
    '''再玩家单击play按钮时开始游戏'''
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        stats.game_active = True


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    # 响应按键
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)


def check_keyup_events(event,ship):
    # 响应松键
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):  # 这里在这个模板中可以不导入其他模块
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 让最近绘制的屏幕可见
    ship.blitme()
    aliens.draw(screen)

    # 如果游戏非活动状态，就绘制play
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def get_number_alien_x(ai_settings,alien_width):
    # 计算一行能容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    '''创建外星人群'''
    # 创建一个外星人，并计算一行可容纳多外星人
    # 外外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)  # 这里有实例化所以就需要调用alien模块
    number_alien_x = get_number_alien_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    # 创建第多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def update_bullets(ai_settings,screen,ship,aliens,bullets):
    '''更新子弹的位置，并删除消失的子弹'''
    # 更新子弹的位置
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中外星人
    # 如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets)

def get_number_rows(ai_settings,ship_height,alien_height):
    '''计算屏幕可容纳多少行'''
    available_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def check_fleet_edges(ai_settings,aliens):
    '''有外星人达到边缘时采取的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):
    '''整个外星人群下移，并改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_alien(ai_settings,stats,screen,ship,aliens,bullets):
    '''检查是否外星人到达边缘，更新外星人所有的位置'''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)


def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets):
    '''响应子弹和外星人的碰撞'''
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens,True,True)
    if len(aliens) == 0:
        # 删除现有的所有子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    '''响应被外星人撞到飞船'''
    if stats.ships_left>0:
        # 将ship_limit减一
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群外星人，并将飞船放到屏幕底端中间
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else: stats.game_active = False

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    '''检查是否有外星人到达屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船撞到一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break