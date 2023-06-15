#!/usr/bin/env python3

import argparse
import random
import sys
import time

from solution.wordle_harness import wordle_init, wordle_begin, wordle_guess
from statistics import mean
from typing import Any, Dict, List


rounds: int = 6

solver_context: Dict[str, Any] = {}
stats: Dict[str, Any] = {}
verbose: bool = False
wordle_candidates: List[str] = []


def load_words():
    with open("dictionary.txt", "r") as dict_file:
        for word in dict_file.readlines():
            wordle_candidates.append(word.strip())


def error(message: str, guess: str):
    print(message)
    print(f"(your guess was {guess})")
    stats["crit_failures"] += 1


def log(message: str):
    if verbose:
        print(message)


def success(word: str, n: int):
    log(f"You successfully guessed the word {word} in {n} tries!")
    # Running average.
    stats["tries_avg"] = \
        (stats["tries_avg"] * (stats["games"] - 1) + n) / stats["games"]


def failure(word: str):
    log(f"You failed to guess the word {word}.")
    stats["failures"] += 1


def play_game(game_num: int):
    wordle = random.choice(wordle_candidates)
    
    log(f"Wordle {game_num}")
    stats["games"] += 1

    wordle_begin(solver_context)

    output = ""

    for round_num in range(rounds):
        log(f"Guess ({round_num + 1}/{rounds})? ")

        guess = wordle_guess(
            solver_context, round_num, None if round_num == 0 else output)

        guess = guess.lower().strip()
        if len(guess) != 5 or not guess.isalpha():
            error(f"Guess must be five letter sequence", guess)
            return

        if guess not in wordle_candidates:
            error("Guess must be a valid english word", guess)
            return

        log(guess)

        output = ""
        for w, g in zip(wordle, guess):
            if w == g:
                output += "o"
            elif g in wordle:
                output += "_"
            else:
                output += "x"

        if output != "ooooo":
            log(output)
        else:
            success(wordle, round_num + 1)
            return

    failure(wordle)



def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-n]",
        description="Play a wordle game.",
        add_help=False
    )
    parser.add_argument(
        "-h", "--help", action="store_true", help="Display this help message"
    )
    parser.add_argument(
        "-n", "--num-rounds", dest="num_rounds", metavar="N", type=int,
        nargs=1, help="Number of rounds to play", default=[1]
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true",
        help="Print verbose output", default=False
    )
    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    options = {
        "games": args.num_rounds[0],
        "verbose": args.verbose,
    }
    return options


def print_stats():
    
    init_time = (stats["game_start"] - stats["init_start"]) * 1000
    game_time = (stats["game_end"] - stats["game_start"])
    num_games = stats["games"]
    num_failures = stats["failures"]
    num_crits = stats["crit_failures"]

    tries_avg = stats["tries_avg"]
    failure_pct = float(num_failures) / num_games
    crit_pct = float(num_crits) / num_games

    if verbose:
        print()

    print(f"Games: {num_games}")
    print(f"Average Num Guesses: {tries_avg}")
    print(f"Failures: {num_failures} ({failure_pct * 100:.3f}%)")
    print(f"Errors: {num_crits} ({crit_pct * 100:.3f}%)")
    print(f"Init time: {init_time:0.3f}ms")
    print(f"Game time: {game_time:0.3f}s")
    print(f"Average round time: {game_time / num_games * 1000:.3f}ms / round")


def main():
    global solver_context
    global stats
    global verbose

    options = parse_args()
    load_words()

    solver_context = {
        "dictionary": wordle_candidates,
    }
    stats = {
        "init_start": 0,
        "game_start": 0,
        "game_end": 0,
        "games": 0,
        "failures": 0,
        "crit_failures": 0,
        "tries_avg": 0,
    }

    stats["init_start"] = time.perf_counter()
    wordle_init(solver_context)
    

    stats["game_start"] = time.perf_counter()
    verbose = options["verbose"]
    for i in range(options["games"]):
        play_game(i + 1)
    stats["game_end"] = time.perf_counter()

    print_stats()


if __name__ == "__main__":
    main()
