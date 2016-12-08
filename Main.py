#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame # biblioteka pygame potrzebna do stworzenia gry
import random # biblioteka random potrzebna do losowej organizacji stones
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import pygame
import random
import sys
import math # klasa matematyczna
import sqlite3
import math
import sys
# import MySQLdb

import pygame

def LoadImage(image,scale,clip): # funkcja ktora laduje obrazy
    picture = pygame.image.load(image)  # zaladowanie obrazu  do zmiennej
    playerSurface = pygame.Surface((clip[2], clip[3])) # stworzenie nowej powierzchni
    playerSurface.blit(picture, (0, 0), clip)  # przyciecie obrazu i wyrysowanie go
    scaledPicture = (clip[2] * scale, clip[3] * scale) # lista potrzebna do tworzenia przeskalowanego obrazu
    scaledPicture = pygame.transform.scale(playerSurface, (clip[2] * scale, clip[3] * scale) ) # skalowanie obrazu

    return scaledPicture # zwrocenie przeskalowanego obrazu



class Bullet(): # klasa pocisku
    def __init__(self,x,y,angle):
        self.bul = pygame.image.load("images/pocisk.png")  # pobranie obrazu (funkcja napisana wlasnorecznie)
        self.bul = pygame.transform.scale(self.bul, (10, 10))
        self.bul = pygame.transform.rotate(self.bul,angle)
        self.image = self.bul  # obrazek
        self.rect = self.image.get_rect()  # pobranie wspolrzednych obrazu
        self.rect.x = x # wspolrzedne x i y pocisku
        self.rect.y = y
        self.dx = 20 # przesuniecie dx i dy pocisku
        self.dy = 20
        self.angle = angle # kąt obrotu przycisku równowazny z kątem obrotu statku


    def update(self): # metoda aktualizujaca pocisk
        if self.angle == 0:
            self.rect.y -= self.dy

        if self.angle == 90:
            self.rect.x -= self.dx

        if self.angle == 270:
            self.rect.x += self.dx

        if self.angle == 180:
            self.rect.y += self.dy

        if self.angle == 135:
            self.rect.x -= self.dx
            self.rect.y += self.dy

        if self.angle == 315:
            self.rect.x += self.dx
            self.rect.y -= self.dy

        if self.angle == 45:
            self.rect.x -= self.dx
            self.rect.y -= self.dy

        if self.angle == 225:
            self.rect.x += self.dx
            self.rect.y += self.dy





class Bonus(): # klasa bonus
    def __init__(self,image):
        self.bonus = pygame.image.load(image)  # pobranie obrazu (funkcja napisana wlasnorecznie)
        self.image = self.bonus  # obrazek
        self.rect = self.image.get_rect()  # pobranie wspolrzednych obrazu
        self.rect.x = random.randint(0,700) # randomowe wartosci x i y
        self.rect.y = random.randint(0,500)
        self.showBonus = False # pokazuje bonus
        self.bonusTime = 400 # czas po jakim zniknie bonus
        self.randBallBonus = random.randint(20,40) # ile wrogow trzeba zabic aby zostal pokazany bonus



class TextField(): # klasa pole tekstowe
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 28) # ustawienie fontu pola
        self.letters = "" # napis

    def showTextField(self):
        pygame.draw.rect(screen, (0, 0, 0),(200,150,400, 30), 0) # wewnetrzny prostokat

        pygame.draw.rect(screen, (255, 255, 255),(200,150,404, 34), 1) # zewnetrzny prostokat

        for event in pygame.event.get(): # pobranie eventow
            if event.type == pygame.KEYDOWN: # sprawdzenie eventu z klawiszami
                if (event.key > 96 and event.key < 123) or event.key == 32 :
                    # if sprawdzajacy czy nie zostaly nacisniete SHIFT,ALT,CTRL lub ENTER
                    self.letters += chr(event.key) # wpisywanie do napisu nastepnego znaku z klawiatury
                if event.key == pygame.K_BACKSPACE: # jesli zostalo klikniete BACKSPACE
                    self.letters = self.letters[0:len(self.letters)-1] # to z listy zostanie usunieta ostatnia litera

        rend = self.font.render(str(self.letters), True, (0, 255, 0)) # wyrenderowanie napisu
        screen.blit(rend, (204,150)) # wyblitowanie go
        return self.letters # zwrocenie ciagu znakow







class Button(): # klasa button(przycisk)
    def __init__(self,x,y,width,height): # inicjalizacja zmiennych
        self.x = x # x obszaru
        self.y = y # y obszaru
        self.width = width # szerokosc obszaru
        self.height = height # wysokosc obszaru
    def InvisibleButton(self): # obszar buttonu (a dokladniej niewidzialny button)
        position = pygame.mouse.get_pos() # pobranie pozycji myszy
        click = pygame.mouse.get_pressed()[0] # pobranie klikniecia lewego przycisku myszy

        if position[0] > self.x and position[0] < self.x + self.width and position[1] > self.y and position[1] < self.y + self.height and click == 1:
            # sprawdzenie czy pozycja myszy miesci sie w obszarze buttonu
            return True # jesli to prawda to true
        else:
            return False # w przeciwnym wypadku false
    def FocusedButton(self,picture): # sprawdzenie focusu najechania na obszar przycisku
        position = pygame.mouse.get_pos() # pobranie pozycji myszy
        if position[0] > self.x and position[0] < self.x + self.width and position[1] > self.y and position[1] < self.y + self.height:
            screen.blit(picture,(self.x,self.y)) # dodanie do obrazu obrazu






