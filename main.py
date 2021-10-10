import sys
import random
import pygame
from copy import deepcopy

####################
#10.10.2021
#не до конца пока разобрался с алгоритмом генерации карт и движения кругов
#нужно каждый новый элемент класса враг закидывать в поток, фризоф не будет
#нужно согратить уровни или поставить подсказки а то я заебался это проходить
#нужно создать главное меню, выбор уровней, включение и выключение звука
#нужно сдлеать кнопку выхода
#можно попробовать уменьшить бокс коллайдер у спрайта стены, чтобы чел мог немного внутрь входить, будет приятнее играть
####################



pygame.init()
pygame.display.set_caption('DOTA 2')
screen = pygame.display.set_mode((800, 600))
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
width, height = screen.get_size()
running = True


def the_end(): #ага хорошо понятно круто
    pygame.quit()
    sys.exit()


def zastav(image): #добавить на заставку меню, нет смысла просто в заставке ибо загружается уровень мнгновенно
    screen.fill((0, 0, 0))
    image = load_image(image)#обработчик ошибки
    fon = pygame.transform.scale(image, screen.get_size())
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                the_end()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:#обработчик ошибки
        level_map = [line.strip('\n').split() for line in mapFile]
    return level_map


def load_enemies(filename):
    filename = "data/" + filename
    with open(filename, 'r') as enemyfile: #обработчик ошибки
        enemy_map = [line.strip('\n').split() for line in enemyfile]
    return enemy_map


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(f'data\{name}')
    except FileNotFoundError: # не ну в целом тут есть один обработчик ошибок)
        print(f'Файл с именем {name} не найден(')
        sys.exit()
    image.set_colorkey((255, 255, 255))
    return image


tile_images = {         #обработчик ошибки?
    'wall': load_image('wall_hungry.png'),
    'enemy': load_image('omegatvar1.png'),
    'sfere': load_image('sfera.png'),
    'portal': load_image('portal1.png'),
}
player_image = load_image('main9.png') #обработчик ошибки

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
sfere_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, position):
        super().__init__(wall_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (20, 220))
        self.rect = self.image.get_rect()
        if position > 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect[2] = 220
            self.rect[3] = 20
        if position % 2 == 1:
            self.rect[0] = 200 * (pos_x - 1) + 180
            self.rect[1] = 200 * (pos_y - 1) + 180
        if position == 0:
            self.rect[0] = 200 * (pos_x) + 180
            self.rect[1] = 200 * (pos_y - 1) + 180
        if position == 2:
            self.rect[0] = 200 * (pos_x - 1) + 180
            self.rect[1] = 200 * (pos_y) + 180


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, marsh):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (148, 148))
        self.rect = self.image.get_rect().move(
            200 * pos_x + 21, 200 * pos_y + 21)
        self.bob = 1
        self.b = 0
        self.moves = 0
        self.marsh = marsh

    def move(self, move):
        self.image = pygame.transform.rotate(self.image, 90)
        if move == '1':         #заменить на словарь по желанию
            self.rect[1] += -20
        elif move == '2':
            self.rect[1] += 20
        elif move == '3':
            self.rect[0] += -20
        else:
            self.rect[0] += 20

    def update(self):
        self.move(self.marsh[self.b % len(self.marsh)])
        self.moves = (self.moves + 1) % 10
        if not self.moves:
            self.b += 1 #на float 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (158, 158))
        self.rect = self.image.get_rect().move(
            200 * pos_x + 21, 200 * pos_y + 21)
        self.image = pygame.transform.rotate(self.image, 180)
        self.bob = 9
        self.with_sfer = False
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False
        self.bre = 1
        self.rotate = 0
        self.closed = False
        self.movesp = 20

    def move(self):
        bib = deepcopy(self.rect)  #заменить ифы на словарь
        if self.moveup:
            self.rect[1] += -self.movesp
        elif self.movedown:
            self.rect[1] += self.movesp
        elif self.moveleft:
            self.rect[0] += -self.movesp
        elif self.moveright:
            self.rect[0] += self.movesp #вот до сюда
        if pygame.sprite.spritecollideany(self, wall_group):
            self.rect = deepcopy(bib)
        if pygame.sprite.spritecollideany(self, sfere_group) and not self.with_sfer:
            self.with_sfer = True
        if pygame.sprite.spritecollideany(self, portal_group) and self.with_sfer:
            return True
        self.bob = (self.bob + 1) % 12
        if self.bob == 0:
            self.bob += 1
        self.image = pygame.transform.scale(load_image(f'main{self.bob}.png'), self.image.get_size())
        self.image = pygame.transform.rotate(self.image, 180)
        self.rotate = 180
        if self.moveup:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rotate = 0
        elif self.moveleft:
            self.image = pygame.transform.rotate(self.image, 270)
            self.rotate = 90
        elif self.moveright:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rotate = 270

    def breathe(self):
        if (self.bob > 7 or self.bob == 1) and self.closed:
            self.image = pygame.transform.scale(load_image(f'main{self.bob}close.png'), self.image.get_size())
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.closed = True
        else:
            self.image = pygame.transform.scale(load_image(f'main{self.bob}.png'), self.image.get_size())
            self.image = pygame.transform.rotate(self.image, self.rotate)


