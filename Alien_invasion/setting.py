class Settings():
    '''存储此项目中所有设置的类'''

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)  # 使用的RGB颜色数值
        self.ship_speed_factor = 1.5  # 飞船移动速度
        self.bullet_speed_factor = 3  # 子弹速度
        self.bullet_width = 5  # 子弹宽度
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60  # 子弹的颜色
        self.bullets_allowed = 5  # 允许屏幕中出现的子弹数量
        self.alien_speed_factor = 0.5  # 外星人移动的速度
        self.fleet_drop_speed = 1  # 外星人下降的速度
        self.fleet_diretion = 1  # 1表示向右移动，-1表示向左移动
        self.ship_limit = 3  # 飞船的数量限制
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_diretion = 1
        self.alien_point = 50


    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_point * self.score_scale)
        #print(self.alien_points)
