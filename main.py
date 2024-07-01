import pygame
from random import randint


pygame.init()
screen = pygame.display.set_mode((800, 800))
balance = 0
islandCost = 100
font = pygame.font.SysFont("Arial Rounded MT Bold", 35)

def getIsland(x, y):
    for island in islandGroup:
        if island.id == (x, y):
            return island

    return None #Get Islands

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Textures/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (400, 400))
        self.facingRight = False
        
    def update(self, vector):
        if vector < 0 and self.facingRight == True:
            self.flip()
            self.facingRight = False
        elif vector > 0 and self.facingRight == False:
            self.flip()
            self.facingRight = True

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False) #Player

class island(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocity = 3
        self.id = (x, y)
        self.visible = False
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.rockPos = []
        self.buying = False

    def update(self, x, y):
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity

    def show(self, balance, cost):
        if balance >= cost and not(self.visible):
            balance -= cost
            self.visible = True
            self.image = pygame.image.load("Textures/floor.png").convert_alpha()
            return balance, True

        return balance, False

    def genRock(self):
        if self.visible:
            if not(randint(0, 50)):
                position = randint(0, 9)
                position2 = randint(0, 8)
                tup = (position, position2)
                if not(tup in self.rockPos):
                    if randint(0, 1):
                        objector = Rock(self.rect.x + (20 * position) + 10, self.rect.y + (20 * position2) + 10, (self.id, tup))
                    else:
                        objector = Tree(self.rect.x + (20 * position) + 10, self.rect.y + (20 * position2) + 10, (self.id, tup))
                    self.rockPos.append(tup)
                    allObjects.add(objector)
                    mineableObjects.add(objector)

    def buyingPending(self):
        if not(self.visible):
            if not(self.buying):
                self.buying = True
                self.image.fill((255, 0, 0))
            else:
                self.buying = False
                self.image.fill(pygame.SRCALPHA)
        else:
            self.buying = False #Islands

    def removeObject(self, id):
        self.rockPos.remove(id) #Islands

class Material(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = ((0, 0, 0))
        self.health = 1
        self.velocity = 3
        self.cost = 0
        self.gotBar = False

    def setValues(self, color, health, x, y, cost, filePath, id):
        self.color = color
        self.health = health
        self.cost = cost
        self.id = id

        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))

    def update(self, x, y):
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity

    def hit(self, balance):
        if self.gotBar:
            self.healthBar.damage()
        else:
            self.healthBar = HealthBar(self.health, 25, 10, self.rect.x, self.rect.y)
            self.healthBar.damage()
            healthBarGroup.add(self.healthBar)
            allObjects.add(self.healthBar)
            self.gotBar = True

        self.health -= 1
        if self.health == 0:
            allObjects.remove(self.healthBar)
            healthBarGroup.remove(self.healthBar)
            del self.healthBar
            return balance + self.cost, self.id
        else:
            return balance, self.id #Material

class Rock(Material):  
    def __init__(self, x, y, id):
        super().__init__()
        super().setValues((50, 50, 50), 3, x, y, 5, "Textures/rock.png", id) #Rock

class Tree(Material):
    def __init__(self, x, y, id):
        super().__init__()
        super().setValues((0, 150, 0), 5, x, y, 10, "Textures/tree.png", id) #Tree

class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 3
        self.cost = 10
        self.visible = False

    def update(self, x, y):
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity #Bridge

    def show(self, balance):
        if balance >= self.cost and not(self.visible):
            balance -= self.cost
            self.visible = True
            self.image = pygame.image.load("Textures/bridgePiece.png").convert_alpha()
            return balance, True

        return balance, False #Bridge

class button(pygame.sprite.Sprite):
    def __init__(self, pos, icon, message, id, costPresent, cost=0):
        super().__init__()
        self.id = id
        self.image = pygame.Surface((250, 50))
        self.image.fill((255, 157, 92))
        self.rect = self.image.get_rect(topleft = pos)
        self.icon = pygame.image.load(icon).convert_alpha()
        self.main = message
        if costPresent:
            self.word = f"{message}: {cost}"
        else:
            self.word = message
        self.costPresent = costPresent
        self.message = font.render(self.word, False, (0, 0, 0))
        self.activate = False

    def update(self, cost=0):
        if self.costPresent:
            self.press()
            self.press()
            self.word = f"{self.main}: {cost}"
        
        self.message = font.render(self.word, False, (0, 0, 0))
        self.image.blit(self.icon, (0, 0))
        self.image.blit(self.message, (55, 12))

    def press(self):
        self.activate = not(self.activate)
        if self.activate:
            self.image.fill((164, 66, 1))
        else:
            self.image.fill((255, 157, 92)) #Button

