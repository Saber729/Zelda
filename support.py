from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map=[]
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')#读csv，分隔符号“，”
		for row in layout:#按行读取
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:#读取每一个图片文件
			full_path=path + '/' + image
			image_surf=pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list
