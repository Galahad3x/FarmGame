#!/usr/bin/python3

import pygame
import sys

pygame.init()

UPDATES_PER_SEC = 30

SIZE = WIDTH, HEIGHT = 800, 600

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


if __name__ in "__main__":
	my_walker = Walker()
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
		pygame.draw.aaline(SCREEN, (100, 100, 255), (400, -100), (-100, 800), 101)
		pygame.display.flip()