class pickaxe(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Textures/pickaxe.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = False

    def update(self, playerFacingDirection):
        if playerFacingDirection and not(self.direction):
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center = (390, 400))
            self.direction = True
        elif not(playerFacingDirection) and self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center = (420, 400))
            self.direction = False #Pickaxe

class bank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (x, y))
        self.cost = 1000
        self.visible = False
        self.velocity = 3
        self.generate = -1
        self.startGenerating = False

    def show(self, balance):
        if balance >= self.cost and not(self.visible):
            balance -= self.cost
            self.visible = True
            self.generate = 0
            self.startGenerating = True
            self.image = pygame.image.load("Textures/bank.png").convert_alpha()
            return balance, True

        return balance, False

    def update(self, x, y):
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity

    def checkPrice(self, balance):
        if self.startGenerating:
            self.generate += 1
            if self.generate == 59:
                self.generate = 0
                return balance + 10

        return balance #Bank

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, initialHealth, length, width, x, y):
        super().__init__()
        self.health = initialHealth
        self.maxHealth = initialHealth
        self.length = length
        self.width = width
        self.image = pygame.Surface((length + 10, width + 10))
        self.image.fill((0, 0, 0))
        self.bar = pygame.Surface((length, width))
        self.bar.fill((255, 255, 255))
        self.rect = self.image.get_rect(center = (x, y))
        self.rect2 = self.bar.get_rect(topleft = (5, 5))
        self.velocity = 3
        
    def update(self, x, y):
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity
        
    def display(self):
        self.image.blit(self.bar, self.rect2)

    def damage(self):
        self.health -= 1
        self.image.fill((0, 0, 0))
        self.bar = pygame.Surface(((self.length * self.health) // self.maxHealth, self.width))
        self.bar.fill((255, 255, 255))
        return self.health < 0 #HealthBar

class Instructions(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = font.render("Welcome to my Game", False, (0, 0, 0))
        self.image2 = font.render("Use WASD to Move", False, (0, 0, 0))
        self.image3 = font.render("Click the Trees and Rocks to break them", False, (0, 0, 0))
        self.image4 = font.render("Collect as much money as you can", False, (0, 0, 0))
        self.rect = self.image.get_rect(midtop = (450, 25))
        self.rect2 = self.image.get_rect(midtop = (450, 50))
        self.rect3 = self.image.get_rect(midtop = (450, 75))
        self.rect4 = self.image.get_rect(midtop = (450, 100))
        self.count = 0

    def update(self):
        self.count += 1
        if self.count == 900:
            return True
        else:
            return False #Instructions

islandGroup = pygame.sprite.Group()
allObjects = pygame.sprite.Group()
mineableObjects = pygame.sprite.Group()
bridgeGroup = pygame.sprite.Group()
buttonGroup = pygame.sprite.Group()
bankGroup = pygame.sprite.Group()
visibleGroup = pygame.sprite.Group()
healthBarGroup = pygame.sprite.Group()

balanceSurface = font.render(str(balance), True, (160, 32, 240))
balanceRect = balanceSurface.get_rect(midleft = (100, 750))
coinSurface = pygame.image.load("Textures/coin.png").convert_alpha()
coinRect = coinSurface.get_rect(midright = (90, 750))

menuPress = button((25, 25), "Textures/settingIcon.png", "Shop", "setting", False)
bridgy = button((25, 100), "Textures/bridgeIcon.png", "Bridges: 10", "bridge", False)
islandys = button((25, 175), "Textures/floorIcon.png", "Island", "islands", True, 100)
banksy = button((25, 250), "Textures/bankIcon.png", "Bank: 1000", "bank", False)
buttonGroup.add(bridgy, islandys, banksy)

instructions = Instructions()
f = False

for row in range(-1, 4):
    for column in range(-1, 4):
        islandy = island((300 * row + 10), (300 * column) + 10)
        islandGroup.add(islandy)
        allObjects.add(islandy)
        if row == 1 and column == 1:
            islandy.show(100, 100)
            visibleGroup.add(islandy)

for row in range(-14, 56):
    for column in range(-14, 56):
        bridge = Bridge(20 * row, 20 * column)
        banks = bank(20 * row, 20 * column)
        if not(pygame.sprite.spritecollide(bridge, islandGroup, False)):
            bridgeGroup.add(bridge)
            allObjects.add(bridge)

        allObjects.add(banks)
        bankGroup.add(banks)

play = player()
players = pygame.sprite.GroupSingle(play)
pick = pygame.sprite.GroupSingle(pickaxe((420, 400)))

while True:
    screen.fill((200, 200, 255))
    balanceSurface = font.render(str(balance), True, (160, 32, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            isPressed = False
            if menuPress.rect.collidepoint(event.pos):
                menuPress.press()
                isPressed = True
            else:
                if menuPress.activate:
                    for buttons in buttonGroup:
                        if buttons.rect.collidepoint(event.pos):
                            buttons.press()
                            if buttons.id == "islands":
                                for islanduwu in islandGroup:
                                    islanduwu.buyingPending()
                            isPressed = True

            if islandys.activate and not(isPressed):
                for islands in islandGroup:
                    if islands.rect.collidepoint(event.pos):
                        balance, visible = islands.show(balance, islandCost)
                        isPressed = True
                        if visible:
                            visibleGroup.add(islands)
                            islandCost += 100

            for objects in mineableObjects:
                if objects.rect.collidepoint(event.pos):
                    balance, alphaId = objects.hit(balance)
                    isPressed = True
                
                if objects.health == 0:
                    islands = getIsland(*alphaId[0])
                    islands.removeObject(alphaId[1])
                    mineableObjects.remove(objects)
                    allObjects.remove(objects)
                    del objects

            if not(isPressed) and bridgy.activate:
                for bridge in bridgeGroup:
                    if bridge.rect.collidepoint(event.pos):
                        balance, visible = bridge.show(balance)
                        if visible:
                            visibleGroup.add(bridge)
                            isPressed = True

            if not(isPressed) and banksy.activate:
                for wank in bankGroup:
                    if wank.rect.collidepoint(event.pos) and pygame.sprite.spritecollide(wank, visibleGroup, False) and not(pygame.sprite.spritecollide(wank, mineableObjects, False)):
                        balance, visible = wank.show(balance)
                        if visible:
                            visibleGroup.add(wank)
                            isPressed = True

    keys = pygame.key.get_pressed()
    movementVector = 0

    if keys[pygame.K_w]:
        allObjects.update(0, 1)
        if not(pygame.sprite.groupcollide(players, visibleGroup, False, False)) or (pygame.sprite.groupcollide(players, mineableObjects, False, False)):
            allObjects.update(0, -1)

    if keys[pygame.K_s]:
        allObjects.update(0, -1)
        if not(pygame.sprite.groupcollide(players, visibleGroup, False, False)) or (pygame.sprite.groupcollide(players, mineableObjects, False, False)):
            allObjects.update(0, 1)

    if keys[pygame.K_d]:
        allObjects.update(-1, 0)
        if not(pygame.sprite.groupcollide(players, visibleGroup, False, False)) or (pygame.sprite.groupcollide(players, mineableObjects, False, False)):
            allObjects.update(1, 0)
        else:
            movementVector -= -1

    if keys[pygame.K_a]:
        allObjects.update(1, 0)
        if not(pygame.sprite.groupcollide(players, visibleGroup, False, False)) or (pygame.sprite.groupcollide(players, mineableObjects, False, False)):
            allObjects.update(-1, 0)
        else:
            movementVector -= 1

    for banks in bankGroup:
        balance = banks.checkPrice(balance)

    players.update(movementVector)
    if not(f):
        killQ = instructions.update()
        if killQ:
            del instructions
            f = True
        else:
            screen.blit(instructions.image, instructions.rect)
            screen.blit(instructions.image2, instructions.rect2)
            screen.blit(instructions.image3, instructions.rect3)
            screen.blit(instructions.image4, instructions.rect4)

    for healthBar in healthBarGroup:
        healthBar.display()
    buttonGroup.update(islandCost)
    menuPress.update()
    for islands in islandGroup:
        islands.genRock()
    pick.update(play.facingRight)
   
    bridgeGroup.draw(screen)
    allObjects.draw(screen)
    healthBarGroup.draw(screen)
    players.draw(screen)
    pick.draw(screen)
    screen.blit(menuPress.image, menuPress.rect)
    screen.blit(balanceSurface, balanceRect)
    screen.blit(coinSurface, coinRect)
    if menuPress.activate:
        buttonGroup.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)