class Pictures(pygame.sprite.Sprite): # klasa do tla ktra dziedziczy po spraitach

    def __init__(self,image,width,height): # konstruktor klasy
        self.originalImage = pygame.image.load(image)  # zaladowanie obrazu (funkcja wbudowana do biblioteki pygame)
        self.image = pygame.transform.scale(self.originalImage, (width, height))  # rozciagniecie obrazu do wielkosci okna
        self.rect = self.image.get_rect() # pobranie plaszczyzny(prostokatnej)




class Player(pygame.sprite.Sprite): # klasa obslugujaca gracza

    def __init__(self, image, scale, clip, explosionSound, screen): # konstruktor klasy
        self.clip = clip
        self.ship = LoadImage(image, scale, clip) # pobranie obrazu (funkcja napisana wlasnorecznie)
        self.image = self.ship # obrazek
        self.image.set_colorkey((0,0,0)) # ustawienie przezroczystosci obrazu
        self.rect = self.image.get_rect() # pobranie wspolrzednych obrazu
        self.rect.x = 400 # ustawienie wspolrzednej x statku
        self.rect.y = 300 # ustawienie wspolrzednej y statku
        self.movementX = 0 # przesuniecie o punkt X
        self.movementY = 0 # przesuniecie o punkt Y
        self.accelerationX = 0 # przyspieszenie statku X
        self.accelerationY = 0 # przyspieszenie statku Y
        self.speed = 1 # predkosc
        self.angle = 0 # kat obrotu statku
        self.damp = 0.4 # zwolnienie statku
        self.maxAcceleration = 8 # maxymalne przyspieszenie statku
        self.colission = False # kolizje
        self.isWaitingToRespawn = False # czy czeka na respawn
        self.waitToRespawn = 0 # czas respawnu
        self.colissionList = [] # lista kolizyjna
        self.loadExplosion() # animacja eksplozji
        self.explosionSound = explosionSound # dzwiek eksplozji
        if self.colission:
            self.Spawn()  # wywolanie metody respawnujacej statek





    def loadExplosion(self): # metoda animujaca eksplozje
        self.explosionCurrentPicture = 0 # bierzaca ramka eksplozji
        self.explosionPictures = [] # lista ramek eksplozji
        frameWidth = 12 # szerokosc ramki

        for i in range(0,7): # petla wykonujaca sie 7 razy
            self.explosionPictures.append(LoadImage("images/Explode2.bmp", 4, (frameWidth*i ,0 , frameWidth, 13)))
            # dodawanie ramek animacji explozji


    def Spawn(self): # reset ustawien lokalizacji gracza
        self.reset()

    def Death(self): # metoda wykonywana gdy gracz zginie
        self.isWaitingToRespawn = True # czekanie na respawn
        self.waitToRespawn = 120 # ilosc sekund oczekiwania na respawn
        self.explosionCurrentPicture = 0 # bierzaca ramka explozji
        self.explosionSound.play() # funkcja ktora odtwarza dzwiek eksplozji

    def reset(self): # metoda resetujaca lokalizacje, przesuniecia i przyspieszenie gracza
        self.rect.x = 400 # ustawienie wspolrzednej x gry
        self.rect.y = 300 # ustawienie wspolrzednej y gry
        self.movementX = 0 # ustawienie przesuniecia X na 0
        self.movementY = 0 # ustawienie przesuniecia Y na 0
        self.accelerationX = 0 # przyspieszenie X na 0
        self.accelerationY = 0 # przyspieszenie Y n a 0
        self.colission = False # brak kolizji gracza z wrogiem

    def update(self): # metoda aktualizujaca
        # OPÓŹNIENIE
        if self.isWaitingToRespawn: # jesli gracz czeka na respawn
            #Animacja gdy gracz zginie
            if self.explosionCurrentPicture < len(self.explosionPictures): # jesli numer biezacej ramki eksplozji jest mniejszy od dlugosci listy to:
                self.image = self.explosionPictures[self.explosionCurrentPicture] # obraz ustawiamy na kolejne indeksy listy eksplozji
                self.image.set_colorkey((0,0,0)) # ustawiamy przezroczystosc ramki
                self.explosionCurrentPicture += 1 # zwiekszamy o 1 numer biezacej ramki eksplozji
            else: # w przeciwnym wypadku:
                self.image = pygame.Surface((0,0)) # ustawiamy plaszczyzne obrazu na wspolrzedne(0,0)

            self.waitToRespawn -= 1 # zmiejszamy o 1 czas oczekiwania na respawn
            if self.waitToRespawn <= 0: # jesli czas respawnu jest ponizej 0 to:
                self.isWaitingToRespawn = False # wtedy już nie czekamy na respawn bo gracz został zrespawnowany
                self.reset() # i resetujemy pozycje gracza
        else: # jesli gracz nie czeka na respawn to:
            controls = self.playerMoving() # ustawimy sterowanie gracza
            self.shipRotate(controls) # rotacja statku gracza
            self.image = pygame.transform.rotate(self.ship, self.angle) # wyrysowanie statku gracza
            self.image.set_colorkey((0,0,0)) # ustawienie przezroczystosci

            # Sprawdzanie kolizji
            self.checkColission()
            self.updateMoving()

        #Zastrzezenie granic okna dla statku
            if self.rect.y + self.clip[3]*2 >= screen.get_height():
                self.rect.y = screen.get_height() - self.clip[3]*2


            if self.rect.x + self.clip[3]*2 >= screen.get_width():
                self.rect.x = screen.get_width() - self.clip[3]*2


            if self.rect.y < 0:
                self.rect.y = 0


            if self.rect.x < 0:
                self.rect.x = 0
        super(Player,self).update()


    def checkColission(self):
        for gameObject in self.colissionList: # sprawdzanie listy kolizji
            self.colission = self.rect.colliderect(gameObject.rect) or self.rect.x < 15 or self.rect.x + 46  > 785
            if self.colission : # jesli kolizja wystapi to:
                self.Death() # smierc gracza
                for gameObject in self.colissionList: # i smierc wszystkich obiektow kolizyjnych
                    gameObject.Death()
                break

    def updateMoving(self):
        self.movementX += self.accelerationX # dodawanie przyspieszenia wsp. X
        self.movementY += self.accelerationY # dodawanie przyspieszenia przy wywolaniu metody

        #tłumienie poziome
        if self.movementX < 0 - self.damp: # jesli przesuniecie X jest mniejsze
            self.movementX +=self.damp # to do przesuniecia dodajemy opoznienie
        elif self.movementX > 0 +self.damp:
            self.movementX -= self.damp
        else:
            self.movementX = 0


        # tłumienie pionowe
        if self.movementY < 0 - self.damp:
            self.movementY += self.damp
        elif self.movementY > 0 + self.damp:
            self.movementY -= self.damp
        else:
            self.movementY = 0

        #Max Przyspieszenie (w skrocie powstrzymuje przed zwiekszaniem predkosci powyzej predkosci maxymalnej)
        if self.accelerationX > self.maxAcceleration:
            self.accelerationX = self.maxAcceleration
        if self.accelerationX < self.maxAcceleration * -1:
            self.accelerationX = self.maxAcceleration * -1
        if self.accelerationY > self.maxAcceleration:
            self.accelerationY = self.maxAcceleration
        if self.accelerationY < self.maxAcceleration * -1:
            self.accelerationY = self.maxAcceleration * -1

        # ustawienie wspolrzednych x i y gracza przez podane przesuniecie
        self.rect.x += self.movementX
        self.rect.y += self.movementY

    def playerMoving(self): # pobieranie kierunkow (strzalek) gracza
        up = pygame.key.get_pressed()[pygame.K_UP]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        left = pygame.key.get_pressed()[pygame.K_LEFT]

        return (up,right,down,left)

    def shipRotate(self,control): # obrocenia gracza o odpowiedni kąt
        self.angle = 0
        if control[0] == 1 and control[1] == 0 and control[2] == 0 and control[3] == 0:
            self.angle = 0
        elif control[0] == 1 and control[1] == 1 and control[2] == 0 and control[3] == 0:
            self.angle = 315
        elif control[0] == 0 and control[1] == 1 and control[2] == 0 and control[3] == 0:
            self.angle = 270
        elif control[0] == 0 and control[1] == 1 and control[2] == 1 and control[3] == 0:
            self.angle = 225
        elif control[0] == 0 and control[1] == 0 and control[2] == 1 and control[3] == 0:
            self.angle = 180
        elif control[0] == 0 and control[1] == 0 and control[2] == 1 and control[3] == 1:
            self.angle = 135
        elif control[0] == 0 and control[1] == 0 and control[2] == 0 and control[3] == 1:
            self.angle = 90
        elif control[0] == 1 and control[1] == 0 and control[2] == 0 and control[3] == 1:
            self.angle = 45

        self.accelerationX = self.speed * (control[1]-control[3])
        self.accelerationY = self.speed * (control[2] - control[0])
        # w przypadku gdy zostana nacisniete razem przyciski gora i dol lub lewo i prawo wtedy gracz sie nie poruszy wcale



