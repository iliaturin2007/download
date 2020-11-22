#Импорт модулей pygame-графический движок, time-модуль времени, os-модуль для работы с командной строкой, easygui-модуль для замены косоли графикой(он используется для выбора карты)
import pygame, time, os, easygui
pygame.init()
#Для настройки игры с помощью файла setting.inf
try:
    setting = open("texture/setting.inf")
    text = setting.readlines()
    setting.close()
    text = "".join(text)
    text = text.split("\n")
    setting = {}
    for i in text:
        i = i.split("=")
        setting[i[0]] = i[1]
except:
    pass
try:
    HP_KT = int(setting["HP_CT"])
except:
    HP_KT = 100
try:
    HP_T = int(setting["HP_T"])
except:
    HP_T = 100
try:
    REPEAT = int(setting["REPEAT"])
except:
    REPEAT = 180
try:
    DAMAGE = int(setting["DAMAGE"])
except:
    DAMAGE = 50
try:
    SPEED = int(setting["SPEED"])
except:
    SPEED = 5
try:
    PATRON_SPEED = int(setting["PATRON_SPEED"])
except:
    PATRON_SPEED = 20
hp_kt = HP_KT
hp_t = HP_T
#Загрузка и выбор карты
maps = os.listdir("texture/maps")
maps_no = []
for i in maps:
    if i.endswith(".map"):
        i = i.split(".")
        i.remove(i[-1])
        i = ".".join(i)
        maps_no.append(i)
maps = easygui.choicebox("Выберите карту", choices = maps_no)
if maps != None:
    file = open("texture/maps/"+maps+".map")
    text = file.readlines()
    file.close()
    try:
        one = text[0]
        one = one.split(" ")
        block = []
        for i in one:
            i = i.split(":")
            block.append([int(i[0]), int(i[1])])
    except:
        block = []
    try:
        two = text[1]
        two = two.split(" ")
        box = []
        for i1 in two:
            i1 = i1.split(":")
            box.append([int(i1[0]), int(i1[1])])
    except:
        box = []
    flag = [-120, -120]
    try:
        three = text[2].split(":")
        flag[0] = int(three[0])
        flag[1] = int(three[1])
    except:
        pass
