"""
    常量文件
"""
import os
import pygame

# 项目的根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件的目录
ASSETS_DTR = os.path.join(BASE_DIR, "assets")

# 背景图片
BG_IMG = os.path.join(ASSETS_DTR, "images/background.png")
# 结束背景图片
BG_IMG_OVER = os.path.join(ASSETS_DTR, "images/game_over.png")

# 背景音乐
BG_MUSIC = os.path.join(ASSETS_DTR, "musics/game_bg_music.wav")

# 游戏分数文字颜色
TEXT_SCORE_COLOR = pygame.Color(255, 255, 0)
# 击中小型敌机10分
SCORE_SHOOT_SMALL = 10
# 游戏分数文件路径
SCORE_FILE = os.path.join(BASE_DIR, 'store/score.txt')

# 游戏标题
GAME_TITLE = os.path.join(ASSETS_DTR, "images/game_title.png")
# 开始游戏的按钮
START_BTN = os.path.join(ASSETS_DTR, "images/game_start.png")

# 我方飞机的静态资源 OurPlane类内引入
OUR_PLANE_IMG_LIST = [
    os.path.join(ASSETS_DTR, "images/hero1.png"),
    os.path.join(ASSETS_DTR, "images/hero2.png"),
]

# 飞机坠毁的静态资源 在我方飞机类引入
OUR_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DTR, "images/hero_broken_n1.png"),
    os.path.join(ASSETS_DTR, "images/hero_broken_n2.png"),
    os.path.join(ASSETS_DTR, "images/hero_broken_n3.png"),
    os.path.join(ASSETS_DTR, "images/hero_broken_n4.png"),
]

# 子弹的图片
BULLET_IMG = os.path.join(ASSETS_DTR, "images/bullet1.png")
# 子弹发射的声音
BULLET_SHOOT_MUSIC = os.path.join(ASSETS_DTR, "musics/bullet.wav")

# 敌方小型飞机图片
SMALL_ENEMY_PLANE_IMG_LIST = [os.path.join(ASSETS_DTR, "images/enemy1.png")]
# 敌方小型飞机坠毁的图片列表
SMALL_ENEMY_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DTR, "images/enemy1_down1.png"),
    os.path.join(ASSETS_DTR, "images/enemy1_down2.png"),
    os.path.join(ASSETS_DTR, "images/enemy1_down3.png"),
    os.path.join(ASSETS_DTR, "images/enemy1_down4.png")
]
# 小型飞机坠毁时的音乐
SMALL_ENEMY_DOWN_MUSIC = os.path.join(ASSETS_DTR, "musics/enemy1_down.wav")
