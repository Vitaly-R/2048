from Game import Game
import sys


def main():
    size = int(sys.argv[1]) if 1 < len(sys.argv) and sys.argv[1].isdigit() else 4
    game = Game(size)
    game.run()


if __name__ == '__main__':
    main()
