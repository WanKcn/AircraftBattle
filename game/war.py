"""
    飞机大战实现，主要功能类
"""
import pygame
import sys

import constants
from game.plane import OurPlane, SmallEnemyPlane
from store.result import PlayRest


class PlaneWar(object):
    """飞机大战，优化main函数入口"""

    # 游戏状态
    # 游戏准备中，游戏中，结束 0，1，2表示
    READY = 0  # 游戏准备中
    PLAYING = 1  # 正在游戏当中
    OVER = 2  # 游戏结束

    status = READY  # 默认游戏状态

    # 加入我方飞机 开始指定为None
    our_plane = None

    frame = 0  # 播放的帧数
    clock = pygame.time.Clock()

    # 一架飞机可以属于多个精灵组
    # 所有小型敌机是一个精灵组
    small_enemies = pygame.sprite.Group()
    # 所有敌机是一个精灵组
    enemies = pygame.sprite.Group()
    # 游戏结果
    rest = PlayRest()

    def __init__(self):
        # 初始化游戏
        pygame.init()

        # 设置游戏标题栏
        pygame.display.set_caption("飞机大战")
        # 游戏窗口大小
        self.width, self.height = 480, 852
        # 获取屏幕对象
        self.screen = pygame.display.set_mode((self.width, self.height))

        # 获取背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        # 游戏结束的背景
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)

        # 游戏开始标题
        self.game_title = pygame.image.load(constants.GAME_TITLE)
        self.game_title_rect = self.game_title.get_rect()
        # 获取游戏标题的宽度和高度
        t_width, t_height = self.game_title.get_size()
        self.game_title_rect.topleft = (int((self.width - t_width) / 2),
                                        int(self.height / 2 - t_height))

        # 开始按钮
        self.btn_start = pygame.image.load(constants.START_BTN)
        self.btn_start_rect = self.btn_start.get_rect()
        b_width, b_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - b_width) / 2),
                                       int(self.height / 2 + b_height))

        # 游戏文字对象
        self.score_font = pygame.font.SysFont('华文楷体', 40)
        # 加载背景音乐
        pygame.mixer.music.load(constants.BG_MUSIC)
        pygame.mixer.music.play(-1)  # 无限循环播放
        pygame.mixer.music.set_volume(0.2)  # 设置音量

        # 我方飞机对象
        self.our_plane = OurPlane(self.screen, speed=20)
        self.clock = pygame.time.Clock()

        # 上一次按的键盘上的某一个键，用来控制飞机
        # self.key_down = None

    def bind_event(self):
        """绑定事件"""
        # 监听事件
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击进入游戏
                # 游戏正在准备中，点击才能进入游戏
                if self.status == self.READY:
                    self.status = self.PLAYING
                elif self.status == self.OVER:
                    # 游戏结束以后点击继续开始
                    self.status = self.READY
                    # 点击继续开始以后递归调用run_game
                    # 需要再次添加飞机
                    self.add_small_enemies(6)
                    # 需要重置分数
                    self.rest.score = 0
                    self.run_game()
            elif event.type == pygame.KEYDOWN:
                # 键盘事件
                # self.key_down = event.key
                # 游戏正在进行中，才需要键盘控制 WASD四个键
                if self.status == self.PLAYING:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.our_plane.move_up()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.our_plane.move_left()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.our_plane.move_down()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.our_plane.move_right()
                    # 空格键发射子弹
                    elif event.key == pygame.K_SPACE:
                        self.our_plane.shoot()

    def add_small_enemies(self, num):
        """随机生成N架敌机"""
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 8)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        """游戏主循环"""
        while True:
            # 1.设置帧速率
            self.clock.tick(60)
            self.frame += 1  # 每循环一次，frame+1
            # 游戏一直运行，frame值可能一直变大 当frame大于60 重置为0
            if self.frame >= 60:
                self.frame = 0
            # 2.绑定事件
            self.bind_event()
            # 3.更新游戏的状态
            if self.status == self.READY:
                # 游戏正在准备中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 正在准备中的标题
                self.screen.blit(self.game_title, self.game_title_rect)
                # 开始按钮
                self.screen.blit(self.btn_start, self.btn_start_rect)
                # self.key_down = None  # 设置游戏结束以后重新开始不保留游戏状态
            elif self.status == self.PLAYING:
                # 表示游戏进行中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制飞机 调用绘制飞机的方法
                self.our_plane.update(self)
                # 绘制子弹
                self.our_plane.bullets.update(self)  # 子弹类传了war对象
                # 绘制敌方飞机
                self.small_enemies.update()

                # 游戏分数
                score_text = self.score_font.render(
                    'Score:{0}'.format(self.rest.score),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                # 不需要改变位置，直接放在左上角
                self.screen.blit(score_text, score_text.get_rect())

            elif self.status == self.OVER:
                # 游戏结束的状态
                # 游戏结束的背景
                self.screen.blit(self.bg_over, self.bg_over.get_rect())
                # 分数的统计
                # 1.绘制总分
                score_text = self.score_font.render(
                    '{0}'.format(self.rest.score),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                score_text_rect = score_text.get_rect()
                text_width, text_height = score_text.get_size()
                # 改变文字的位置
                score_text_rect.topleft = (
                    int((self.width - text_height) / 2),
                    int(self.height / 2)
                )
                self.screen.blit(score_text, score_text_rect)
                # 2.历史最高分
                score_history = self.score_font.render(
                    '{0}'.format(self.rest.get_max_score()),
                    False,
                    constants.TEXT_SCORE_COLOR
                )
                self.screen.blit(score_history, (150, 40))

            # 更新屏幕
            pygame.display.flip()
