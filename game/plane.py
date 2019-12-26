"""
    飞机的基类
    1.我方飞机
    2.敌方飞机 (小型，中型，大型)
"""
import random

import pygame
import constants
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """
        飞机的基类
    """
    # list 用来保存飞机的图片
    plane_img = []
    # list 飞机爆炸的图片
    destroy_img = []
    # 飞机的状态 True 活的，False死的
    active = True
    # 飞机发射的子弹放在精灵组
    bullets = pygame.sprite.Group()
    # 坠毁的音乐地址
    down_music_src = None

    # 重写构造方法
    def __init__(self, screen, speed=None):
        super().__init__()
        # 需要拿到屏幕对象
        self.screen = screen
        # 加载的静态资源
        self.img_list = []
        self._destroy_list = []
        self.down_music = None
        self.load_src()

        # 飞机的速度 不传的时候默认为10
        # 在游戏中就是图片移动的速度
        self.speed = speed or 10

        # 获取飞机所在位置，取飞机的第一张图片
        self.rect = self.img_list[0].get_rect()

        # 获取飞机的高度和宽度
        self.plane_width, self.plane_height = self.img_list[0].get_size()
        # 得到游戏窗口的宽和高
        self.width, self.height = self.screen.get_size()

        # 改变飞机的初始化位置，放在屏幕的下方
        self.rect.left = int((self.width - self.plane_width) / 2)
        self.rect.top = int(self.height / 2)

    def load_src(self):
        """加载静态资源"""
        # 飞机图像
        for img in self.plane_img:
            self.img_list.append(pygame.image.load(img))
        # 飞机坠毁的图像
        for img in self.destroy_img:
            self._destroy_list.append(pygame.image.load(img))
        # 飞机坠毁的音乐
        if self.down_music_src:
            self.down_music = pygame.mixer.Sound(self.down_music_src)

    @property
    def image(self):
        return self.img_list[0]

    # 在当前类绘制飞机
    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """飞机向上移动"""
        self.rect.top -= self.speed  # y值变小，不断减去速度

    def move_down(self):
        """飞机向下移动"""
        self.rect.top += self.speed  # y值变大，不断加上速度

    def move_left(self):
        """飞机向左移动"""
        self.rect.left -= self.speed  # x值变小

    def move_right(self):
        """飞机向右移动"""
        self.rect.left += self.speed  # x值变大

    def broken_down(self):
        """飞机坠毁"""
        # 1.坠毁播放坠毁音乐
        if self.down_music:
            self.down_music.play()  # 只需要播放一次
        # 2.播放坠毁的动画
        for img in self._destroy_list:
            self.screen.blit(img, self.rect)
        # 3.坠毁后飞机的状态
        self.active = False

    def shoot(self):
        """飞机都可以发射子弹"""
        # 往精灵组内不断的添加子弹，然后再main()中改变精灵组的位置
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


class OurPlane(Plane):
    """我方的飞机"""
    # list 用来保存飞机的图片资源
    plane_img = constants.OUR_PLANE_IMG_LIST  # 放图片的地址，地址写在常量里
    # list 飞机爆炸的图片
    destroy_img = constants.OUR_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_music_src = None

    def update(self, war):
        """我方飞机的动画切换"""
        # self.move(war.key_down)
        # 1.飞机的动画效果，喷气式效果
        if war.frame % 5:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)
        # 2.飞机撞机的检测
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        if rest:
            # 1.撞机了，游戏结束 状态判断
            war.status = war.OVER
            # 2.游戏结束，敌方飞机消失 empty()移除精灵组
            war.enemies.empty()
            war.small_enemies.empty()
            # 3.我方飞机坠毁的效果
            self.broken_down()
            # 4.统计游戏分数

    def move(self, key):
        """飞机移动自动控制"""
        if key == pygame.K_w or key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.move_left()
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.move_right()

    # 重写的方法来控制我方飞机不能飞出边界
    def move_up(self):
        """向上移动，超出范围重置为0"""
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        """向下移动，超出范围归减去超出部分"""
        super().move_down()
        # 运动到最底下还需要减去飞机高度
        if self.rect.top >= self.height - self.plane_height:
            self.rect.top = self.height - self.plane_height

    def move_left(self):
        """向左移动，超出范围归0"""
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        """"向右移动，超出范围减去"""
        super().move_right()
        if self.rect.left >= self.width - self.plane_width:
            self.rect.left = self.width - self.plane_width


class SmallEnemyPlane(Plane):
    """敌方小型飞机类"""
    plane_img = constants.SMALL_ENEMY_PLANE_IMG_LIST
    # list 飞机爆炸的图片
    destroy_img = constants.SMALL_ENEMY_DESTROY_IMG_LIST
    # 坠毁的音乐地址
    down_music_src = constants.SMALL_ENEMY_DOWN_MUSIC

    def __init__(self, screen, speed):
        """敌方飞机从屏幕上方随机出现"""
        super().__init__(screen, speed)
        # 每次生成一架小型飞机的时候，随机出现在屏幕中
        # 改变飞机的随机位置
        self.init_pos()

    def init_pos(self):
        """提高代码复用,改变飞机的随机位置"""
        # 0到最右边的宽度减去飞机宽度 屏幕宽度-飞机宽度
        self.rect.left = random.randint(0, self.width - self.plane_width)
        # 屏幕之外飞机高度，后面随机摆五架飞机
        self.rect.top = random.randint(-5 * self.plane_height, -self.plane_height)

    def update(self, *args):
        """更新敌方飞机的移动"""
        super().move_down()
        # 画在屏幕上
        self.blit_me()
        # 超出范围，如何处理
        # 1.重用
        if self.rect.top >= self.height:
            self.active = False
            # self.kill()
            self.reset()
        # TODO 2.多线程、多进程

    def reset(self):
        """重置飞机的状态，达到复用的效果"""
        self.active = True
        self.init_pos()

    def broken_down(self):
        """重写爆炸效果"""
        super().broken_down()
        # 重置飞机状态
        self.reset()
