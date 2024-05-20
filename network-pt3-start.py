import pygame
import socket
from math import hypot

USERNAME = "username"
MY_COLOR = pygame.Color(0, 255, 0)

sock = socket.create_connection(("127.0.0.1", 12345))
sock.settimeout(0.01)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Client")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 18)

x = 0
y = 0

others = {}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    speed = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    sock.send(f"{x},{y},{int(MY_COLOR)},{USERNAME};".encode())

    try:
        data = sock.recv(4096)
    except socket.timeout:
        pass
    else:
        messages = data.decode().split(";")
        for message in messages:
            if message.startswith("quit"):
                name = message.split(",")[1]
                del others[name]
                continue
            coords = message.split(",")
            try:
                other_x = float(coords[0])
                other_y = float(coords[1])
                other_color = pygame.Color(int(coords[2]))
                other_name = coords[3]
            except (IndexError, ValueError):
                pass
            else:
                others[other_name] = (other_x, other_y, other_color)

    for other_name, (other_x, other_y, other_color) in others.items():
        pygame.draw.rect(screen, other_color, (other_x, other_y, 50, 50))
        name_surface = font.render(other_name, True, (255, 255, 255))
        screen.blit(name_surface, (other_x, other_y - 30))

        if hypot(other_x - x, other_y - y) < 50:
            x -= (other_x - x) / 10
            y -= (other_y - y) / 10

    pygame.draw.rect(screen, MY_COLOR, (x, y, 50, 50))

    pygame.display.update()
    clock.tick(60)

sock.send(f"quit,{USERNAME};".encode())
pygame.quit()
