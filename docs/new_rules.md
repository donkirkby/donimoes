---
title: New Rules for Donimoes
---
# Experiments in Progress
These are new puzzles that aren't finished yet. You can try them out and let me
know what you think.

* **Partner Donimoes** is a puzzle I designed where chess pieces walk around on
    top of the dominoes. (1 player, double-six dominoes, 4 pawns)
* **Adding Donimoes** is a puzzle I designed where you add dominoes in the given
    order. (1 player, double-six dominoes)

## Partner Donimoes

### Goal
Move all the pawns into one connected group. Diagonal connection don't count.

### Start
Place the dominoes in the starting position shown in the problem, then put a
pawn on top of each corner space.

### Moves
There are two possible moves for each turn:

1. Domino move - if a domino has a pawn on it, you can slide the domino one
    space along its long axis. The domino goes along for the ride. You can only
    move one domino at a time, and all the dominoes must stay connected in one
    group before and after the move. Diagonal connections don't count.
2. Pawn move - you can move a pawn one space up, down, or sideways, with a few
    restrictions.
    * Moving to the other end of the same domino is allowed.
    * The number at the other end of a pawn's domino is the pawn's partner. The
        pawn's partner before the move must match the pawn's partner after the
        move.
    * A domino cannot have two pawns on it.
    * Diagonal moves are not allowed.

### Problems
#### Problem 1
    2|3 0|3
    
    2 2|2 0
    -     -
    0 1|3 1

## Adding Donimoes
The idea was to avoid the slow setup phase at the start of the other puzzles.

### Goal
The goal is to add all the dominoes from the queue onto the board. Each problem
shows the queue of dominoes to add, from left to right.

### Start
Take the two dominoes from the left end of the queue and place them on the board
in the same position relative to each other.

For example, if this is the queue:

    2 3 5
    - - -
    1 5 1

Then the start position is like this:

    2 3
    - -
    1 5

Not like this:

    2 5
    - -
    1 3

### Moves
There are only two ways a domino can move.

#### Adding
The next domino from the queue can be added to the board if it matches at least
two of the adjacent numbers on neighbouring dominoes. Those two adjacent
numbers can match the two ends of the domino, or both match one end.

In this example, the 13 can be added, because it matches the 1 below and the 3
below.

    1+3
    
    1 3
    - -
    5 5

In this example, the 52 can be added, because it matches the 5 beside and the 5
above. The 52 could also be added in the vertical position.

      3
      -
    1 5
    -
    5 5+2

#### Sliding
Move a domino one space along its long axis so that it ends up with at least
one of its numbers next to an adjacent number that adds up to six, or it
matches at least two of the adjacent numbers on neighbouring dominoes.

In this example, the left domino can move down, because the 1 and the 5 add to
six.

    1|3
    
      3
      -
    1 5
    v
    5

The left domino can move back up, because the 1 matches the 1 above, and the 5
matches the 5 to the right.

    1|3
    
    1 3
    ^ -
    5 5

#### Stay Connected
All the dominoes on the board must stay in one connected group, you can't split the group
after moving a domino.

### Problems
Here are the starting positions for several Capturing Donimoes problems. The
solutions are listed at the end.

#### Problem 1
    2 3 5 4 5 2
    - - - - - -
    1 5 1 5 5 4

# Solutions
## Partner Donimoes Solutions
Here are the solutions to the Partner Donimoes problems.

1. BDR, NDR, PDU, PR, PR, NR, RU, BL

## Adding Donimoes Solutions
Here are the solutions to the Adding Donimoes problems. For each step, move the
listed domino left, right, up, or down. Adding moves contain the domino
numbers, (H)orizontal or (V)ertical direction, and the position to place it.
The top left corner is 11, one space to the right is 21, and one space below is 12.

1. 36D, 23V21, 33D, 53V32, 25H21, 36D, 23D, 22H13, 33D, 53D, 22R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/
