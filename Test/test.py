import pygame
import threading
import time
import sys

pygame.init()

UPDATES_PER_SEC = 30

SIZE = WIDTH, HEIGHT = 800, 600

SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("FarmGame")


def call_loop():
	global loopit, loopit_alive
	while loopit_alive:
		loopit = True
		time.sleep(1 / UPDATES_PER_SEC)


def load_image(image_name):
	image = pygame.image.load(image_name)
	image = pygame.transform.scale(image, (85, 137))
	rectangle = image.get_rect()
	return image, rectangle


class Walker:
	MOVE_SPEED = 30 / UPDATES_PER_SEC

	def update_frame(self):
		self.in_frame_counter += 1
		if self.in_frame_counter >= self.frame_limit:
			self.frame_cont = (self.frame_cont + 1) % len(self.frames)
			self.image, self.rectangle = load_image(self.frames[self.frame_cont])
			self.in_frame_counter = 0

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
		self.idle_frame_name = "../Assets/stick0.jpg"
		self.frame_cont = 0
		self.in_frame_counter = 0
		self.frame_limit = 7
		self.frames = ["../Assets/stick1.jpg", "../Assets/stick2.jpg", "../Assets/stick3.jpg", "../Assets/stick2.jpg"]
		self.image, self.rectangle = load_image(self.frames[self.frame_cont])


if __name__ in "__main__":
	loopit = True
	loopit_alive = True
	loopit_thread = threading.Thread(target=call_loop, args=[], daemon=True)
	loopit_thread.start()
	my_walker = Walker()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				my_walker.dest_x, my_walker.dest_y = [int(c) for c in pygame.mouse.get_pos()]
				my_walker.dest_x = my_walker.dest_x - int(87 // 2)
				my_walker.dest_y = my_walker.dest_y - int(125 // 2)
		if loopit:
			print("loop")
			SCREEN.fill((0, 0, 0))
			my_walker.move_towards_dest()
			my_walker.draw()
			my_walker.update_frame()
			pygame.display.flip()
			loopit = False
