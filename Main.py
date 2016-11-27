#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame # biblioteka pygame potrzebna do stworzenia gry
import random # biblioteka random potrzebna do losowej organizacji stones
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
import math # klasa matematyczna
import sqlite3
from tkinter import *
import tkinter
import math
import sys


import pygame


def LoadImage(image,scale,clip): # funkcja ktora laduje obrazy
    picture = pygame.image.load(image)  # zaladowanie obrazu  do zmiennej
    playerSurface = pygame.Surface((clip[2], clip[3])) # stworzenie nowej powierzchni
    playerSurface.blit(picture, (0, 0), clip)  # przyciecie obrazu i wyrysowanie go
    scaledPicture = (clip[2] * scale, clip[3] * scale) # lista potrzebna do tworzenia przeskalowanego obrazu
    scaledPicture = pygame.transform.scale(playerSurface, (clip[2] * scale, clip[3] * scale) ) # skalowanie obrazu

    return scaledPicture # zwrocenie przeskalowanego obrazu

class Button():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def InvisibleButton(self):
        position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if position[0] > self.x and position[0] < self.x + self.width and position[1] > self.y and position[1] < self.y + self.height and click == 1:
            return True
        else:
            return False
    def FocusedButton(self,picture):
        position = pygame.mouse.get_pos()
        if position[0] > self.x and position[0] < self.x + self.width and position[1] > self.y and position[1] < self.y + self.height:
            screen.blit(picture,(self.x,self.y))






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
            self.colission = self.rect.colliderect(gameObject.rect) or self.rect.x < 10 or self.rect.x + 46  > 790
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
            self.checkState()

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


    def resetOffScreen(self): # reset wspolrzednych wroga
        self.rect.x = self.boundX
        self.rect.y = self.boundY




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