#Экран
screen = pygame.display.set_mode([1200, 650])
#Переменнная определяющая включён ли полноэкранный режим
screen_full = -1
#Переменнная для остановки цикла программы
running = True
#Загрузка текстур
tank_kt_img = pygame.image.load("texture/tank_kt.png")
tank_t_img = pygame.image.load("texture/tank_t.png")
flag_img = pygame.image.load("texture/flag.png")
patron_img = pygame.image.load("texture/patron.png")
wood = pygame.image.load("texture/wood.jpg")
stone = pygame.image.load("texture/stone.jpg")
#Убираем белый цвет с картинок
tank_kt_img.set_colorkey([255, 255, 255])
tank_t_img.set_colorkey([255, 255, 255])
flag_img.set_colorkey([255, 255, 255])
#Переменные поворота танка
rotate = 0
rotate_t = 0
#Переменные движения и местоположения танков
move_x_t = 0
move_y_t = 0
pos_x_t = 0
pos_y_t = 0
move_x_kt = 0
move_y_kt = 0
pos_x_kt = 1140
pos_y_kt = 540
#Создаём объект для контроля фпс в игре
clock = pygame.time.Clock()
#Массив для указания местоположения патронов
patron = []
#Переменные нужные для перезарядки
repeat_kt = 0
repeat_t = 0
shut=True
while running:
    shut = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Проверка нажали ли вы кнопку
        if event.type == pygame.KEYDOWN:
            #Полноэкранный режим
            if event.key == pygame.K_F11:
                if screen_full == 1:
                    screen = pygame.display.set_mode([1200, 650])
                if screen_full == -1:
                    screen = pygame.display.set_mode([1200, 650], pygame.FULLSCREEN)
                screen_full = -screen_full
            #Передвижение танка контр-террориста
            if event.key == pygame.K_DOWN:
                move_y_kt=SPEED
                move_x_kt = 0
                rotate = 180
            if event.key == pygame.K_UP:
                move_y_kt=-SPEED
                move_x_kt = 0
                rotate = 0
            if event.key == pygame.K_RIGHT:
                move_x_kt=SPEED
                move_y_kt = 0
                rotate = 270
            if event.key == pygame.K_LEFT:
                move_x_kt=-SPEED
                move_y_kt = 0
                rotate = 90
            #Передвижение танка террориста
            if event.key == pygame.K_s:
                move_y_t=SPEED
                move_x_t = 0
                rotate_t = 180
            if event.key == pygame.K_w:
                move_y_t=-SPEED
                move_x_t = 0
                rotate_t = 0
            if event.key == pygame.K_d:
                move_x_t=SPEED
                move_y_t = 0
                rotate_t = 270
            if event.key == pygame.K_a:
                move_x_t=-SPEED
                move_y_t = 0
                rotate_t = 90
            #Стрельба контр-террориста
            if event.key == pygame.K_RCTRL and repeat_kt <= 0:
                if rotate == 0:
                    patron.append([pos_x_kt+20, pos_y_kt+20, rotate])
                if rotate == 90:
                    patron.append([pos_x_kt-20, pos_y_kt+20, rotate])
                if rotate == 180:
                    patron.append([pos_x_kt+20, pos_y_kt+80, rotate])
                if rotate == 270:
                    patron.append([pos_x_kt+80, pos_y_kt+20, rotate])
                repeat_kt = REPEAT
            #Стрельба террориста
            elif event.key == pygame.K_LSHIFT and repeat_t <= 0:
                if rotate_t == 0:
                    patron.append([pos_x_t+20, pos_y_t+20, rotate_t])
                if rotate_t == 90:
                    patron.append([pos_x_t-20, pos_y_t+20, rotate_t])
                if rotate_t == 180:
                    patron.append([pos_x_t+20, pos_y_t+80, rotate_t])
                if rotate_t == 270:
                    patron.append([pos_x_t+80, pos_y_t+20, rotate_t])
                repeat_t = REPEAT
        #Проверка отпустили ли вы кнопку
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                move_y_kt=0
            if event.key == pygame.K_DOWN:
                move_y_kt=0
            if event.key == pygame.K_RIGHT:
                move_x_kt=0
            if event.key == pygame.K_LEFT:
                move_x_kt=0
            if event.key == pygame.K_s:
                move_y_t=0
            if event.key == pygame.K_w:
                move_y_t=0
            if event.key == pygame.K_d:
                move_x_t=0
            if event.key == pygame.K_a:
                move_x_t=0
            if event.key == pygame.K_LSHIFT:
                shut = False
    #Перемещение танка
    pos_x_kt+=move_x_kt
    pos_y_kt+=move_y_kt
    pos_x_t+=move_x_t
    pos_y_t+=move_y_t
    stop = []
    #Отчистка экрана и отрисовка флага
    pygame.draw.rect(screen, [255, 255, 255], [0, 0, 1200, 600], 0)
    screen.blit(flag_img, flag)
    #Блоки и коробки
    for i in box:
        screen.blit(wood, i)
        stop.append(i)
        for each in patron:
            if each[0] > i[0]-20 and each[0] < i[0]+80 and each[1] > i[1]-20 and each[1] < i[1]+80:
                patron.remove(each)
                box.remove(i)
    for i in block:
        screen.blit(stone, i)
        stop.append(i)
        for each in patron:
            if each[0] > i[0] and each[0] < i[0]+60 and each[1] > i[1] and each[1] < i[1]+60:
                patron.remove(each)
    #Остановка танка
    for i in stop:
        if pos_x_kt > i[0]-60 and pos_x_kt < i[0]-20:
            if pos_y_kt > i[1]-40 and pos_y_kt < i[1]+40:
                pos_x_kt = i[0]-60
        if pos_y_kt > i[1]-60 and pos_y_kt < i[1]-20:
            if pos_x_kt > i[0]-40 and pos_x_kt < i[0]+40:
                pos_y_kt = i[1]-60
        if pos_x_kt < i[0]+60 and pos_x_kt > i[0]+20:
            if pos_y_kt > i[1]-40 and pos_y_kt < i[1]+40:
                pos_x_kt = i[0]+60
        if pos_y_kt < i[1]+60 and pos_y_kt > i[1]+20:
            if pos_x_kt > i[0]-40 and pos_x_kt < i[0]+40:
                pos_y_kt = i[1]+60
        if pos_x_t > i[0]-60 and pos_x_t < i[0]-20:
            if pos_y_t > i[1]-40 and pos_y_t < i[1]+40:
                pos_x_t = i[0]-60
        if pos_y_t > i[1]-60 and pos_y_t < i[1]-20:
            if pos_x_t > i[0]-40 and pos_x_t < i[0]+40:
                pos_y_t = i[1]-60
        if pos_x_t < i[0]+60 and pos_x_t > i[0]+20:
            if pos_y_t > i[1]-40 and pos_y_t < i[1]+40:
                pos_x_t = i[0]+60
        if pos_y_t < i[1]+60 and pos_y_t > i[1]+20:
            if pos_x_t > i[0]-40 and pos_x_t < i[0]+40:
                pos_y_t = i[1]+60
    #Границы экрана и перезарядка
    if repeat_kt > 0:
        repeat_kt -= 1
    if pos_x_kt < 0:
        pos_x_kt = 0
    if pos_x_kt > 1200-60:
        pos_x_kt = 1200-60
    if pos_y_kt < 0:
        pos_y_kt = 0
    if pos_y_kt > 600-60:
        pos_y_kt = 600-60
    if repeat_t > 0:
        repeat_t -= 1
    if pos_x_t < 0:
        pos_x_t = 0
    if pos_x_t > 1200-60:
        pos_x_t = 1200-60
    if pos_y_t < 0:
        pos_y_t = 0
    if pos_y_t > 600-60:
        pos_y_t = 600-60
    i=0
    #Патроны
    for each in patron:
        screen.blit(patron_img, [each[0], each[1]])
        if each[2] == 0:
            patron[i][1] -= PATRON_SPEED
        if each[2] == 90:
            patron[i][0] -= PATRON_SPEED
        if each[2] == 180:
            patron[i][1] += PATRON_SPEED
        if each[2] == 270:
            patron[i][0] += PATRON_SPEED
        if each[0] < 0 or each[0] > 1200 or each[1] > 600 or each[1] < 0:
            del patron[i]
        if each[0] > pos_x_kt and each[0] < pos_x_kt+60 and each[1] > pos_y_kt and each[1] < pos_y_kt+60:
            HP_KT -= DAMAGE
            patron.remove(each)
        if each[0] > pos_x_t and each[0] < pos_x_t+60 and each[1] > pos_y_t and each[1] < pos_y_t+60:
            HP_T -= DAMAGE
            patron.remove(each)
        if each[0] > flag[0] and each[1] > flag[1] and each[0] < flag[0]+60 and each[1] < flag[1]+60:
            HP_KT = 0
        i+=1
    #Отрисовка танка
    screen.blit(pygame.transform.rotate(tank_kt_img, rotate), [pos_x_kt, pos_y_kt])
    screen.blit(pygame.transform.rotate(tank_t_img, rotate_t), [pos_x_t, pos_y_t])
    pygame.draw.rect(screen, [150, 150, 150], [0, 600, 1200, 50], 0)
    #Проверка жизней и экран победы
    if HP_T > 0:
        pygame.draw.rect(screen, [200, 200, 100], [150, 615, int(300*HP_T/hp_t), 20], 0)
    else:
        screen.fill([255, 255, 255])
        font = pygame.font.Font(None, 60)
        text = font.render("Контртеррористы победили", 1, (0, 0, 255))
        screen.blit(text, text.get_rect(center=(600, 200)))
        pygame.display.flip()
        time.sleep(3)
        running = False
        pygame.quit()
    if HP_KT > 0:
        pygame.draw.rect(screen, [0, 0, 255], [1050, 615, 0-int(300*HP_KT/hp_kt), 20], 0)
    else:
        screen.fill([255, 255, 255])
        font = pygame.font.Font(None, 60)
        text = font.render("Террористы победили", 1, (200, 200, 100))
        screen.blit(text, text.get_rect(center=(600, 200)))
        pygame.display.flip()
        time.sleep(3)
        running = False
    #Отрисовка перезарядки
    if repeat_t > 0:
        pygame.draw.rect(screen, [50, 50, 0], [25, 615, 100, 20], 2)
        pygame.draw.rect(screen, [50, 50, 0], [25, 615, 100-int(repeat_t*100/REPEAT)+1, 20], 0)
    if repeat_kt > 0:
        pygame.draw.rect(screen, [0, 0, 50], [1175, 615, -100, 20], 2)
        pygame.draw.rect(screen, [0, 0, 50], [1175, 615, int(repeat_kt*100/REPEAT)-100, 20], 0)
    #Контроль фпс
    clock.tick(60)
    #Обновление экрана
    if HP_KT > 0 and HP_T > 0:
        pygame.display.flip()
pygame.quit()
    
