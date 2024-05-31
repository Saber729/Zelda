import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index=0
        self.animation_speed=0.15
        self.direction=pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:  # 返回欧几里得距离
            self.direction = self.direction.normalize()  # 使斜着走路和横竖走路都为1

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')  # 判断水平是否碰撞
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')  # 判断垂直是否碰撞
        self.rect.center = self.hitbox.center

    # self.rect.center+= self.direction * speed

    def collision(self, direction):  # 判断是否撞墙
        if direction == 'horizontal':  # 水平方向
            for sprite in self.obstacle_sprites:  # 比较player和所有障碍物
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # 向右移动，一定撞到障碍物左边
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # 向左移动
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # 向上移动
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # 向下移动
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0