class DataBase():
    def createTable(self,wynik):

        self.connection = sqlite3.connect('baza_danych.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        # DROP TABLE IF EXISTS gracz;
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS gracz (nick varchar(250) NOT NULL,wynik INTEGER)""")

        self.gracze = []
        self.gracze.append((self.n,wynik))


        self.cursor.executemany('INSERT INTO gracz VALUES(?,?)', self.gracze)
        self.connection.commit()

    def readData(self):
        self.playerList = []
        self.scoreList = []
        self.cursor.execute(
            """
            SELECT nick, wynik FROM gracz ORDER BY wynik DESC
            """)
        self.gracze = self.cursor.fetchall()
        for gracz in self.gracze:
            self.playerList.append(str(gracz['nick']))
            self.scoreList.append(str(gracz['wynik']))
            if len(self.playerList) == 11:
                self.playerList.pop()
                self.scoreList.pop()
                self.gracze.pop()
        return (self.playerList, self.scoreList)




    def writeDataUser(self):
        self.main = tkinter.Tk()
        self.main.resizable(width=False,height=False)
        self.main.title("Nick")
        self.infoName = tkinter.Label(self.main,text="Podaj swoj nick")
        self.infoName.grid(row = 0, column = 0)
        self.name = Entry(self.main)
        self.name.grid(row = 0, column = 1)
        self.buttonName = tkinter.Button(self.main,text="Zapisz",command = self.getNick)
        self.buttonName.grid(row=1, column=1)
        self.main.mainloop()




    def getNick(self):
        self.n = self.name.get()
        self.main.destroy()


class Shot(pygame.sprite.Sprite):
    def __init__(self,image,scale,clip,x,y):
        self.image = LoadImage(image, scale, clip)
        self.image.set_colorkey((0, 0, 0))
        self.distance = 30
        self.speedShot = 7
        self.shotTime = 40
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ifX = False
        self.clip = clip
        self.dx = 5
        self.dy = 5
        self.stopBall = False
        self.a = 0
        self.b = 0


    def update(self,player):
        if pygame.key.get_pressed()[pygame.K_SPACE] or True:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.rect.x += self.dx
            self.rect.y += self.dy

        if player.isWaitingToRespawn == True:
            if self.stopBall == False:
                self.a = self.rect.x
                self.b = self.rect.y
                self.stopBall = True
            self.rect.x = self.a
            self.rect.y = self.b


        if self.rect.y + self.clip[3] >= screen.get_height():
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

        if self.rect.colliderect(player):
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


class Panel():
    def showPane(self):
        global isStart
        isStart = False
        screen.blit(backgroundPanel.image, (0, 0))
        screen.blit(panelPicture.image,(150,75))
        screen.blit(panelPlayOption.image,(315,300))
        screen.blit(panelExitOption.image,(315,430))

        playButton.FocusedButton(panelPlayFocusedOption.image)
        exitButton.FocusedButton(panelExitFocusedOption.image)

        if pygame.key.get_pressed()[pygame.K_SPACE] or playButton.InvisibleButton() == True :
            global startTime
            startTime = pygame.time.get_ticks()
            isStart = True
            global isBegin
            isBegin = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or exitButton.InvisibleButton() == True:
            sys.exit()




pygame.init() # inicjalizacja biblioteki pygame
pygame.mixer.init() # inicjalizacja mixera biblioteki pygame

isEnd = False
isWindow = True
countDeathsAfter = 3
score = 0

music = pygame.mixer.Sound("sound/march.wav") # zapisanie(wybór) muzyki do gry
explosion = pygame.mixer.Sound("sound/explosion.wav") # dzwiek eksplozji
monster_kill = pygame.mixer.Sound("sound/monster_kill.wav") # dzwiek przy zabiciu
kill = pygame.mixer.Sound("sound/kill.wav") # dzwiek przy zabiciu
icon = pygame.transform.scale(pygame.image.load("images/icon.png"), (32,32))

playButton = Button(315,300,180,100)
exitButton = Button(315,430,180,100)
countDeaths = 360
gameObjects = [] # lista obiektow gry
clock = pygame.time.Clock() # zegar gry
shot = Shot("images/pilka.png", 1, (0, 0 , 25, 25),200,200)
screen = pygame.display.set_mode((800,600)) # wywolanie okna w bibliotece pygame i przydzielenie mu rozmiaru 800x600
pygame.display.set_caption("Space Hunter v.1.0.0")
pygame.display.set_icon(icon)
background = Pictures("images/b.jpg",screen.get_width(), screen.get_height()) # ustawienie tla gry i ustalenie mu szerokosci i wysokosci jako szerokosc i wysokosc calego okna
backgroundPanel = Pictures("images/panel.jpg",screen.get_width(), screen.get_height()) # ustawienie tla gry i ustalenie mu szerokosci i wysokosci jako szerokosc i wysokosc calego okna
panelPicture = Pictures("images/napis.png",500, 200)

panelPlayOption = Pictures("images/play.png",180,100)
panelPlayFocusedOption = Pictures("images/playFocused.png",180,100)

panelExitOption = Pictures("images/exit.png",180,100)
panelExitFocusedOption = Pictures("images/exitFocused.png",180,100)

lives = Pictures("images/lives.png",23,25)
scoreAndName = Pictures("images/ScoreAndName.png",500,100)

laserPicture = LoadImage("images/laser.png",1,(0,0,10,600))


player = Player("images/playership.bmp", 2, (25,1,23,23), explosion, screen) # obiekt typu Player
gameObjects.append(player) # dodawanie obiektu typu Player do listy obiektow gry
# playerRotation = pygame.transform.rotate(player.image,30) # transformowanie(obracanie) obrazu o 30 stopni



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



baza = DataBase()
start = True
mainLoop = True
isStart = False
moreObjects = False
startTime = 0
levell = 1
kills = 0
bonus = 0
panel = Panel()
# livep = LivePictures()
# livep.showLives()
isBegin = False


while mainLoop: # glowna petla gry
    if isBegin == False:
        panel.showPane()




    for event in pygame.event.get():  # pobranie eventu okna
        if event.type == pygame.QUIT:  # porownanie typu okna czy nie jest to button zamykajacy
            sys.exit()  # jesli bedzie to on wtedy okno zostaje zamkniete




    if isStart == True:
        if moreObjects == True:
            for i in range(2):
                bomb = Stone("images/asteroid.png", 1, (0, 0, 49, 49), (screen.get_width() + 49, screen.get_height() + 49))
                # tworzenie obiektu bomb na podstawie obrazu w skali 100% i przy zalozeniu punktu wejsciowego 6,3, szerokosci 80 i wysokosci 67
                asteroids.append(bomb)  # dodanie obiektu asteroidy do listy asteroid
                gameObjects.append(bomb)  # dodanie obiektu asteroidy do obiektow gry
                player.colissionList.append(bomb)
                moreObjects = False

        score = ((pygame.time.get_ticks() - startTime) / 1000) + bonus

        # dodawanie kolizji do wrogów
        for i in enemies:
            if i.rect.colliderect(shot):
                i.reset()
                bonus += 100
                if bonus % 1000 == 0:
                    monster_kill.play()
                    levell += 1
                    moreObjects = True
                else:
                    kills += 1
                    kill.play()



        if start == True:
            music.play(-1)
            start = False

        # renderowanie
        if isWindow == True:
            if player.colission:
                screen.fill(pygame.Color(255, 0, 0))
                countDeaths -= 1  # licznik zyc

                countDeathsAfter = countDeaths / 120
            else:
                screen.blit(background.image, (0, 0))  # w przeciwnym wypadku tlem jest sprite


        if isEnd == False:
            for gameObject in gameObjects:  # lista obiektow gry
                screen.blit(gameObject.image, (gameObject.rect.x, gameObject.rect.y))  # wyrysowanie obiektow gry
                gameObject.update()

        if isWindow == True:
            # waves = pygame.font.SysFont("Arial", 30, bold="TRUE")
            live = 0
            live = int(round(countDeathsAfter, 0))
            # waveLabel = waves.render("LIVES : " + str(live), 1, (0, 255, 0))
            # screen.blit(waveLabel, (0, 0))

            if live == 3:
                screen.blit(lives.image, (15, 0))
                screen.blit(lives.image, (45, 0))
                screen.blit(lives.image, (75, 0))
            if live == 2:
                screen.blit(lives.image, (15, 0))
                screen.blit(lives.image, (45, 0))
            if live == 1:
                screen.blit(lives.image, (15, 0))

            screen.blit(laserPicture, (0,0))
            screen.blit(laserPicture, (790, 0))





            waves = pygame.font.SysFont("Arial", 30, bold="TRUE")
            waveLabel = waves.render("SCORE : " + str(score), 1, (0, 255, 0))
            screen.blit(waveLabel, (15, 570))

            level = pygame.font.SysFont("Arial", 30, bold="TRUE")
            levelLabel = level.render("LEVEL : " + str(levell), 1, (0, 255, 0))
            screen.blit(levelLabel, (630, 570))

            kil = pygame.font.SysFont("Arial", 30, bold="TRUE")
            kilLabel = kil.render("KILLS : " + str(kills), 1, (0, 255, 0))
            screen.blit(kilLabel, (630, 0))


            shot.update(player)


            #############################################################################################################

        if countDeathsAfter == 0:

            screen.blit(background.image, (0, 0))

            for gameObject in gameObjects:
                gameObject.isWaitingToRespawn = True
                screen.blit(background.image, (0, 0))
            isEnd = True
            music.stop()


            screen.blit(scoreAndName.image, (180, 30))  # wyrysowanie napisów gry

            if isWindow == True:
                baza.writeDataUser()
                baza.createTable(score)
                isWindow = False

            listaP = baza.readData()
            strGr = ""
            a = 0
            b = 0
            for i in listaP[0]:
                a += 40
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

    pygame.display.flip()

    clock.tick(60)

