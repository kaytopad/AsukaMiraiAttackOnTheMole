#ライブラリーのインポート
import pygame as pg
import random
#ゲームの初期化
pg.init()
WIDTH, HEIGHT = 980, 650
mole_size = 80
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("進撃のモグラ")
#画像の読み込み
backgrand = pg.image.load("img/background.png")
backgrand = pg.transform.scale(backgrand, (WIDTH, HEIGHT))

mole_image = pg.image.load("img/mole.png")
mole_image = pg.transform.scale(mole_image, (mole_size, mole_size))

mole_hit_image = pg.image.load("img/mole_hit.png")
mole_hit_image = pg.transform.scale(mole_hit_image, (mole_size, mole_size))

current_mole_image = mole_image

mole_rect = current_mole_image.get_rect()
mole_rect.topleft = (random.randint(0, WIDTH - mole_size), random.randint(0, HEIGHT - mole_size))

#サウンド
hit_sound = pg.mixer.Sound("sound/中パンチ.mp3")
pg.mixer.music.load("sound/maou_bgm_8bit25.mp3")
pg.mixer.music.play(-1)  # BGMのループ再生

#色・フォントの設定
font = pg.font.SysFont(None, 36)
BLACK = (0, 0, 0)
score = 0

#タイマーイベント
mole_timer = pg.USEREVENT + 1
mole_interval = 1000  # モグラが出現する間隔（ミリ秒）
pg.time.set_timer(mole_timer, mole_interval)

##叩かれてからの表示時間
hit_timer = pg.USEREVENT + 2
hit_display_time = 200  # モグラが叩かれた後の表示時間（ミリ秒）

#各種フラグ
mouse_push = pg.USEREVENT + 3
pushFlag = False  # モグラが叩かれたかどうかのフラグ
running = True  # ゲームの実行フラグ

#フレームレート設定
clock = pg.time.Clock()
FPS = 60  # フレームレート

#ゲームのループ
while running:
    #イベントの設定
    screen.blit(backgrand, (0, 0))  # 背景の描画
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if mole_rect.collidepoint(event.pos) and not pushFlag:
            ##ここにモグラ叩いた時のポイントを加算する処理を入れてみよう
                
                current_mole_image = mole_hit_image
                hit_sound.play()
                pushFlag = True
                pg.time.set_timer(hit_timer, hit_display_time,loops= 1)
            ##スピードアップをしてみよう

            pg.time.set_timer(mole_timer,mole_interval,loops=0)
        elif event.type == mole_timer and not pushFlag:
            current_mole_image = mole_image
            mole_rect.topleft = (random.randint(0, WIDTH - mole_size), random.randint(0, HEIGHT - mole_size))
        elif event.type == hit_timer:
            current_mole_image = mole_image
            pushFlag = False
            mole_rect.topleft = (random.randint(0, WIDTH - mole_size), random.randint(0, HEIGHT - mole_size))   
        #スコアに応じて中ボスの出現
    #スコア・モグラの描画
    screen.blit(current_mole_image, mole_rect)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pg.display.flip()
    clock.tick(FPS)

#ゲームの終了処理
pg.quit()