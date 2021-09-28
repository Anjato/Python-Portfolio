class Character:

    def __init__(self, name):
        self.name = name


class Human(Character):

    def printHMN(self):
        print('Hello human character,', self.name)


class CPU(Character):

    def printAI(self):
        print('Hello CPU character,', self.name)


h = Human('Nick.')
c = CPU('Robotron.')
h.printHMN()
c.printAI()
