---
title: New Rules for Donimoes
---
# Experiments in Progress
These are new puzzles that aren't finished yet. You can try them out and let me
know what you think.

* **Mirror Donimoes** is a puzzle I designed where pawns walk around on top of
    the dominoes. (1 player, double-six dominoes, 4 pawns)
* **Adding Donimoes** is a puzzle I designed where you add dominoes in the given
    order. (1 player, double-six dominoes)

## Mirror Donimoes
Help four ghosts find each other in a haunted house. Each domino is a room in
the house, and the ghosts can't go through the closed doors. They can go through
the mirrors, though. Spooky!

### Goal
Move all the pawns into one connected group. Diagonal connections don't count.

### Start
Place the dominoes in the starting position shown in the problem, then put a
pawn on top of each corner space.

### Moves
There are two possible moves for each turn: a domino move or a pawn move.

#### Domino Moves
The house is so spooky, the rooms can move. If a domino has one or two pawns on
it, you can slide the domino one space along its long axis. The dominoes go
along for the ride. You can only move one domino at a time, and all the dominoes
must stay connected in one group before and after the move. Diagonal connections
don't count.

Remember, a domino with no pawns on it cannot move.

#### Pawn Moves
The ghosts can always move around the room, and they can move through mirrors to
the room next door. You can move a pawn one space up, down, or sideways, with a
few restrictions.

* Two pawns can't be on the same space, but you can have a pawn at each end
    of a domino.
* Moving to a neighbouring domino is only allowed if the number you move to
    matches the number you were on. (There's a mirror for the ghost to go
    through.)
* Pawns have to stay on top of the dominoes - no leaving the house.
* Diagonal moves are not allowed.

### Example
    1 0 2
    - - -
    1 2 1

### Problems
Here are the starting positions for several Mirror Donimoes problems. The
solutions are listed at the end.

#### Problem 1
    2 0 2|2
    - -
    0 3 1 1
        - -
    3|3 1 0

#### Problem 2
    3 0|2 1
    -     -
    3 2|3 1
    
    2|1 0|3

#### Problem 3
    4 3|3 3 0
    -     - -
    2 0|0 0 1
    
    2|2 3 2|1
        -
    1|4 4 0|2

#### Problem 4
    1|4 3|1 2
            -
    4 2 0|3 1
    - -
    0 2 2|4 3
            -
    0|0 0|2 3

#### Problem 5
    2 3 5 0|0 5
    - - -     -
    0 0 0 4|3 1
    
    3|3 5|5 2|5
    
    3|5 2|4 2|2
    
    0|1 1|2 1|3

#### Problem 6
    5|5 1 1|2 3
        -     -
    1 1 5 0 4 2
    - -   - -
    4 1 5 3 0 5
        -     -
    2|0 0 4|4 4
    
    4|2 2|5 1|3

#### Problem 7
    4|4 0|3 0 2
            - -
    3|5 5 5 4 2
        - -
    1 2 5 2 2|4
    - -
    1 3 5 1|0 4
        -     -
    0|5 4 2|1 3

#### Problem 8
    4 2 4 2 5|5
    - - - -
    2 1 1 5 1|1
    
    4|5 0|5 4|4
    
    0|4 3 0|1 3
        -     -
    0|2 2 0|0 0

#### Problem 9
    0 1|3 1|1 3
    -         -
    0 0|3 1|4 3
    
    3|5 4|5 0|1
    
    0|2 2|5 1|2
    
    0|5 2|4 1|5

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
Here are the starting positions for several Adding Donimoes problems. The
solutions are listed at the end.

#### Problem 1
    2 3 5 4 5 2
    - - - - - -
    1 5 1 5 5 4

# Solutions
## Mirror Donimoes Solutions
To distinguish the four different pawns in each solution, the top left is
labelled as a (P)awn, the bottom left is a k(N)ight, the top right is a
(B)ishop, and the bottom right is a (R)ook. Each pawn move has two letters and
each domino move has three letters.

* The first letter identifies the pawn that will move or one of the pawns on the
    domino that will move.
* For a domino move, the second letter is "D" for (D)omino.
* The last letter shows the direction: (L)eft, (R)ight, (U)p, or (D)own.

Here are the Mirror Donimoes solutions:

1. NR, NU, NDU, BL, RU, RL
2. NDL, RDL, PDU, BDD, PD, RU, RDL, RDL, NU, NDR, NDR, PDD

## Adding Donimoes Solutions
Here are the solutions to the Adding Donimoes problems. For each step, move the
listed domino left, right, up, or down. Adding moves contain the domino
numbers, (H)orizontal or (V)ertical direction, and the position to place it.
The top left corner is 11, one space to the right is 21, and one space below is 12.

1. 36D, 23V21, 33D, 53V32, 25H21, 36D, 23D, 22H13, 33D, 53D, 22R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/
