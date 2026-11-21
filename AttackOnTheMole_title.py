
# ==========================================
# ライブラリーのインポート
# ==========================================

import pygame as pg
import random
from pathlib import Path


# ==========================================
# ゲームの初期化
# ==========================================

pg.init()

WIDTH, HEIGHT = 980, 650
MOLE_SIZE = 80

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("進撃のモグラ")

# ファイルの場所を取得
BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# 画像の読み込み
# ==========================================

title_image = pg.image.load(
    str(BASE_DIR / "img" / "titleimage.png")
)
title_image = pg.transform.scale(
    title_image, (WIDTH, HEIGHT)
)

result_image = pg.image.load(
    str(BASE_DIR / "img" / "resultimage.png")
)
result_image = pg.transform.scale(
    result_image, (WIDTH, HEIGHT)
)

background = pg.image.load(
    str(BASE_DIR / "img" / "background.png")
)
background = pg.transform.scale(
    background, (WIDTH, HEIGHT)
)

mole_image = pg.image.load(
    str(BASE_DIR / "img" / "mole.png")
)
mole_image = pg.transform.scale(
    mole_image, (MOLE_SIZE, MOLE_SIZE)
)

mole_hit_image = pg.image.load(
    str(BASE_DIR / "img" / "mole_hit.png")
)
mole_hit_image = pg.transform.scale(
    mole_hit_image, (MOLE_SIZE, MOLE_SIZE)
)

current_mole_image = mole_image

mole_rect = mole_image.get_rect()


# ==========================================
# サウンド
# ==========================================

hit_sound = pg.mixer.Sound(
    str(BASE_DIR / "sound" / "中パンチ.mp3")
)

pg.mixer.music.load(str(BASE_DIR / "sound" / "maou_bgm_8bit25.mp3"))


# ==========================================
# 色・フォントの設定
# ==========================================

font = pg.font.SysFont(None, 36)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ==========================================
# ゲームの状態
# ==========================================

TITLE = 0
PLAY = 1
RESULT = 2

game_state = TITLE


# ==========================================
# ゲームの設定
# ==========================================

score = 0

GAME_TIME = 30

# モグラの出現間隔
MOLE_INTERVAL = 1000

# 最低出現間隔
MIN_MOLE_INTERVAL = 250

# モグラを叩いた画像の表示時間
HIT_DISPLAY_TIME = 200


# ==========================================
# イベントの設定
# ==========================================

# モグラ出現イベント
mole_timer = pg.USEREVENT + 1

# モグラを叩いた後のイベント
hit_timer = pg.USEREVENT + 2

# イベントタイマーを初期停止
pg.time.set_timer(mole_timer, 0)
pg.time.set_timer(hit_timer, 0)


# ==========================================
# フラグ
# ==========================================

pushFlag = False


# ==========================================
# モグラの位置を変更
# ==========================================

def reset_mole():

    global current_mole_image
    global pushFlag

    current_mole_image = mole_image
    pushFlag = False

    mole_rect.topleft = (
        random.randint(0, WIDTH - MOLE_SIZE),
        random.randint(0, HEIGHT - MOLE_SIZE)
    )


# ==========================================
# スピードアップ処理
# ==========================================

def update_mole_speed():

    global MOLE_INTERVAL
    
    if score >= 400:
        MOLE_INTERVAL = 250

    elif score >= 300:
        MOLE_INTERVAL = 400

    elif score >= 200:
        MOLE_INTERVAL = 600

    elif score >= 100:
        MOLE_INTERVAL = 800

    else:
        MOLE_INTERVAL = 1000

    # タイマーの間隔を変更
    pg.time.set_timer(mole_timer, MOLE_INTERVAL)


# ==========================================
# ゲーム開始時の初期化
# ==========================================

def start_game():

    global score
    global MOLE_INTERVAL
    global pushFlag
    global game_start_time

    # スコアを初期化
    score = 0

    pg.mixer.music.play(-1)
    # スピードを初期化
    MOLE_INTERVAL = 1000

    # フラグを初期化
    pushFlag = False

    # ゲーム開始時間を記録
    game_start_time = pg.time.get_ticks()

    # モグラの位置を初期化
    reset_mole()

    # イベントタイマーを開始
    pg.time.set_timer(mole_timer, MOLE_INTERVAL)


# ==========================================
# フレームレート設定
# ==========================================

clock = pg.time.Clock()
FPS = 60


# ==========================================
# ゲームループ
# ==========================================

running = True

while running:

    current_time = pg.time.get_ticks()

    # --------------------------------------
    # イベント処理
    # --------------------------------------

    for event in pg.event.get():

        if event.type == pg.QUIT:

            running = False

        # ==================================
        # タイトル画面
        # ==================================

        elif game_state == TITLE:

            if event.type == pg.KEYDOWN:

                start_game()
                game_state = PLAY

        # ==================================
        # ゲーム画面
        # ==================================

        elif game_state == PLAY:

            # モグラを叩いたとき
            if event.type == pg.MOUSEBUTTONDOWN:

                if (
                    event.button == 1
                    and mole_rect.collidepoint(event.pos)
                    and not pushFlag
                ):

                    # スコア加算
                    score += 10

                    # スピード更新
                    update_mole_speed()

                    # 叩かれた画像に変更
                    current_mole_image = mole_hit_image

                    hit_sound.play()

                    pushFlag = True

                    # 叩いた後の表示時間を設定
                    pg.time.set_timer(
                        hit_timer,
                        HIT_DISPLAY_TIME,
                        loops=1
                    )

            # モグラ出現イベント
            elif event.type == mole_timer:

                if not pushFlag:

                    reset_mole()

            # モグラを叩いた後のイベント
            elif event.type == hit_timer:

                reset_mole()

        # ==================================
        # リザルト画面
        # ==================================

        elif game_state == RESULT:
            pg.mixer.music.stop()
            if event.type == pg.KEYDOWN:

                game_state = TITLE

    # --------------------------------------
    # ゲーム画面の時間管理
    # --------------------------------------

    if game_state == PLAY:

        elapsed_time = (current_time - game_start_time) / 1000

        remaining_time = max(0,GAME_TIME - int(elapsed_time))

        # 30秒経過したらゲーム終了
        if elapsed_time >= GAME_TIME:

            # イベントタイマーを停止
            pg.time.set_timer(mole_timer, 0)
            pg.time.set_timer(hit_timer, 0)

            game_state = RESULT

    # --------------------------------------
    # 画面描画
    # --------------------------------------

    if game_state == TITLE:

        # タイトル画面
        screen.blit(title_image, (0, 0))

    elif game_state == PLAY:

        # 背景
        screen.blit(background, (0, 0))

        # モグラ
        screen.blit(current_mole_image, mole_rect)

        # スコア
        score_text = font.render(
            f"Score: {score}",
            True,
            BLACK
        )

        screen.blit(score_text, (10, 10))

        # 残り時間
        time_text = font.render(
            f"Time: {remaining_time}",
            True,
            BLACK
        )

        screen.blit(time_text, (10, 50))

    elif game_state == RESULT:

        # リザルト画面
        screen.blit(result_image, (0, 0))

        # 最終スコア
        result_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            result_text,
            (
                WIDTH // 2 - result_text.get_width() // 2,
                HEIGHT // 2
            )
        )


    # 画面更新
    pg.display.flip()

    clock.tick(FPS)


# ==========================================
# ゲーム終了処理
# ==========================================

pg.time.set_timer(mole_timer, 0)
pg.time.set_timer(hit_timer, 0)

pg.quit()