class Enemy(pygame.sprite.Sprite): # klasa Enemy(wrogów) rozszerzona przez Sprite

    def __init__(self, image, scale, clip, bounds, gameTarget): # konstruktor klasy
        self.image = LoadImage(image, scale, clip) # wywołanie metody LoadImage i przypisanie jej do image
        self.image.set_colorkey(0x454e5b) # ustawienie przezroczystosci
        self.rect = self.image.get_rect() # pobranie wspolrzednych calego obrazu
        self.rect.x = 200 # ustawienie wspolrzednych obrazu (X)
        self.rect.y = 500 # ustawienie wspolrzednych obrazu (Y)
        self.accelerationX = 0 # przyspieszenie statku wroga (X)
        self.accelerationY = 0 # przyspieszenie statku wroga (Y)
        self.damp = 0.3 # opuznienie(tlumienie)
        self.maxAcceleration = 6 # maxymalne przyspieszenie
        self.boundX = bounds[0] # biezaca wspolrzedna x
        self.boundY = bounds[1] # biezaca wspolrzedna y
        self.isWaitingToRespawn = False # czekanie na respawn
        self.waitToRespawn = 0 # ile czasu czeka na respawn
        self.target = gameTarget # cel (czyli statek gracza)
        self.speed = 0.4 # predkosc statku wroga

        self.reset() # metoda resetujaca wrogow


    def update(self): # metoda aktualizujaca

        if self.isWaitingToRespawn:
            self.waitToRespawn -= 1
            if self.waitToRespawn <= 0:
                self.isWaitingToRespawn = False
                self.reset()
        else:
            self.checkState() # sprawdzanie stanu wrogów

            # tłumienie poziome
            if self.accelerationY < 0 - self.damp:
                self.accelerationY += self.damp
            elif self.accelerationY > 0 + self.damp:
                self.accelerationY -= self.damp
            else:
                self.accelerationY = 0

            # Max  - acceleration - przyspieszenie
            if self.accelerationX > self.maxAcceleration:
                self.accelerationX = self.maxAcceleration
            if self.accelerationX < self.maxAcceleration * -1:
                self.accelerationX = self.maxAcceleration * -1
            if self.accelerationY > self.maxAcceleration:
                self.accelerationY = self.maxAcceleration
            if self.accelerationY < self.maxAcceleration * -1:
                self.accelerationY = self.maxAcceleration * -1

            # aktualizacja pozycji wroga
            self.rect.x += self.accelerationX;
            self.rect.y += self.accelerationY;
            # sprawdzanie granic wrogów
            if self.rect.x > self.boundX or self.rect.y > self.boundY:
                self.Death()


    def Spawn(self):
        self.reset()

    def Death(self):
        self.isWaitingToRespawn = True # w razie smierci wroga , wrog czeka na respawn
        self.waitToRespawn = 120 # czas respawnu


    def reset(self):
        self.state = 1 # stan wroga ustawiamy na 1
        self.rect.x = random.randrange(0, self.boundX) * -1 # losowe ustawienie skad ma pojawic sie wrog
        self.rect.y = random.randrange(0, self.boundY) * -1
        self.accelerationX = 0 # reset przyspieszen
        self.accelerationY = 0




    def checkState(self): # Stany wrogow
        # Stan 1 - Sprawdzenie
        if self.state == 1:
            if math.sqrt((self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2) < 300:
                self.state = 2
            else:
                self.accelerationX += self.speed
                self.accelerationY += self.speed
        # Stan 2 - Poscig gracza
        elif self.state == 2:
            if math.sqrt((self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2) >= 300:
                self.state = 3
            else:
                targetVectorX = self.target.rect.x - self.rect.x
                targetVectorY = self.target.rect.y - self.rect.y
                distance = math.sqrt((0 - targetVectorX) ** 2 + (0 - targetVectorY) ** 2)
                targetVectorY /= distance
                targetVectorX /= distance
                # predkosc celu
                self.accelerationX += targetVectorX * self.speed
                self.accelerationY += targetVectorY * self.speed
        # Stan 3 - Zostaw gracza
        elif self.state == 3:
            self.accelerationX += self.speed
            self.accelerationY += self.speed



class Stone(pygame.sprite.Sprite): # asteroidy

    def __init__(self, image, scale, clip, bounds): # konstruktor klasy
        self.image = LoadImage(image, scale, clip) # obraz
        self.image.set_colorkey((0,0,0)) # przezroczystosc
        self.rect = self.image.get_rect() # pobranie wspolrzednych obrazu
        self.rect.x = 100 # wspolrzedna x
        self.rect.y = 400 # wspolrzedna y
        self.accelerationX = 0.01 # przyspieszenie poczatkowe asteroidy
        self.accelerationY = 0.01
        self.movementX = 0 # przesuniecie
        self.movementY = 0
        self.boundX = bounds[0] # x
        self.boundY = bounds[1] # y
        self.maxAcceleration = 3 # maxymalne przyspieszenie
        self.Spawn() # metoda spawnujaca
        self.isWaitingToRespawn = False # czekanie na respawn
        self.waitToRespawn = 0 # czas respawnu


    def Spawn(self): # reset
        self.reset()

    def Death(self): # smierc
        self.isWaitingToRespawn = True # czekanie na respawn
        self.waitToRespawn = 120 # czas respawnu

    def reset(self):
        self.rect.x = random.randrange(0, self.boundX) * -1 # losowa wspolrzedna poza planem
        self.rect.y = random.randrange(0, self.boundY) * -1

    def update(self): # aktualizacja stones

        # OPÓŹNIENIE
        if self.isWaitingToRespawn: # jesli czeka na respawn to:
            self.waitToRespawn -= 1 # czas respawnu sie zmiejsza
            if self.waitToRespawn <= 0: # jesli czas respawnu jest <= od 0 to:
                self.isWaitingToRespawn = False # juz nie czekamy na respawn
                self.reset() # reset koordynatow stones
        else: # w przeciwnym razie

            if self.movementX < self.maxAcceleration or self.movementY < self.maxAcceleration:
                # zwiekszanie przyspieszenia i  przesuniecia do momentu przekroczenia maksymalnego przyspieszenia
                self.movementX += self.accelerationX
                self.movementY += self.accelerationY

            self.rect.x += self.movementX;
            self.rect.y += self.movementY;



            if self.rect.x > self.boundX or self.rect.y > self.boundY:
                self.reset() # po przejsciu fali stones nastepna fala sie tworzy


class DataBase(): # baza danych
    def createTable(self,wynik): # metoda tworzaca tabele w bazie danych i sama baze danych

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='game')
        self.cursor = self.conn.cursor()

        self.players = [] # lista graczy
        self.players.append((self.n,wynik)) # dodanie gracza do listy graczy
        self.cursor.execute('INSERT INTO players (player,score) VALUES(%s,%s)', (self.n, wynik)) # wrzucenie wartosc do tabeli

        self.conn.commit()

    def readData(self):
        self.playerList = [] # lista graczy
        self.scoreList = [] # lista punktow
        self.cursor.execute(
            """
            SELECT player, score FROM players ORDER BY score DESC;
            """) # zapytanie pobierajace nick i score gracza i uporzadkowanie listy rosnaco
        self.players = self.cursor.fetchall()

        for gracz in self.players:
            self.playerList.append(str(gracz[0])) # wrzucenie do listy graczy graczy z bazy
            self.scoreList.append(str(gracz[1])) # wrzucenie do listy wynikow wynikow z bazy
            if len(self.playerList) >= 11: # jesli lista playerow jest rowna 11 to :
                self.cursor.execute('DELETE FROM players WHERE player = %s',(self.playerList[len(self.playerList) - 1]))
                self.conn.commit()
                self.playerList.pop() # gracz zostaje usuniety z listy
                self.scoreList.pop() # wynik zostaje usuniety z listy

        return (self.playerList, self.scoreList) # zwrocenie wszystkich graczy

    def writeData(self,string): # metoda czytajaca dane
        self.n = string


class Ball(pygame.sprite.Sprite): # klasa Pilki
    def __init__(self,image,scale,clip,x,y):
        self.image = LoadImage(image, scale, clip) # pobranie obrazu
        self.image.set_colorkey((0, 0, 0)) # ustawienie przezroczystosci
        self.rect = self.image.get_rect() # pobranie plaszczyzny
        self.rect.x = x # wspolrzedne x i y
        self.rect.y = y
        self.ifX = False
        self.clip = clip
        self.dx = 5 # przesuniecia dx i dy
        self.dy = 5
        self.stopBall = False # warunek zatrzymujacy pilke
        self.a = 0 # zmienne pomocnicze
        self.b = 0


    def update(self,player):
        screen.blit(self.image, (self.rect.x, self.rect.y)) # wyrysowanie kulki
        self.rect.x += self.dx # przesuniecie kulki w osi x i y
        self.rect.y += self.dy

        if player.isWaitingToRespawn == True: # zastopowanie kulki
            if self.stopBall == False:
                self.a = self.rect.x
                self.b = self.rect.y
                self.stopBall = True
            self.rect.x = self.a
            self.rect.y = self.b


        if self.rect.y + self.clip[3] >= screen.get_height(): # ograniczenie ruchow kulki do obszaru okna
            self.rect.y = screen.get_height()-self.clip[3]
            self.dy = -(self.dy)

        if self.rect.x + self.clip[3] >= screen.get_width():
            self.rect.x = screen.get_width() - self.clip[3]
            self.dx = -(self.dx)

        if self.rect.y  < 0:
            self.rect.y = 0
            self.dy = -(self.dy)

        if self.rect.x < 0:
            self.rect.x = 0
            self.dx = -(self.dx)

        if self.rect.colliderect(player): # kolizja kulki ze statkiem gracza (algorytm odbijania)
            pomx = (self.rect.x + self.clip[3]) - (player.rect.x + 23)
            pomy = (self.rect.y + self.clip[3]) - (player.rect.y + 23)

            if(pomx <= 0 and pomy <= 0):
                if(self.dx < 0 and self.dy > 0):
                    self.dy = -(self.dy)
                elif(self.dx > 0 and self.dy < 0):
                    self.dx = -(self.dx)
                elif(pomy > -10):
                    self.dx = -(self.dx)
                else:
                    self.dy = -(self.dy)
            elif(pomx > 0 and pomy <= 0):
                if(self.dx > 0 and self.dy >0):
                    self.dy = -(self.dy)
                elif(self.dx < 0 and self.dy < 0):
                    self.dx = -(self.dx)
                elif(pomy > -10):
                    self.dx = -(self.dx)
                else:
                    self.dy = -(self.dy)
            elif(pomx <= 0 and pomy > 0):
                if(self.dx < 0 and self.dy < 0):
                    self.dx = -(self.dx)
                elif(self.dx > 0 and self.dy > 0):
                    self.dx = -(self.dx)
                elif(pomy < 10):
                    self.dx = -(self.dx)
                else:
                    self.dy = -(self.dy)
            elif(pomx > 0 and pomy > 0):
                if(self.dx > 0 and self.dy < 0):
                    self.dy = -(self.dy)
                elif(self.dx < 0 and self.dy > 0):
                    self.dx = -(self.dx)
                elif(pomy < 10):
                    self.dx = -(self.dx)
                else:
                    self.dy = -self.dy

class Panel(): # klasa panel odpowiedzialna za panel glowny gry
    def showPane(self): # metoda pokazujaca panael
        global isStart
        isStart = False
        global wordList
        global napis
        screen.blit(backgroundPanel.image, (0, 0)) # wyrysowanie tla panelu
        screen.blit(panelPicture.image,(150,75)) # wyrysowanie napisu "Space Shooter"
        screen.blit(panelPlayOption.image,(315,300)) # wyrysowanie opcji play
        screen.blit(panelExitOption.image,(315,430)) # wyrysowanie opcji exit
        screen.blit(keysImage.image,(25,300))
        screen.blit(spaceImage.image,(30,480))



        playButton.FocusedButton(panelPlayFocusedOption.image) # obszar buttonu play
        exitButton.FocusedButton(panelExitFocusedOption.image) # obszar buttonu exit

        if pygame.key.get_pressed()[pygame.K_SPACE] or playButton.InvisibleButton() == True : # przykliknieciu spacji lub kliknieciu przycisku myszy gra sie rozpoczyna
            global startTime
            startTime = pygame.time.get_ticks()
            isStart = True
            global isBegin
            isBegin = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or exitButton.InvisibleButton() == True: # przy kliknieciu escape lub kliknieciu przycisku myszy zamykamy gre
            sys.exit()




pygame.init() # inicjalizacja biblioteki pygame
pygame.mixer.init() # inicjalizacja mixera biblioteki pygame
pygame.font.init() # inicjalizacja fontow
isEnd = False # zmienna pomocnicza
isWindow = True # zmienna pomocnicza
countDeathsAfter = 3 # liczba zyc
score = 0 # wynik

music = pygame.mixer.Sound("sound/march.wav") # zapisanie(wybór) muzyki do gry
explosion = pygame.mixer.Sound("sound/explosion.wav") # dzwiek eksplozji
shotSound = pygame.mixer.Sound("sound/ShipShot.wav") # wystrzeliwany pocisk
monster_kill = pygame.mixer.Sound("sound/monster_kill.wav") # dzwiek przy zabiciu
kill = pygame.mixer.Sound("sound/kill.wav") # dzwiek przy zabiciu
icon = pygame.transform.scale(pygame.image.load("images/icon.png"), (32,32)) # ikona okna
textField = TextField() # obiekt pole tekstowe
playButton = Button(315,300,180,100) # button play
exitButton = Button(315,430,180,100) # button exit
scoreArea = Button(260,200,300,120) # obszar save

countDeaths = 360
gameObjects = [] # lista obiektow gry
clock = pygame.time.Clock() # zegar gry

screen = pygame.display.set_mode((800,600)) # wywolanie okna w bibliotece pygame i przydzielenie mu rozmiaru 800x600
pygame.display.set_caption("Space Hunter v.1.0.0") # tytul okna gry
pygame.display.set_icon(icon) # dodanie ikony gry

background = Pictures("images/b.jpg",screen.get_width(), screen.get_height()) # ustawienie tla gry i ustalenie mu szerokosci i wysokosci jako szerokosc i wysokosc calego okna
backgroundPanel = Pictures("images/panel.jpg",screen.get_width(), screen.get_height()) # ustawienie tla gry i ustalenie mu szerokosci i wysokosci jako szerokosc i wysokosc calego okna
panelPicture = Pictures("images/napis.png",500, 200) # napis "Space Hunter"

panelPlayOption = Pictures("images/play.png",180,100) # obraz play opcji
panelPlayFocusedOption = Pictures("images/playFocused.png",180,100) # obraz sfokusowany play opcji

panelExitOption = Pictures("images/exit.png",180,100) # obraz exit opcji
panelExitFocusedOption = Pictures("images/exitFocused.png",180,100) # obraz sfokusowany exit opcji

lives = Pictures("images/lives.png",23,25) # zycia gracza
scoreAndName = Pictures("images/ScoreAndName.png",500,100) # wynik i nick w bazie

scoreButton = Pictures("images/save.png",300,120) # napis save
scoreButtonFocused = Pictures("images/saveFocused.png",300,120) # napis save sfokusowany
laserPicture = LoadImage("images/laser.png",1,(0,0,10,600)) # laser obraz
bonusBallPicture = Pictures("images/bonus_pilka.png",30,30) # obrazek bonusu pilki
bonusBallObject = Bonus("images/bonus_pilka.png") # objekt Bonus
namePicture = Pictures("images/imie.png",500,80) # napis "insert your nick"

player = Player("images/playership.bmp", 2, (25,1,23,23), explosion, screen) # obiekt typu Player
gameObjects.append(player) # dodawanie obiektu typu Player do listy obiektow gry
# playerRotation = pygame.transform.rotate(player.image,30) # transformowanie(obracanie) obrazu o 30 stopni

keysImage = Pictures("images/strzalki.png",200,175)
spaceImage = Pictures("images/spacja.png",198,75)

enemies = [] # lista enemies(wrogow)

for i in range(3):
    enemy = Enemy("images/enemy.png", 1, (0, 0, 78, 67), (screen.get_width() + 78, screen.get_height() + 67),player)
    # tworzenie obiektu Enemy na podstawie obrazu w skali 100% i przy zalozeniu punktu wejsciowego 101,13, szerokosci 91 i wysokosci 59
    enemies.append(enemy) # dodanie wroga do listy wrogow
    gameObjects.append(enemy) # dodanie wroga do listy obiektow gry
    player.colissionList.append(enemy) # dodanie wroga do listy kolizyjnej



asteroids = [] # tworzenie pustej listy stone

for i in range(5):
    thornStone = Stone("images/mine.bmp", 1, (0, 0, 49, 49), (screen.get_width() + 49, screen.get_height() + 49))
    # tworzenie obiektu stone na podstawie obrazu w skali 100% i przy zalozeniu punktu wejsciowego 6,3, szerokosci 80 i wysokosci 67


    asteroids.append(thornStone) # dodanie obiektu asteroidy do listy stone
    gameObjects.append(thornStone) # dodanie obiektu asteroidy do obiektow gry
    player.colissionList.append(thornStone)



baza = DataBase() # baza danych
start = True # start gry
mainLoop = True # glowna petla gry
isStart = False # sprawdzenie czy start
moreObjects = False # wiecej Stones
startTime = 0 # czas poczatkowy gry
levell = 1 # level
kills = 0 # zabici
points = 0 # punkty
panel = Panel() # obiekt panel
isBegin = False # sprawdzenie startu (poczatku gry)
showScore = False # pokazanie wynikow
string = "" # napis
ifShot = False # kulka
bulletList = [] # lista pociskow
delay = 25 # opoznienie strzelania
live = 0 # zycia
isBallCreated = False  # stworzenie kulki
isUpdateObjects = False
fps = 1000
while mainLoop: # glowna petla gry
    if isBegin == False: # sprawdzenie czy mozna wyswietlic panel
        panel.showPane()




    for event in pygame.event.get():  # pobranie eventu okna
        if event.type == pygame.QUIT:  # porownanie typu okna czy nie jest to button zamykajacy
            sys.exit()  # jesli bedzie to on wtedy okno zostaje zamkniete




    if isStart == True: # jesli start gry
        if moreObjects == True: # dodawanie nowych obiektow w grze
            for i in range(2):
                bomb = Stone("images/asteroid.png", 1, (0, 0, 49, 49), (screen.get_width() + 49, screen.get_height() + 49))
                # tworzenie obiektu bomb na podstawie obrazu w skali 100% i przy zalozeniu punktu wejsciowego 6,3, szerokosci 80 i wysokosci 67
                asteroids.append(bomb)  # dodanie obiektu asteroidy do listy asteroid
                gameObjects.append(bomb)  # dodanie obiektu asteroidy do obiektow gry
                player.colissionList.append(bomb) # dodanie do listy kolizji
                moreObjects = False

        score = ((pygame.time.get_ticks() - startTime) / 1000) + points # wynik gry


        if start == True: # odtworzenie muzyki w grze
            music.play(-1) # -1 oznacza zapetlenie sie muzyki
            start = False

        # renderowanie
        if isWindow == True:
            if player.colission: # jesli kolizja gracza z wrogiem to wtedy
                screen.fill(pygame.Color(255, 0, 0)) # wypelnienie ekranu czerownym kolorem
                countDeaths -= 1  # zmiejszenie licznika zyc
                countDeathsAfter = countDeaths / 120 # operacje zmiany licznka zyc
            else:
                live = int(round(countDeathsAfter, 0)) # zycie
                screen.blit(background.image, (0, 0))  # w przeciwnym wypadku tlem jest sprite


        if isEnd == False: # update obiektow gry
            for gameObject in gameObjects:  # lista obiektow gry
                screen.blit(gameObject.image, (gameObject.rect.x, gameObject.rect.y))  # wyrysowanie obiektow gry
                gameObject.update() # wywolanie metody aktualizujacej

        if isWindow == True:

            if live == 3:# wyswietlanie liczby zyc na ekranie w zaleznosci od ilosci zyc
                screen.blit(lives.image, (15, 0))
                screen.blit(lives.image, (45, 0))
                screen.blit(lives.image, (75, 0))
            if live == 2:
                screen.blit(lives.image, (15, 0))
                screen.blit(lives.image, (45, 0))
            if live == 1:
                screen.blit(lives.image, (15, 0))

            screen.blit(laserPicture, (5,0)) # wyrysowanie laserow
            screen.blit(laserPicture, (785, 0))

            space = pygame.key.get_pressed()[pygame.K_SPACE] # kliknieie spacji
            if space == 1: # jesli zostala kliknieta
                if delay == 0: # zostaje tworzony nowy pocisk i dodawane jest jego opoznienie
                    delay = 25
                    bullet = Bullet(player.rect.x, player.rect.y,player.angle)
                    bulletList.append(bullet)
                    shotSound.play()

            if delay > 0: # jesli opoznienie jest wieksze od 0 to wtedy odejmowane jest od opoznienia 1
                delay -= 1

            for i in bulletList: # lista pociskow wyrysowanie
                screen.blit(i.image, (i.rect.x+18, i.rect.y+18)) # wyrysownaie
                i.update() # aktualizacja
                if (i.rect.y + 10 >= screen.get_height() or i.rect.x + 10 >= screen.get_width() or i.rect.y < 0 or i.rect.x < 0) and len(bulletList) > 0 :
                    bulletList.remove(i) # usuniecie pocisku jesli przekroczy obszar gry
                for e in enemies: # sprawdzenie kolizji pocisku z wrogiem
                    if e.rect.colliderect(i.rect):
                        e.reset()
                        points += 100 # dodanie 100 punktow
                        if points % 1000 == 0: # sprawdzenie czy zostalo zlikwidowane 10 wrogow jesli tak to
                            kills += 1 # dodajemy do licznika zabitych 1
                            monster_kill.play() # odtwarzamy dzwiek
                            levell += 1 # zwiekszamy level
                            moreObjects = True # dodajemy wiecej obiekto w grze
                        else:
                            kills += 1 # licznik zabitych + 1
                            kill.play() # odtwarzanie dzwieku
            # wyrysowanie napisow w grze
            waves = pygame.font.SysFont("Arial", 30, bold="TRUE")
            waveLabel = waves.render("SCORE : " + str(int(score)), 1, (0, 255, 0))
            screen.blit(waveLabel, (15, 570))

            level = pygame.font.SysFont("Arial", 30, bold="TRUE")
            levelLabel = level.render("LEVEL : " + str(levell), 1, (0, 255, 0))
            screen.blit(levelLabel, (630, 570))

            kil = pygame.font.SysFont("Arial", 30, bold="TRUE")
            kilLabel = kil.render("KILLS : " + str(kills), 1, (0, 255, 0))
            screen.blit(kilLabel, (630, 0))
            # bonus kulki w grze
            if (kills == bonusBallObject.randBallBonus) and bonusBallObject.bonusTime > 0:
                screen.blit(bonusBallPicture.image,(bonusBallObject.rect.x,bonusBallObject.rect.y))
                bonusBallObject.bonusTime -= 1

            # utworzenie kulki i sprawdzenie kolizji
            if player.rect.colliderect(bonusBallObject.rect) or bonusBallObject.showBonus == True:
                if isBallCreated == False:
                    ball = Ball("images/pilka.png", 1, (0, 0, 25, 25), 200, 200)
                    isBallCreated = True
                    bonusBallObject.bonusTime = 0
                bonusBallObject.showBonus = True
                if kills < 30:
                    ball.update(player)
                    for i in enemies:
                        if i.rect.colliderect(ball):
                            i.reset()
                            points += 100
                            if points % 1000 == 0:
                                monster_kill.play()
                                levell += 1
                                moreObjects = True

                            else:
                                kills += 1
                                kill.play()



    # jesli liczba zyc gracza jest rowna 0 to wtedy
    if countDeathsAfter == 0:
        isStart = False
        isBegin = False
        # wyrysowanie tla gry
        screen.blit(background.image, (0, 0))
        # ustawienie czekania na respawn dla wszystkich
        if isUpdateObjects == False:
            for gameObject in gameObjects:
                gameObject.isWaitingToRespawn = True
            isUpdateObjects = True

        isEnd = True # zastopowanie dzwiekow w grze
        music.stop()

        # sprawdzenie czy we wpisane pole tekstowe zostalo wpisane przynajmniej 5 znakow
        if scoreArea.InvisibleButton() == True and (len(string) > 2 and len(string) < 5):
                baza.writeData(string)
                showScore = True

        # wyrysowanie buttonu 'save'
        if showScore == False:
            screen.blit(namePicture.image,(150,30))
            string = textField.showTextField()
            screen.blit(scoreButton.image,(260,200))
            scoreArea.FocusedButton(scoreButtonFocused.image)


        if showScore == True: # pokazanie wynikow graczy
            screen.blit(scoreAndName.image, (180, 30))  # wyrysowanie napisu Score and Nick
            if isWindow == True:
                baza.createTable(int(score)) # utworzenie lub otworzenie tabeli
                isWindow = False
            listaP = baza.readData() # odczyt danych
            strGr = "" # pomoznicze zmienne
            a = 0
            b = 0
            for i in listaP[0]: # 0 element listy
                a += 40 # odstpy w nickach graczy
                strGr = str(i)
                napis = pygame.font.SysFont("Arial", 40, bold="TRUE")  # ustawienie czcionki napisów w grze
                napisLab = napis.render(strGr, 1, (0, 255, 0))  # wyrenderowanie napisów gry
                screen.blit(napisLab, (180, 70 + a))  # wyrysowanie napisów gry
            for i in listaP[1]:
                b += 40
                strGr = str(i)
                napis = pygame.font.SysFont("Arial", 40, bold="TRUE")  # ustawienie czcionki napisów w grze
                napisLab = napis.render(strGr, 1, (0, 255, 0))  # wyrenderowanie napisów gry
                screen.blit(napisLab, (565, 70 + b))  # wyrysowanie napisów gry

    pygame.display.flip() # odswiezanie okna
    clock.tick(50) # zegar gry


