import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('Image/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):  # 外星人检查碰撞
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.right <= 0:
            return True

    def update(self):  # 更新位置
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_diretion)
        self.rect.x = self.x

    def biltme(self):  # 根据self.rect指定的位置将图像绘制在屏幕上
        self.screen.blit(self.image, self.rect)
