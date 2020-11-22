import pygame, easygui
pygame.init()
screen = pygame.display.set_mode([1200, 600])
running = True
block = []
box = []
flag_texture = pygame.image.load("texture/flag.png")
flag_texture.set_colorkey([255, 255, 255])
flag = [-120, -120]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, 1200, 60):
                for j in range(0, 600, 60):
                    if event.pos[0] > i and event.pos[0] < i+60:
                        if event.pos[1] > j and event.pos[1] < j+60:
                            if event.button == 1:
                                if [i, j] in block:
                                    block.remove([i, j])
                                else:
                                    block.append([i, j])
                                if [i, j] in box:
                                    box.remove([i, j])
                                if [i, j] == flag:
                                    flag = [-120, -120]
                            if event.button == 3:
                                if [i, j] in box:
                                    box.remove([i, j])
                                else:
                                    box.append([i, j])
                                if [i, j] in block:
                                    block.remove([i, j])
                            if event.button == 2:
                                if [i, j] in block:
                                    block.remove([i, j])
                                if flag == [i, j]:
                                    flag = [-120, -120]
                                else:
                                    flag = [i, j]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                name = easygui.enterbox("Введите название карты")
                if name != None and name != "":
                    text = []
                    for i in block:
                        text.append(str(i[0])+":"+str(i[1]))
                    text = " ".join(text)
                    two = []
                    for i in box:
                        two.append(str(i[0])+":"+str(i[1]))
                    two = " ".join(two)
                    text = text+"\n"+two+"\n"+str(flag[0])+":"+str(flag[1])
                    file = open("texture/maps/"+name+".map", "w")
                    file.write(text)
                    file.close()
    screen.fill([255, 255, 255])
    for i in block:
        pygame.draw.rect(screen, [100, 100, 100], [i[0], i[1], 60, 60], 0)
    for i in box:
        pygame.draw.rect(screen, [150, 50, 0], [i[0], i[1], 60, 60], 0)
    for i in range(60, 1200, 60):
        pygame.draw.rect(screen, [0, 0, 0], [i-1, 0, 2, 600], 0)
    for i in range(60, 600, 60):
        pygame.draw.rect(screen, [0, 0, 0], [0, i-1, 1200, 2], 0)
    screen.blit(flag_texture, [flag[0], flag[1]])
    pygame.display.flip()
pygame.quit()
