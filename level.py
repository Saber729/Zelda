import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice,randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
	def __init__(self):

		self.display_surface=pygame.display.get_surface()
		self.game_paused=False

		self.visible_sprites=YSortCameraGroup()#可视精灵组
		self.obstacle_sprites=pygame.sprite.Group()#障碍物

		#
		self.current_attack=None
		self.attack_sprites=pygame.sprite.Group()
		self.attackable_sprites=pygame.sprite.Group()

		# 创建地图
		self.create_map()

		#UI
		self.ui=UI()
		self.upgrade=Upgrade(self.player)

		#particles
		self.animation_player=AnimationPlayer()
		self.magic_player=MagicPlayer(self.animation_player)

	# 计算坐标（x, y），并根据格子的值（'x'或'p'）创建相应的对象
	def create_map(self):
		layouts={
			'boundary':import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities':import_csv_layout('../map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('../graphics/Grass'),
			'objects': import_folder('../graphics/objects')
		}
		for style,layout in layouts.items():#读取字典
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col!='-1':
						x=col_index * TILESIZE
						y=row_index * TILESIZE
						if style=='boundary':#不可视，不会被draw，update，但是阻碍
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style=='grass':#随机画花草的样子
							random_grass_image=choice(graphics['grass'])
							Tile((x,y),
								 [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
								 'grass',
								 random_grass_image)

						if style=='object':#根据编号选不同的object
							surf=graphics['objects'][int(col)]#强制转换成数字
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						if style=='entities':
							if col=='394':
								self.player = Player(
							    (x,y),
							[self.visible_sprites],
									 self.obstacle_sprites,
									 self.creat_attack,
									 self.destroy_attack,
									 self.creat_magic)
							else:
								if col=='390':
									monster_name='bamboo'
								elif col=='391':
									monster_name='spirit'
								elif col=='392':
									monster_name='raccoon'
								else:
									monster_name='squid'
								Enemy(monster_name,
									  (x,y),
									  [self.visible_sprites,self.attackable_sprites],
									  self.obstacle_sprites,
									  self.damage_player,
									  self.trigger_death_particles,
									  self.add_exp)



		# 		if col=='x':
		# 			Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
		# 		if col=='p':#传入可视精灵组和障碍物
		# 			self.player=Player((x,y),[self.visible_sprites],self.obstacle_sprites)
		#将玩家生成在一个合适的位置，这样生成其他的草不会被挡住


	def creat_attack(self):#攻击时采用武器图片
		self.current_attack=Weapon(self.player,[self.visible_sprites,self.attack_sprites])

	def creat_magic(self,style,strength,cost):
		if style=='heal':
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

		if style=='flame':
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])


	def destroy_attack(self):#攻击完毕将武器图片删掉
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack=None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites=pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type=='grass':
							pos=target_sprite.rect.center
							offset=pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos-offset,[self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health-=amount
			self.player.vulnerable=False
			self.player.hurt_time=pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	def trigger_death_particles(self,pos,particle_type):

		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	def add_exp(self,amount):

		self.player.exp+=amount

	def toggle_menu(self):

		self.game_paused=not self.game_paused

	def run(self):
		self.visible_sprites.custom_draw(self.player)#绘制所有可视化图片
		self.ui.display(self.player)

		if self.game_paused:
			self.upgrade.display()
			#display upgrade menu
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		super().__init__()
		self.display_surface=pygame.display.get_surface()
		self.half_width=self.display_surface.get_size()[0]//2
		self.half_height=self.display_surface.get_size()[1]//2
		self.offset=pygame.math.Vector2()

		#创建地面   不是一个精灵组，因为永远在最底层，不会进行y sort
		self.floor_surf=pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect=self.floor_surf.get_rect(topleft=(0,0))

	def custom_draw(self,player):

		#获得偏移量
		self.offset.x=player.rect.centerx-self.half_width
		self.offset.y=player.rect.centery-self.half_height

		#绘制地面
		floor_offset_pos=self.floor_rect.topleft-self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		#根据矩形中心点y坐标从小到大排列顺序，先画的在下面，后画的在上面
		#centry可以换成top
		for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
			offset_rect=sprite.rect.topleft-self.offset
			#将image画在surface上
			self.display_surface.blit(sprite.image,offset_rect)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type=='enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)