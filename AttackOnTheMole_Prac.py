# ライブラリーのインポート
import pygame as pg
import random

# ゲームの初期化
pg.init()

WIDTH, HEIGHT = 980, 650
MOLE_SIZE = 80

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("進撃のモグラ")

# --------------------------------
# 画面画像の読み込み
# --------------------------------

title_image = pg.image.load("img/titleimage.png")
title_image = pg.transform.scale(title_image, (WIDTH, HEIGHT))

result_image = pg.image.load("img/resultimage.png")
result_image = pg.transform.scale(result_image, (WIDTH, HEIGHT))

background = pg.image.load("img/background.png")
background = pg.transform.scale(background, (WIDTH, HEIGHT))

# --------------------------------
# モグラ画像の読み込み
# --------------------------------

mole_image = pg.image.load("img/mole.png")
mole_image = pg.transform.scale(mole_image, (MOLE_SIZE, MOLE_SIZE))

mole_hit_image = pg.image.load("img/mole_hit.png")
mole_hit_image = pg.transform.scale(mole_hit_image, (MOLE_SIZE, MOLE_SIZE))

current_mole_image = mole_image

mole_rect = mole_image.get_rect()

# --------------------------------
# サウンド
# --------------------------------

hit_sound = pg.mixer.Sound("sound/中パンチ.mp3")

pg.mixer.music.load("sound/maou_bgm_8bit25.mp3")
pg.mixer.music.play(-1)

# --------------------------------
# 色・フォントの設定
# --------------------------------

font = pg.font.SysFont(None, 36)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --------------------------------
# ゲームの状態
# --------------------------------

TITLE = 0
PLAY = 1
RESULT = 2

game_state = TITLE

# --------------------------------
# ゲームの設定
# --------------------------------

score = 0

GAME_TIME = 60  # 制限時間（秒）

MOLE_INTERVAL = 1000  # モグラの移動間隔（ミリ秒）
HIT_DISPLAY_TIME = 200  # 叩かれた画像の表示時間

pushFlag = False

# モグラの初期位置
def reset_mole():
    global current_mole_image, pushFlag

    current_mole_image = mole_image
    pushFlag = False

    mole_rect.topleft = (
        random.randint(0, WIDTH - MOLE_SIZE),
        random.randint(0, HEIGHT - MOLE_SIZE)
    )

# ゲーム開始時の初期化
def start_game():
    global score
    global game_start_time
    global last_mole_time

    score = 0

    game_start_time = pg.time.get_ticks()
    last_mole_time = game_start_time

    reset_mole()

# --------------------------------
# フレームレート設定
# --------------------------------

clock = pg.time.Clock()
FPS = 60

# --------------------------------
# ゲームループ
# --------------------------------

running = True

while running:

    current_time = pg.time.get_ticks()
    title_image = pg.image.load("img/titleimage.png")
    title_image = pg.transform.scale(title_image, (WIDTH, HEIGHT))

    # イベント処理
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        # --------------------------------
        # タイトル画面
        # --------------------------------

        elif game_state == TITLE:

            if event.type == pg.KEYDOWN:
                start_game()
                game_state = PLAY

        # --------------------------------
        # ゲーム画面
        # --------------------------------

        elif game_state == PLAY:

            if event.type == pg.MOUSEBUTTONDOWN:

                if mole_rect.collidepoint(event.pos) and not pushFlag:

                    # スコアを加算
                    score += 10

                    # モグラを叩いた画像に変更
                    current_mole_image = mole_hit_image

                    hit_sound.play()

                    pushFlag = True

                    # 叩かれた時間を記録
                    hit_time = current_time

        # --------------------------------
        # リザルト画面
        # --------------------------------

        elif game_state == RESULT:

            if event.type == pg.KEYDOWN:
                game_state = TITLE

    # --------------------------------
    # 画面描画・ゲーム処理
    # --------------------------------

    if game_state == TITLE:

        # タイトル画面の描画
        screen.blit(title_image, (0, 0))

        title_text = font.render(
            "Press Any Key to Start", True, WHITE
        )

        screen.blit(
            title_text,
            (WIDTH // 2 - title_text.get_width() // 2, HEIGHT - 80)
        )

    elif game_state == PLAY:

        # 背景の描画
        screen.blit(background, (0, 0))

        # --------------------------------
        # 制限時間の計算
        # --------------------------------

        elapsed_time = (current_time - game_start_time) / 1000

        remaining_time = max(0, GAME_TIME - int(elapsed_time))

        # 60秒経過したらリザルト画面へ
        if elapsed_time >= GAME_TIME:

            game_state = RESULT

        else:

            # --------------------------------
            # モグラの表示時間管理
            # --------------------------------

            if pushFlag:

                # 叩かれてから一定時間経過したら移動
                if current_time - hit_time >= HIT_DISPLAY_TIME:

                    reset_mole()
                    last_mole_time = current_time

            else:

                # 一定時間経過したらモグラを移動
                if current_time - last_mole_time >= MOLE_INTERVAL:

                    reset_mole()
                    last_mole_time = current_time

            # モグラの描画
            screen.blit(current_mole_image, mole_rect)

            # --------------------------------
            # スコアの描画
            # --------------------------------

            score_text = font.render(f"Score: {score}", True, BLACK)

            screen.blit(score_text, (10, 10))

            # --------------------------------
            # 残り時間の描画
            # --------------------------------

            time_text = font.render(
                f"Time: {remaining_time}", True, BLACK
            )

            screen.blit(time_text, (10, 50))

    elif game_state == RESULT:

        # リザルト画面の描画
        screen.blit(result_image, (0, 0))

        # 最終スコアの描画
        result_text = font.render(
            f"Final Score: {score}", True, WHITE
        )

        screen.blit(
            result_text,
            (
                WIDTH // 2 - result_text.get_width() // 2,
                HEIGHT // 2
            )
        )


        screen.blit(
            return_text,
            (
                WIDTH // 2 - return_text.get_width() // 2,
                HEIGHT - 80
            )
        )

    # 画面更新
    pg.display.flip()

    clock.tick(FPS)

# --------------------------------
# ゲーム終了処理
# --------------------------------

pg.quit()