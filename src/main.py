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


if __name__ in "__main__":
	loopit = True
	loopit_alive = True
	loopit_thread = threading.Thread(target=call_loop, args=[], daemon=True)
	loopit_thread.start()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
