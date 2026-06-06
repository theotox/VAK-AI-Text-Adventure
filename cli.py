#!/usr/bin/env python3
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vak import Game
from vak.state import load_game, list_slots


def main():
    parser = argparse.ArgumentParser(description="VAK-NODE-7 terminal")
    parser.add_argument("--load", metavar="SLOT", help="Load a saved game")
    parser.add_argument("--list", action="store_true", help="List saved games")
    args = parser.parse_args()

    if args.list:
        slots = list_slots()
        if slots:
            print("Saved games:")
            for s in slots:
                print(f"  {s}")
        else:
            print("No saved games.")
        return

    if args.load:
        nstate, nfs = load_game(args.load)
        if nstate is None:
            print(f"No saved game in slot '{args.load}'.")
            return
        game = Game(state=nstate, fs=nfs)
    else:
        game = Game()

    game.run()


if __name__ == "__main__":
    main()
