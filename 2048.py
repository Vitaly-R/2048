from Game import Game
import sys


def main():
    size = 4
    if 1 < len(sys.argv):
        if sys.argv[1].isdigit():
            size = int(sys.argv[1])
    game = Game(size)
    game.run()


if __name__ == '__main__':
    main()