def generate_level(level, n):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            for k in range(4):
                if level[y][x][k] == '1':
                    Tile('wall', x, y, k)
    if n == 1:
        player = Player(11, 13)
        sfere = Sfere('sfere', 15, 2)
        portal = Portal('portal', 14, 13)
    elif n == 2:
        player = Player(20, 3)
        sfere = Sfere('sfere', 5, 21)
        portal = Portal('portal', 7, 4)
    elif n == 3:
        player = Player(0, 9)
        sfere = Sfere('sfere', 14, 6)
        portal = Portal('portal', 0, 7)
    return player, x, y, sfere, portal


class Sfere(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sfere_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (158, 158))
        self.rect = self.image.get_rect().move(
            200 * pos_x + 21, 200 * pos_y + 21)


class Portal(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(portal_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (158, 158))
        self.rect = self.image.get_rect().move(
            200 * pos_x + 21, 200 * pos_y + 21)
        self.bob = 0

    def update(self):
        self.bob = (self.bob + 1) % 9
        if self.bob == 0:
            self.bob += 1
        self.image = pygame.transform.scale(load_image(f'portal{self.bob}.png'), self.image.get_size())


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect[0] += self.dx
        obj.rect[1] += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Button(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, size):
        super().__init__(button_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], size)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


def win():
    Button('win', 0, 0, (1200, 1200))
    button_group.draw(screen)


def start(level):
    sound1.play()
    sound2.stop()

    return generate_level(load_level(f'map{level}.txt'), level)


fps = 1000
level = 2
sound1 = pygame.mixer.Sound('data\msic.mp3')  #можно попробовать подгружать и удалять, будет меньше памяти занимать
sound2 = pygame.mixer.Sound('data\death.mp3')
sound3 = pygame.mixer.Sound('data\start.mp3')
sound2.set_volume(0.0) #сорян, постоянно запускаю и уже заколебало
sound1.set_volume(0.0)
sound3.set_volume(0.0)
clock = pygame.time.Clock()
camera = Camera()
but = pygame.key.get_pressed()
for i in load_enemies(f'hell_enemy{level}.txt'):
    x, y, map = i
    Enemy('enemy', int(x), int(y), map)
sound3.play()
zastav('fon.jpg')
sound3.stop()
player, level_x, level_y, sfere, portal = start(level)
dd = 0
while True: #добавить кнопку, заменить на ожидание нажатия на кнопку
    screen.fill((255, 100, 100))
    camera.update(player);
    for sprite in all_sprites:
        camera.apply(sprite)
    if player.with_sfer:
        sfere.rect = player.rect[:]
        sfere.image = pygame.transform.scale(sfere.image, (48, 48))
    all_sprites.draw(screen)
    portal_group.update()
    screen.blit(load_image(f'lvl{level}.png'), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_end()
            #print(123)
        if event.type == pygame.KEYDOWN: #заменить на список
            if event.key == pygame.K_UP:
                player.moveup = True
            elif event.key == pygame.K_DOWN:
                player.movedown = True
            elif event.key == pygame.K_LEFT:
                player.moveleft = True
            elif event.key == pygame.K_RIGHT:
                player.moveright = True
        if event.type == pygame.KEYUP:  #заменить на список
            if event.key == pygame.K_UP:
                player.moveup = False
            elif event.key == pygame.K_DOWN:
                player.movedown = False
            elif event.key == pygame.K_LEFT:
                player.moveleft = False
            elif event.key == pygame.K_RIGHT:
                player.moveright = False
    if True in (player.moveup, player.movedown, player.moveleft, player.moveright): #после замены на список достаточно будет сдесь только 1 переменной
        if player.move():
            level += 1
            sound1.stop()
            all_sprites = pygame.sprite.Group()
            wall_group = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            sfere_group = pygame.sprite.Group()
            portal_group = pygame.sprite.Group()
            button_group = pygame.sprite.Group()
            for i in load_enemies(f'hell_enemy{level}.txt'): #обработчик ошибки
                x, y, map = i
                Enemy('enemy', int(x), int(y), map)
            player, level_x, level_y, sfere, portal = start(level)
            dd = 0
    else:#хахахахахах бля это сука ахаахахахаххах это надо оставить, вххвхвхвхвх (но можно вынести в поток)
        if player.closed and dd < 10:
            dd += 1
        else:
            player.closed = False
            player.breathe()
        k = random.randrange(25)
        if k == 5 and not player.closed:
            player.closed = True
            dd = 0
        player.breathe()
    '''
    if pygame.sprite.spritecollideany(player, enemy_group):
        sound2.play()
        sound1.stop()
        zastav('retry.jpg')
        all_sprites = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        sfere_group = pygame.sprite.Group()
        portal_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()
        for i in load_enemies(f'hell_enemy{level}.txt'):
            x, y, map = i
            Enemy('enemy', int(x), int(y), map)
        player, level_x, level_y, sfere, portal = start(level)
        dd = 0
    '''
    enemy_group.update()
    clock.tick(fps)
    pygame.display.flip()
