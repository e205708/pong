# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *
from model import Model

WIN_SIZE = (700,800)
WIN_TITLE = "break_block"
class View:
    def __init__(self,screen):
        self.screen = screen
        self.sprites = {}
        self.sprites["bar"] = pygame.image.load("sprites/bar_small.png")
        self.sprites["ball"] = pygame.image.load("sprites/ball_small.png")
        self.sprites["block"] = pygame.image.load("sprites/block_small.png")
        self.sprites["special_block"] = pygame.image.load("sprites/special_block_small.png")
        self.sprites["speedup"] = pygame.image.load("sprites/item_ballspeed_small.png")
        self.sprites["twin"] = pygame.image.load("sprites/item_ballplus_small.png")
        self.sprites["bigger"] = pygame.image.load("sprites/item_longver_small.png")
        self.sprites["title"] = pygame.image.load("sprites/title.png")
        self.sprites["play"] = pygame.image.load("sprites/play.png")
        self.sprites["clear"] = pygame.image.load("sprites/clear.png")
        self.sprites["gameover"] = pygame.image.load("sprites/gameover.png")
        self.sprites["start"] = pygame.image.load("sprites/start.png")
        self.sprites["score"] = pygame.image.load("sprites/score.png")
        self.sprites["retry"] = pygame.image.load("sprites/retry.png")
        self.sprites["exit"] = pygame.image.load("sprites/exit.png")


    def draw(self,visible_obj):
        if(visible_obj.name == "item"):
            img = self.sprites[visible_obj.item_type]
            img_trasform = pygame.transform.scale(img,visible_obj.size) #画像サイズの調整
        elif(visible_obj.name=="text"):
            font = pygame.font.Font(None, 55) 
            img_trasform = font.render(visible_obj.text+"point",True,(255,255,255))
        else:
            img = self.sprites[visible_obj.name]
            img_trasform = pygame.transform.scale(img,visible_obj.size) #画像サイズの調整

        if(visible_obj.name == "block"):
            if visible_obj.has_item():
                img = self.sprites["special_block"]
                img_trasform = pygame.transform.scale(img,visible_obj.size) #画像サイズの調整

        self.screen.blit(img_trasform,(visible_obj.x_pos,visible_obj.y_pos))

    
class Controller:
    def __init__(self,model):
        self.model = model

    def left_key_down(self):
        self.model.move("left")
    
    def right_key_down(self):
        self.model.move("right")

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption(WIN_TITLE)

        self.view = View(self.screen)
        self.model = Model(self.view)
        self.controller = Controller(self.model)

        self.model.make_title() # タイトル画面を作成する。

        pygame.key.set_repeat(5,15) #キーの長押しに対応するようにする。

    '''
    イベントに関する処理。ボタン、キーが押された時の処理を書く。
    '''
    def event_controll(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()        
            
            #キー入力に関するもの
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.controller.left_key_down()
                elif event.key == K_RIGHT:
                    self.controller.right_key_down()
            
            #ボタンが押された時の処理
            if event.type == pygame.MOUSEBUTTONDOWN:
                for e in self.model.visibles:
                    if e.name == "start" and e.is_inner(event.pos): #スタートボタンが押された時
                        #画面に表示されている要素を全て削除する
                        self.model.visibles_clear()
                        self.model.make_game_play() #プレイ画面を作る
                    
                    if e.name == "retry" and e.is_inner(event.pos): #retryボタンが押されたら
                        #画面に表示されている要素を全て削除する
                        self.model.visibles_clear()
                        self.model.make_game_play() #プレイ画面を作る

                    if e.name == "exit" and e.is_inner(event.pos):
                        pygame.quit()
                        sys.exit()  

    def event_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.event_controll()
            self.screen.fill((0,0,0))
            self.model.update()
            pygame.display.update()

if __name__ == "__main__":
    app = App()
    app.event_loop()