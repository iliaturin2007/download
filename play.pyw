import pygame, os, easygui
pygame.init()
screen = pygame.display.set_mode([600, 600])
running = True
play = pygame.image.load("texture/buttons/play.png")
maps = pygame.image.load("texture/buttons/maps.png")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 200 and event.pos[0] < 400:
                if event.pos[1] > 150 and event.pos[1] < 250:
                    os.system("start tank.pyw")
                if event.pos[1] > 350 and event.pos[1] < 450:
                    os.system("start maps.pyw")
            #if event.pos[0] > 275 and event.pos[0] < 275+50 and event.pos[1] > 500 and event.pos[1] < 550:
                #os.system("start setting.pyw")
    pygame.draw.rect(screen, [255, 255, 255], [0, 0, 600, 600], 0)
    screen.blit(play, [200, 150])
    screen.blit(maps, [200, 350])
    pygame.draw.rect(screen, [0, 0, 0], [275, 500, 50, 50], 0)
    pygame.display.flip()
pygame.quit()
