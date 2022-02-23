#
# Wordle harness file.
# Use this to bootstrap your solution.
#

from typing import Any, Dict, Optional


def wordle_init(context: Dict[str, Any]):
    """Called once to initialize solver.

    `context` will contain a member `dictionary`, containing a dictionary
    of all possible English words that can be used in the puzzle.

    Args:
        context: Context passed from wordle puzzle runner.

    Returns:
        Number of iterations of solutions to be preformed on the same word
    """
    return 1


def wordle_begin(context: Dict[str, Any], iteration: int):
    """Called at the beginning of each new wordle puzzle.

    This can be used to initialize or reset any state attached to the context.

    Args:
        context: Context passed from wordle puzzle runner.
        iteration: The iteration number for this puzzle
    """
    pass


def wordle_guess(
    context: Dict[str, Any], guess_num: int, last_guess: Optional[str]) -> str:
    """Called by game to request a guess.

    Args:
        context: Context passed from wordle puzzle runner.
        guess_num: Current guess number (out of 6).
        last_guess: Response to the last guess (None if guess number is 1).

    Returns:
        Solver's guess word. Must be a 5 letter word present in the game
        dictionary.
    """
    return "hello"
