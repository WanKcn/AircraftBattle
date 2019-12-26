"""
    用于分数统计
"""
import constants


class PlayRest(object):
    """玩家的结果"""
    __score = 0  # 总分

    @property
    def score(self):
        """单词游戏分数"""
        return self.__score

    @score.setter
    def score(self, value):
        """设置游戏分数"""
        if value < 0:
            return None
        self.__score = value

    def set_history(self):
        """记录最高分"""
        # 1. 读取文件中存储的分数
        # 2. 和新分数对比保存最大值
        # 3. 存储分数，替换文件 w模式
        if int(self.get_max_score()) < self.score:
            with open(constants.SCORE_FILE, 'w') as f:
                f.write('{0}'.format(self.score))

    def get_max_score(self):
        """读取文件中的历史最高分"""
        rest = 0
        with open(constants.SCORE_FILE, 'r') as f:
            temp = f.read()
            if temp:
                rest = temp
        return rest
