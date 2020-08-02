#!/usr/bin/python3

import pygame
import sys

pygame.init()
print("\r\r")

GRASS = 0
RIVER = 1
ROAD = 2

SPRITE_DICT = {
	GRASS: "../assets/gespa/1.png",
	RIVER: "../assets/riu/1_1.png",
	ROAD: "../assets/carretera/1.png"
}

UPDATES_PER_SEC = 30
BLOCK_SIZE = 40

SIZE = WIDTH, HEIGHT = 1280, 768

SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("FarmGame")


def load_image(image_name):
	image = pygame.image.load(image_name)
	image = pygame.transform.scale(image, (BLOCK_SIZE * 6 + 7, BLOCK_SIZE * 6 + 7))
	rectangle = image.get_rect()
	return image, rectangle


def find_image(type_of_tile):
	return load_image(SPRITE_DICT[type_of_tile])


class Walker:
	MOVE_SPEED = 30 / UPDATES_PER_SEC

	def update_frame(self):
		self.in_frame_counter += 1
		if self.x == self.dest_x and self.y == self.dest_y:
			self.image, self.rectangle = load_image(self.idle_frame_name)
		else:
			if self.in_frame_counter >= self.frame_limit:
				self.frame_cont = (self.frame_cont + 1) % len(self.frames)
				self.in_frame_counter = 0
			self.image, self.rectangle = load_image(self.frames[self.frame_cont])

	def draw(self):
		self.rectangle.x = int(self.x)
		self.rectangle.y = int(self.y)
		SCREEN.blit(self.image, self.rectangle)

	def move_towards_dest(self):
		if self.x < self.dest_x:
			if self.x < (self.dest_x - Walker.MOVE_SPEED):
				self.x += Walker.MOVE_SPEED
			else:
				self.x = self.dest_x
		elif self.x > self.dest_x:
			if self.x > (self.dest_x + Walker.MOVE_SPEED):
				self.x -= Walker.MOVE_SPEED
			else:
				self.x = self.dest_x
		if self.y < self.dest_y:
			if self.y < (self.dest_y - Walker.MOVE_SPEED):
				self.y += Walker.MOVE_SPEED
			else:
				self.y = self.dest_y
		elif self.y > self.dest_y:
			if self.y > (self.dest_y + Walker.MOVE_SPEED):
				self.y -= Walker.MOVE_SPEED
			else:
				self.y = self.dest_y

	def __init__(self):
		self.x, self.y = 0, 0
		self.dest_x, self.dest_y = 0, 0
		self.idle_frame_name = "../assets/stick0.jpg"
		self.frame_cont = 0
		self.in_frame_counter = 0
		self.frame_limit = 7
		self.frames = ["../assets/stick1.jpg", "../assets/stick2.jpg", "../assets/stick3.jpg", "../assets/stick2.jpg"]
		self.image, self.rectangle = load_image(self.frames[self.frame_cont])


