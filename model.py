
class Visible:
    #初期化、name,visual_nameはstring、x_pos、y_posは左上をさす
    def __init__(self,init_x_pos,init_y_pos,name,size):
        self.is_appear = True
        self.init_x_pos = init_x_pos
        self.init_y_pos = init_y_pos
        self.x_pos = init_x_pos
        self.y_pos = init_y_pos
        self.name = name
        self.size = size

    def delete(self):
        self.is_appear = False #is_apperをFalseにすることでvisiblesから削除される

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def get_name(self):
        return self.name

class Ball(Visible):

    #x_speedとy_speedが追加
    def __init__(self, init_x_pos, init_y_pos, name, size,x_speed,y_speed):
        super().__init__(init_x_pos, init_y_pos, name, size)
        self.x_speed = x_speed
        self.y_speed = y_speed

    #xの移動方向を変える
    def turn_x(self):
        self.x_speed = -self.x_speed

    #yの移動方向を変える
    def turn_y(self):
        self.y_speed = -self.y_speed

    #speedの分だけ座標を移動させる
    def move(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

    def set_x_speed(self,speed):
        self.x_speed = speed

    def set_y_speed(self,speed):
        self.y_speed = speed

    
class Item(Ball):
    
    #アイテムは下に落ちるだけなのでx_speedを0にする
    #item_typeはitemの種類を表しています。
    #種類はspeedup,twin,biggerの３種類です。main関数のinteractなんたらーで利用しています。
    def __init__(self, init_x_pos, init_y_pos, name, size, x_speed, y_speed,item_type):
        super().__init__(init_x_pos, init_y_pos, name, size, x_speed, y_speed)
        self.x_speed = 0
        self.item_type = item_type

    def get_item_type(self):
        return self.item_type


class Bar(Visible):

    #lengthとx_speedを追加。
    def __init__(self, init_x_pos, init_y_pos, name, size,x_speed):
        super().__init__(init_x_pos, init_y_pos, name, size)
        self.x_speed = x_speed

    #バーの座標に制限をもうける。バーを動かせるならTrueを返す
    def can_move(self):
        if self.x_pos < -3:
            self.x_pos = self.x_pos + 5
            return False
        if 603 < self.x_pos:
            self.x_pos = self.x_pos - 5
            return False

        return True

    #バーを動かしていいなら、プラス方向へ進める
    def move_right(self):
        if self.can_move():
            self.x_pos += self.x_speed

    #バーを動かしていいなら、マイナス方向へ進める
    def move_left(self):
        if self.can_move():
            self.x_pos -= self.x_speed

    def set_length(self,length):
        self.length = length

class Block(Visible):
    #itemオブジェクトを入れる変数を持たせる。初期値はNone
    def __init__(self, init_x_pos, init_y_pos, name,size):
        super().__init__(init_x_pos, init_y_pos, name,size)
        self.item = None

    #itemを持っているかどうか
    def has_item(self):
        if self.item == None:
            return False
        else:
            return True

    #ブロックとボールの当たり判定
    def hit_block(self,ball):
        if self.get_x_pos() <ball.get_x_pos()< self.get_x_pos() + 140:
            if self.get_y_pos() < ball.get_y_pos() <self.get_y_pos() + 40:
                return True

    #Itemオブジェクトを引数に持つ
    def set_item(self,item):
        self.item= item

    def get_item_type(self):
        return self.item.get_item_type()


class Button(Visible):
    def __init__(self, init_x_pos, init_y_pos, name,size):
        super().__init__(init_x_pos, init_y_pos, name,size)
    
    #押された場所か内部かどうかを判定する
    def is_inner(self,mouse_pos):
        if self.x_pos < mouse_pos[0] and mouse_pos[0] < self.x_pos + self.size[0]:
            if self.y_pos < mouse_pos[1] and mouse_pos[1] < self.y_pos + self.size[1]:
                return True
            else:
                return False


class Model:

    def __init__(self,view):
        self.view = view
        self.blocks = [[None for i in range(5)] for j in range(4)] #２次元配列
        self.bar = None
        self.visibles = []

    #Controllerで呼び出す.
    def move(self,identifier_key):
        #キー入力に応じて移動させる
        if identifier_key == "right":
            self.bar.move_right()
        if identifier_key == "left":
            self.bar.move_left()

    #Blockを作成し、blocksに入れる
    def create_blocks(self):
        for i in range(4):
            for j in range(5):
                #iとjの値を参考にBlockの座標を決める
                bl = Block(j*140,i*40,"block",(140,40))
                self.blocks[i][j] = bl
                self.visibles.append(bl)
        

    #ボタンを作成して、visiblesに追加する
    def create_button(self,x_pos,y_pos,name,size):
        bt = Button(x_pos,y_pos,name,size)
        self.visibles.append(bt)

    #画像を作成して、visiblesに追加する
    def create_picture(self,x_pos,y_pos,name,size):
        pi = Visible(x_pos,y_pos,name,size)
        self.visibles.append(pi)

    #ブロックとボールが接触した時の処理を書く。
    def interact_block_ball(self,ball):
        for e in range(4):
            for b in range(5):
                
                #下側からぶつかった時
                if self.blocks[e][b].is_appear == True and self.blocks[e][b].hit_block(ball):
                    ball.turn_y()
                    self.blocks[e][b].delete()

                    #ゲームクリアした時の処理
                    if self.is_clear():
                        self.visibles_clear()
                        self.make_clear()

    #バーとボールが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_bar_ball(self,bar,ball):
        #もし接触していたら、
        if bar.x_pos -10< ball.x_pos < bar.x_pos + bar.size[0]:#-10しているのは判定の微調整のため
            if  bar.y_pos  < ball.y_pos + 30 < bar.y_pos + 20:
                ball.turn_y()

    #バーとアイテムが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_bar_item(self,item):
        #もし接触していたら、
        if self.bar.x_pos -10< item.x_pos < self.bar.x_pos + self.bar.size[0]:#-10しているのは判定の微調整のため
            if  self.bar.y_pos  < item.y_pos + 30 < self.bar.y_pos + 20:
                # アイテムの種類によって処理を変える。
                if item.get_item_type() == "speedup":
                    for e in self.visibles:
                        if e.name =="ball":
                            if e.x_speed < 0:
                                e.x_speed = e.x_speed - 5
                            else:
                                e.x_speed = e.x_speed + 5

                            if e.y_speed < 0:
                                e.y_speed = e.y_speed - 5
                            else:
                                e.y_speed = e.y_speed + 5

                    item.delete()

                elif item.get_item_type() == "twin":
                    return
                elif item.get_item_type() == "bigger":
                    x_pos = self.bar.get_x_pos()
                    y_pos = self.bar.get_y_pos()
                    self.bar.delete()

                    self.bar = Bar(x_pos,y_pos,"bar",(150,20),6)
                    self.visibles.append(self.bar)

                    item.delete()

    #壁とボールが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_wall_ball(self,ball):
        
        if ball.x_pos < 5 or 695 < ball.x_pos:#左右の壁に衝突したなら
            ball.turn_x()
        #上の壁に衝突したなら
        if  ball.y_pos < 5 :
            ball.turn_y()
        #下の壁に衝突したなら消す
        if 795 < ball.y_pos:
            ball.delete()

    #clearかどうか
    def is_clear(self):
        for e in self.blocks:
             for j in e:
                 if j.is_appear == True:
                     return False #ブロックがあればFalse
        return True

    #gameoverかどうか
    def is_gameover(self):
        for v in self.visibles:
            if v.name == "ball" and v.is_appear == True or self.is_clear()==True:
                return False

        return True

    #title画面を作る
    def make_title(self):
        #ウィンドウサイズと同じ画像を作る
        self.create_picture(0,0,"title",(700,800))
        self.create_button(200,500,"start",(260,80))
        self.create_button(200,600,"score",(260,80))
        #描画順を調整する
        self.sort_visual_order()
    
    #play画面を作る
    def make_game_play(self):
        self.create_picture(0,0,"play",(700,800))
        self.bar = Bar(300,700,"bar",(100,20),6)
        self.ball = Ball(200,200,"ball",(30,30),5,5)
        self.create_blocks()

        #item_1 = Item(300,300,"item",(30,30),0,1,"speedup")
        #self.visibles.append(item_1)

        self.visibles.append(self.bar)
        self.visibles.append(self.ball)
        self.sort_visual_order()

    #クリア画面を作る
    def make_clear(self):
        self.create_picture(0,0,"clear",(700,800))
        self.create_button(200,500,"start",(260,80))
        self.sort_visual_order()

    #ゲームオーバー画面を作る
    def make_gameover(self):
        self.create_picture(0,0,"gameover",(700,800))
        self.create_button(200,500,"retry",(260,80))
        self.create_button(200,600,"exit",(260,80))

    #描画する順番を調整する
    def sort_visual_order(self):
        for e in self.visibles:
            #背景の要素を最初に描画するようにする
            if e.name == "title":
                self.visibles.remove(e)
                temp = self.visibles[0]
                self.visibles[0] = e
                self.visibles.append(temp)

    #全てのvisiblesを削除する
    def visibles_clear(self):
        for v in self.visibles:
            v.delete()

    #おそらく、毎秒呼び出すような。そんな感じの処理をまとめる。
    def update(self):

        #サンプルコードを参考にしている。何をしているかはわからない。
        for v in self.visibles[:]:
            #viewに書くべきオブジェクトを通知する
            self.view.draw(v)

            #ここにボールに関する、毎回実行した方が良いようなものをまとめおく
            if v.get_name() == "ball":
                v.move()
                self.interact_bar_ball(self.bar,v)
                self.interact_block_ball(v)
                self.interact_wall_ball(v)      

                #ゲームオーバーか調べる
                if self.is_gameover():
                    self.visibles_clear()
                    self.make_gameover()          
               
            
            #ここにアイテムに関する、毎回実行した方が良さそうなものをまとめておく
            if v.get_name() == "item":
                v.move()
                self.interact_bar_item(v)

            if v.is_appear == False:
                print(v.name)
                self.visibles.remove(v)
            



            
        

    

