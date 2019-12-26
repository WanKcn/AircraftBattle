"""
Title: AircraftBattle
Author:Wankcn<wankcn@icloud.com>
Created:2019-12-26
"""

from game.war import PlaneWar


def main():
    """ 游戏入口，main方法"""
    war = PlaneWar()
    # 添加小型敌机
    war.add_small_enemies(6)
    war.run_game()


if __name__ == '__main__':
    main()