class Tile:
	def __init__(self, top_left, type_of_tile):
		self.top_left = top_left
		self.top_right = top_left[0] + 3 * BLOCK_SIZE, top_left[1] + 2 * BLOCK_SIZE
		self.bottom_left = top_left[0] - 3 * BLOCK_SIZE, top_left[1] + 2 * BLOCK_SIZE
		self.bottom_right = top_left[0], top_left[1] + 4 * BLOCK_SIZE
		self.sprite_point = self.bottom_left[0], self.bottom_left[1] - BLOCK_SIZE * 4
		self.image, self.rectangle = find_image(type_of_tile)
		self.color = (100, 100, 255)

	def draw_sprite(self):
		self.rectangle.x = self.sprite_point[0]
		self.rectangle.y = self.sprite_point[1]
		SCREEN.blit(self.image, self.rectangle)

	def draw(self):
		pygame.draw.aaline(SCREEN, self.color, self.top_left, self.bottom_left, 100)
		pygame.draw.aaline(SCREEN, self.color, self.top_left, self.top_right, 100)
		pygame.draw.aaline(SCREEN, self.color, self.bottom_right, self.top_right, 100)
		pygame.draw.aaline(SCREEN, self.color, self.bottom_right, self.bottom_left, 100)

	def collides(self, other_coords):
		ox = other_coords[0]
		oy = other_coords[1]
		if ox < self.bottom_left[0] or ox >= self.top_right[0]:
			return False
		if oy >= self.bottom_right[1] or oy < self.top_left[1]:
			return False
		if ox < self.top_left[0]:
			if oy >= self.bottom_left[1]:
				return (oy - self.bottom_left[1]) < (ox - self.bottom_left[0]) * 0.666
			else:
				return (oy - self.bottom_left[1]) >= (ox - self.bottom_left[0]) * -0.666
		elif ox < self.bottom_right[0]:
			if oy >= self.bottom_left[1] and oy >= self.top_right[1]:
				return True
			elif oy < self.bottom_left[1]:
				return (oy - self.bottom_left[1]) < (ox - self.bottom_left[0]) * 0.666
			else:
				return (oy - self.top_right[1]) >= (ox - self.top_left[0]) * 0.666
		else:
			if oy >= self.top_right[1]:
				return (oy - self.top_right[1]) < (ox - self.top_right[0]) * -0.666
			else:
				return (oy - self.top_right[1]) >= (ox - self.top_right[0]) * 0.666


class AdvancedTile:
	def __init__(self, top_tile, bottom_tile):
		self.top_tile = top_tile
		self.bottom_tile = bottom_tile
		self.bottom_tile.image, self.bottom_tile.rectangle = load_image("../assets/carretera/1.png")

	def collides(self, other_coords):
		if self.bottom_tile.collides(other_coords) or self.top_tile.collides(other_coords):
			return True
		else:
			if self.top_tile.bottom_left[0] <= other_coords[0] < self.top_tile.top_right[0]:
				return self.top_tile.bottom_left[1] <= other_coords[1] < self.bottom_tile.bottom_left[1]
			return False

	def draw(self):
		self.top_tile.draw()
		self.bottom_tile.draw()

	def draw_sprite(self):
		self.bottom_tile.draw_sprite()


class Map:
	def __init__(self, map_table):
		self.map_table = map_table
		self.tile_table = self.update_table()

	def update_table(self):
		tile_tab = []
		for i, line in enumerate(self.map_table):
			tile_line = []
			if i % 2 == 0:
				x_offset = 3 * BLOCK_SIZE
			else:
				x_offset = 0
			for j, elem in enumerate(line):
				tile_line.append(Tile(((j * 6 * BLOCK_SIZE) + x_offset, i * 2 * BLOCK_SIZE), elem))
			tile_tab.append(tile_line)
		return tile_tab

	def draw_on_screen(self):
		SCREEN.fill((72, 255, 59))
		self.tile_table = self.update_table()
		for line in self.tile_table:
			for tile in line:
				tile.draw_sprite()


if __name__ in "__main__":
	clock = pygame.time.Clock()
	my_map = Map([[]])
	my_map.map_table = [[GRASS, GRASS, RIVER, RIVER, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, RIVER, RIVER, GRASS, GRASS, GRASS],
	                    [GRASS, RIVER, RIVER, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, RIVER, RIVER, GRASS, GRASS, GRASS, GRASS],
	                    [RIVER, RIVER, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [RIVER, RIVER, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [RIVER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [RIVER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [ROAD, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [ROAD, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, ROAD, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, ROAD, GRASS, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, ROAD, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, ROAD, GRASS, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, ROAD, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, ROAD, GRASS, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, GRASS, ROAD, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, GRASS, ROAD, GRASS, GRASS],
	                    [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS]]
	while True:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		my_map.draw_on_screen()
		pygame.display.flip()
