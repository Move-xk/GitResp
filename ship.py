import pygame


class Ship():

    def __init__(self, screen, ai_settings):
        self.screen = screen  # 初始化飞船并且设置其初始位置
        self.ai_settings = ai_settings
        self.image = pygame.image.load('Image/ship.bmp')  # 加载飞船图像并获取其外接矩形
        self.rect = self.image.get_rect()  # 获取图像的外接矩形，rect对象的属性是center、centerx、centery;与屏幕边缘对齐的话使用top、bottom、left、right
        self.screen_rect = screen.get_rect()  # 将矩形存储在此变量中
        self.rect.centerx = self.screen_rect.centerx  # 将飞船初始值设置在中间
        self.rect.bottom = self.screen_rect.bottom  # 将飞船设置在屏幕底部
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):  # 飞船居中
        self.center = self.screen_rect.centerx

    def blitme(self):  # 根据self.rect指定的位置将图像绘制在屏幕上
        self.screen.blit(self.image, self.rect)
