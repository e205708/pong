
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
    def __init__(self, init_x_pos, init_y_pos, name, size, length, x_speed):
        super().__init__(init_x_pos, init_y_pos, name, size)
        self.length = length
        self.x_speed = x_speed

    #バーの座標に制限をもうける。バーを動かせるならTrueを返す
    def can_move(self):
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
        self.blocks = []
        self.bar = None
        self.ball = None
        self.visibles = []

    #Controllerで呼び出す.
    def move(self,identifier_key):
        #キー入力に応じて移動させる
        if identifier_key == "right":
            self.bar.move_right()
        if identifier_key == "left":
            self.bar.move_left()

    #Blockを作成し、blocksに入れる、関数にする必要があるのかはわからない
    #blockもvisiblesに入れた方がいいのかなぁ。まあ層の方がいいのかもな・・・とするとなんでblocks作ったのかが・・・
    def cleate_blocks(self):
        for i in range(5):
            for j in range(4):
                #iとjの値を参考にBlockの座標を決める
                self.blocks[i][j] = Block()

    #ボタンを作成して、visiblesに追加する
    def create_button(self,x_pos,y_pos,name,size):
        bt = Button(x_pos,y_pos,name,size)
        self.visibles.append(bt)

    #画像を作成して、visiblesに追加する
    def create_picture(self,x_pos,y_pos,name,size):
        pi = Visible(x_pos,y_pos,name,size)
        self.visibles.append(pi)

    #ブロックとボールが接触した時の処理を書く。ここが一番難関になるでしょう。
    def interact_block_ball(self):
        #どうにかぶつかったブロックを見つけてblock.deleteしたい。で適切なball_turnを呼び出す。
        #接触したかどうか？もここに書くつもりだけど、サンプルをみるに、別「接触したか？」を調べる関数を作り。
        #ここでは接触した時に「処理」だけを書くという方法もあるけど・・・んーー
        return

    #バーとボールが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_bar_ball(self):
        #ここで接触したかも判定するつもり。
        #もし接触していたら、
        self.ball.turn_y()

    #バーとアイテムが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_bar_item(self,item):
        #item.nameに応じてif分で処理を変えていく方がいいかもしれないね。
        #そしたらitemのtouch()はいらなくなるかも？
        #ここも接触したアイテムオブジェクトを特定する必要があるね・・・
        if item.get_item_type() == "speedup":
            return
        elif item.get_item_type() == "twin":
            return
        elif item.get_item_type() == "bigger":
            return

    #壁とボールが接触したかの判定とその場合の処理を書く。updateで呼び出す
    def interact_wall_ball(self):
        #左右の壁に衝突したなら
        self.ball.turn_x()
        #上の壁に衝突したなら
        self.ball.turn_y()
        #下の壁に衝突したなら消す
        self.ball.delete()

    #title画面を作る
    def make_title(self):
        #ウィンドウサイズと同じ画像を作る
        self.create_picture(0,0,"title",(700,800))
        self.create_button(200,500,"start",(260,80))
        self.create_button(200,600,"score",(260,80))
        #描画順を調整する
        self.sort_visual_order()
    
    def make_game_play(self):
        self.bar = Bar(10,600,"bar",(300,300),10,5)
        self.ball = Ball(10,10,"ball",(300,300),0,0)
        self.visibles.append(self.bar)
        self.visibles.append(self.ball)

    #描画する順番を調整する
    def sort_visual_order(self):
        for e in self.visibles:
            #背景の要素を最初に描画するようにする
            if e.name == "title":
                self.visibles.remove(e)
                temp = self.visibles[0]
                self.visibles[0] = e
                self.visibles.append(temp)

    '''
    ページ切り替えの関数を作ってもいいかも。
    プレイ画面からクリア画面へ行こうとしたら。
    クリアしたら、現在のvisiblesを全部removeして、
    クリア画面に必要なvisibleを作ってしまうような関数。
    '''

    #おそらく、毎秒呼び出すような。そんな感じの処理をまとめる。
    def update(self):

        #サンプルコードを参考にしている。何をしているかはわからない。
        for v in self.visibles[:]:
            #viewに書くべきオブジェクトを通知する
            self.view.draw(v)

            #ここにボールに関する、毎回実行した方が良いようなものをまとめおく
            if v.get_name() == "ball":
                #self.interact_bar_ball()
                #self.interact_block_ball()
                #self.interact_wall_ball()
                a = 1 #テストで書いているだけ
            
            #ここにアイテムに関する、毎回実行した方が良さそうなものをまとめておく
            if v.get_name() == "item":
                self.interact_bar_item(v)

            if v.is_appear == False:
                self.visibles.remove(v)
            



            
        

    

