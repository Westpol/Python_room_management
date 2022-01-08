import pygame
import json

accFile = open("accounts.json", encoding='UTF-8')
accounts = json.load(accFile)

loginSize = 30
triangleSize = 50   # length of each side
fps = 75
pos = 0
secondsPerTriangle = 3
typingUname = True
typingPasswd = False
overLogin = False
uname = ""
passwd = ""
asterics = True

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
clock = pygame.time.Clock()
text = pygame.freetype.Font("arial.ttf", 24)
loginText = pygame.freetype.Font("arial.ttf", 35)
loginButton = pygame.Rect(width / 2 - 48, height / 2 + 67, 96, 36)
unameButton = pygame.Rect(width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 100 - (40 - 34) / 2, 290, 30)
passwdButton = pygame.Rect(width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 150 - (40 - 34) / 2, 290, 30)


def validateUser(un, pwd):
    global uname, passwd, overLogin, typingPasswd, typingUname
    for goThrough in accounts["users"]:
        if goThrough["name"] == un:
            print("Logged In")
            exit()

    print("User not found")
    uname = ""
    passwd = ""
    overLogin = False
    typingPasswd = False
    typingUname = True


def writeData(passw, unamee):
    text.render_to(screen, ((width / 2 - (16 / 2 * loginSize) + 130) + 30, height / 2 - (9 / 2 * loginSize) + 100 + 3), unamee, (0, 0, 0))
    if asterics:
        text.render_to(screen, ((width / 2 - (16 / 2 * loginSize) + 130) + 30, height / 2 - (9 / 2 * loginSize) + 150 + 3), "*"*len(passw), (0, 0, 0))
    else:
        text.render_to(screen, ((width / 2 - (16 / 2 * loginSize) + 130) + 30, height / 2 - (9 / 2 * loginSize) + 150 + 3), passw, (0, 0, 0))


def detectInput(even):
    global uname, passwd
    unwantedKeys = even.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_TAB, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK, pygame.K_KP_ENTER, pygame.K_RETURN)
    if not unwantedKeys and typingUname:
        if ord(even.unicode) == 8:
            uname = uname[0:len(uname)-1]
        else:
            uname += even.unicode
    if not unwantedKeys and typingPasswd:
        if ord(even.unicode) == 8:
            passwd = passwd[0:len(passwd)-1]
        else:
            passwd += even.unicode


def updown(ud):
    global typingUname, typingPasswd, overLogin
    if ud == "down":
        if typingUname:
            typingUname = False
            typingPasswd = True
        elif typingPasswd:
            typingPasswd = False
            overLogin = True
        elif overLogin:
            overLogin = False
            typingUname = True
    elif ud == "up":
        if typingUname:
            typingUname = False
            overLogin = True
        elif typingPasswd:
            typingPasswd = False
            typingUname = True
        elif overLogin:
            overLogin = False
            typingPasswd = True
    else:
        raise NameError('input of updown is not "up" or "down"')


while 1:
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            detectInput(event)
            if event.key == pygame.K_ESCAPE:
                exit()

            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if typingUname:
                    updown("down")
                elif typingPasswd or overLogin:
                    validateUser(uname, passwd)

            if event.key == pygame.K_TAB and event.mod & pygame.KMOD_SHIFT:
                updown("up")
            elif event.key == pygame.K_TAB:
                updown("down")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if loginButton.collidepoint(mousePos):
                validateUser(uname, passwd)
                exit()
            elif unameButton.collidepoint(mousePos):
                typingUname = True
                typingPasswd = False
            elif passwdButton.collidepoint(mousePos):
                typingPasswd = True
                typingUname = False
            else:
                typingPasswd = False
                typingUname = False

    if pos / triangleSize >= 4:
        pos = 0
    pos += triangleSize * (clock.get_fps()/(fps**2)) / secondsPerTriangle
    for f in range(-5, int(height/triangleSize)+5):
        for i in range(0, int(width/triangleSize)+5):
            if i % 2 == 0 and f % 2 == 0 or i % 2 != 0 and f % 2 != 0:
                ts = triangleSize
                pygame.draw.polygon(screen, (0, 0, 255), [(ts * i, ts * f + pos), (ts * i + ts, ts * f + pos), (ts * i - (ts / 2) + ts, ts * f + ts + pos)], width=0)

    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - (16 / 2 * loginSize), height / 2 - (9 / 2 * loginSize), 16 * loginSize, 9 * loginSize))
    text.render_to(screen, (width-80, 40), str(int(clock.get_fps())), (0, 255, 0))

    loginText.render_to(screen, (width / 2 - (16 / 2 * loginSize)+20, height / 2 - (9 / 2 * loginSize) + 20), "Login", (0, 0, 0))
    text.render_to(screen, (width / 2 - (16 / 2 * loginSize) + 130 - text.get_rect("Username:")[2], height / 2 - (9 / 2 * loginSize) + 100), "Username:", (0, 0, 0))
    text.render_to(screen, (width / 2 - (16 / 2 * loginSize) + 130 - text.get_rect("Password:")[2], height / 2 - (9 / 2 * loginSize) + 150), "Password:", (0, 0, 0))

    pygame.draw.rect(screen, (120, 120, 120), (width / 2 - (16 / 2 * loginSize) + 150, height / 2 - (9 / 2 * loginSize) + 100 - (40 - 24) / 2, 300, 40), border_radius=3)
    if unameButton.collidepoint(mousePos) or typingUname:
        pygame.draw.rect(screen, (200, 200, 200), (width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 100 - (40 - 34) / 2, 290, 30), border_radius=3)
    else:
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 100 - (40 - 34) / 2, 290, 30), border_radius=3)
    pygame.draw.rect(screen, (120, 120, 120), (width / 2 - (16 / 2 * loginSize) + 150, height / 2 - (9 / 2 * loginSize) + 150 - (40 - 24) / 2, 300, 40), border_radius=3)
    if passwdButton.collidepoint(mousePos) or typingPasswd:
        pygame.draw.rect(screen, (200, 200, 200), (width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 150 - (40 - 34) / 2, 290, 30), border_radius=3)
    else:
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - (16 / 2 * loginSize) + 155, height / 2 - (9 / 2 * loginSize) + 150 - (40 - 34) / 2, 290, 30), border_radius=3)
    pygame.draw.rect(screen, (120, 120, 120), (width / 2 - 50, height / 2 + 65, 100, 40), border_radius=3)
    if loginButton.collidepoint(mousePos) or overLogin:
        pygame.draw.rect(screen, (200, 200, 200), (width / 2 - 48, height / 2 + 67, 96, 36), border_radius=3)
    else:
        pygame.draw.rect(screen, (255, 255, 255), (width / 2 - 48, height / 2 + 67, 96, 36), border_radius=3)
    text.render_to(screen, (width / 2 - text.get_rect("Login")[2]/2, height / 2 + 67 + text.get_rect("Login")[1]/2), "Login",  (0, 0, 0))

    writeData(passwd, uname)

    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(fps)
