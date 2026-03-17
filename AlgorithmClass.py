"""Класс алгоритма для запоминания статистики побед/поражений"""
class Algorythm:

    def __init__(self):
        self.previousPredict = ''
        self.lastWinElement = ''
        self.gamesCounter = 0
        self.tieStreak = False
        self.win_lose = {
            'Wins' : 0,
            'Lose' : 0
        }

    def check_win(self, last_element, pred):
        """Функция для определения победы или поражения алгоритма"""

        self.lastWinElement = last_element
        self.gamesCounter+=1
        if self.previousPredict == self.lastWinElement:
            self.win_lose['Wins'] += 1
            self.previousPredict = pred
            self.lastWinElement = ''
            return True
        else:
            self.win_lose['Lose'] += 1
            self.previousPredict = pred
            self.lastWinElement = ''
            return False

    def calculate_tie(self):
        """Функция для расчёта ничьи"""

        self.tieStreak = True
        self.win_lose['Lose'] += 1
        self.gamesCounter += 1
        self.previousPredict = ''
        self.lastWinElement = ''


    def check_first_turn(self, pred):
        """Функция для проверки на первый ход алгоритма, или ход после ничьи"""
        if self.previousPredict == '':
            self.previousPredict = pred
            return True
        else:
            return False

    def print_stat(self):
        """Функция для получения текущей статистики алгоритма"""

        import logging
        logger = logging.getLogger(__name__)

        temp_s = f'|  Количество игр: {self.gamesCounter}  |  Победы: {self.win_lose['Wins']}  |  Пройгрыши: {self.win_lose['Lose']}  |'
        logger.info('='*len(temp_s))
        logger.info(temp_s)
        logger.info('='*len(temp_s))