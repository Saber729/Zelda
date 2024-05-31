import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		pygame.init()
		self.screen=pygame.display.set_mode((WIDTH,HEIGTH))#设置屏幕长宽高
		pygame.display.set_caption('Zelda')#游戏标题
		self.clock=pygame.time.Clock()

		self.level=Level()

		# sound
		main_sound=pygame.mixer.Sound('../audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops=-1)
	
	def run(self):
		while True:
			for event in pygame.event.get():#监测游戏退出
				if event.type==pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)#填充背景颜色为黑色
			self.level.run()
			pygame.display.update()#更新画面
			self.clock.tick(FPS)#控制频率

if __name__=='__main__':
	game = Game()
	game.run()