import pygame
import constants

""" 封装子弹 """


class Bullet(pygame.sprite.Sprite):
    """子弹类"""
    # 子弹状态 True:活着，False：死的 超出屏幕或者发生碰撞
    active = True

    def __init__(self, screen, plane, speed=None):
        super().__init__()
        self.screen = screen
        # 速度
        self.speed = speed or 10
        self.plane = plane

        # 加载子弹的图片
        self.img = pygame.image.load(constants.BULLET_IMG)

        # 改变子弹的位置
        self.rect = self.img.get_rect()
        self.rect.centerx = plane.rect.centerx  # 子弹中心等于飞机中心
        self.rect.top = plane.rect.top  # 子弹顶部等于飞机顶部

        # 发射的音乐效果
        self.shoot_music = pygame.mixer.Sound(constants.BULLET_SHOOT_MUSIC)
        # 设置子弹发射声音大小
        self.shoot_music.set_volume(0.3)
        # 发射出去其实就是创建一个新的子弹对象，直接播放
        self.shoot_music.play()

    def update(self, war):
        """更新改变子弹的位置,我方飞机的子弹一定是向上移动的"""
        self.rect.top -= self.speed
        # 超出屏幕范围后
        if self.rect.top < 0:
            self.remove(self.plane.bullets)
            # 验证精灵组超出范围移除
            # print(self.plane.bullets)
        # 绘制子弹
        self.screen.blit(self.img, self.rect)
        # 碰撞检测，检测子弹是否已经碰撞到了敌机 是一个列表
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        # 子弹打中
        for r in rest:
            # 1.子弹不能继续飞行
            self.kill()
            # 2.飞机坠毁效果
            r.broken_down()
            # 3.统计游戏成绩
            war.rest.score += constants.SCORE_SHOOT_SMALL
            # 保存历史记录
            war.rest.set_history()
