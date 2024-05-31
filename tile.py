import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
#sprite type类型
#object中不一定是64*64的，还有128*128的，surface没传默认64*64，为了绘制隐形边界
	def __init__(self,pos,groups,sprite_type,surface=pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)# 调用父类的构造函数，将当前对象添加到指定的精灵组中
		self.sprite_type=sprite_type
		y_offset=HITBOX_OFFSET[sprite_type]
		self.image = surface # 加载瓦片的图片资源
		if sprite_type=='object':
			self.rect=self.image.get_rect(topleft=(pos[0],pos[1]-TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)# 设置瓦片的位置
		self.hitbox=self.rect.inflate(0,y_offset)