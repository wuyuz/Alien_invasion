class Settings():
    '''
    储存《外星人入侵》的所有设置类
    '''
    def __init__(self):
        '''
        初始化设置
        '''
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # 飞船
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,0,0
        self.bullet_allowed = 5

        # 外星人
        self.alien_speed_factor = 1
        # 设置外星人方向
        self.fleet_drop_speed = 50
        self.fleet_direction = 1    # 如果是负数就是反方向


