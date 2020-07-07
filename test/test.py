#!/usr/bin/python3

import pygame
import sys

pygame.init()
print("\r\r")

UPDATES_PER_SEC = 30
BLOCK_SIZE = 40

SIZE = WIDTH, HEIGHT = 1280, 768

SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("FarmGame")


def load_image(image_name):
	image = pygame.image.load(image_name)
	image = pygame.transform.scale(image, (85, 137))
	rectangle = image.get_rect()
	return image, rectangle


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
	def __init__(self, top_left, top_right, bottom_left, bottom_right):
		self.top_left = top_left
		self.top_right = top_right
		self.bottom_left = bottom_left
		self.bottom_right = bottom_right
		self.color = (100, 100, 255)

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
				return (oy - self.bottom_left[1]) >= (ox - self.bottom_left[0]) * -0.4
		elif ox < self.bottom_right[0]:
			if oy >= self.bottom_left[1] and oy >= self.top_right[1]:
				return True
			elif oy < self.bottom_left[1]:
				return (oy - self.bottom_left[1]) >= (ox - self.bottom_left[0]) * -0.4
			else:
				return (oy - self.top_right[1]) < (ox - self.top_left[0]) * -0.4
		else:
			if oy >= self.top_right[1]:
				return (oy - self.top_right[1]) < (ox - self.top_left[0]) * -0.4
			else:
				return (oy - self.bottom_right[1]) >= (ox - self.bottom_right[0]) * 0.666


if __name__ in "__main__":
	my_walker = Walker()
	my_tile = Tile((500, 50), (500 + 5 * BLOCK_SIZE, 50 + 2 * BLOCK_SIZE), (500 - 3 * BLOCK_SIZE, 50 + 2 * BLOCK_SIZE),
	               (500 + 2 * BLOCK_SIZE, 50 + 4 * BLOCK_SIZE))
	tiles = [my_tile]
	clock = pygame.time.Clock()
	while True:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				my_walker.dest_x, my_walker.dest_y = [int(c) for c in pygame.mouse.get_pos()]
				my_walker.dest_x = my_walker.dest_x - int(87 // 2)
				my_walker.dest_y = my_walker.dest_y - int(125 // 2)
		SCREEN.fill((0, 0, 0))
		my_walker.move_towards_dest()
		my_walker.draw()
		my_walker.update_frame()
		my_tile.draw()
		if my_tile.collides([int(c) for c in pygame.mouse.get_pos()]):
			print("\rCollides")
		else:
			print("\rDoesnt")
		pygame.display.flip()
