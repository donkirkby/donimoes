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
Each turn, you can make a domino move or a pawn move.

#### Domino Moves
The house is so spooky, the rooms can move. If a domino has one or two pawns on
it, you can slide the domino one space along its long axis. The pawns go
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
Here's a small problem to start with. First, set up the dominoes as shown in the
starting position.

    1 0 2
    - - -
    1 2 1

Then put a pawn on each corner. You can use four identical pawns, but for this
example and the solutions at the end, we use a (P)awn, a (B)ishop, a k(N)ight,
and a (R)ook, so you can keep track of which is which. The small white dots show
you the number under the pawn.

    P 0 B
    - - -
    N 2 R
    ---
    N1R1P1B2

In this position, none of the numbers match their neighbours, so there are no
mirrors for the pawns to move between dominoes. However, the 2 under the
bishop could match the 2 in the middle, so the first move is to slide the
bishop's domino down.

    P 0 x
    - -
    N 2 B
        v
    x x R
    ---
    N1R1P1B2

Now that there's a mirror to move through, the bishop can move to the left.

    P 0 x
    - -
    N B 2
        -
    x x R
    ---
    N1R1P1B2

The last move is to join the ghosts into a single, connected group, and there
are two choices. We can just move the rook to the other end of its domino, or
we can slide the rook's domino back up, and the rook comes along for the ride.

    P 0 2
    - - ^
    N B R
    ---
    N1R1P1B2

### Problems
Here are the starting positions for several Mirror Donimoes problems. The
solutions are listed at the end.

#### Problem 1
    1|2 0|2
    
    1 0 0 1
    - - - -
    1 0 3 0

#### Problem 2
    0 1 2|3
    - -
    2 0 3 3
        - -
    1|3 0 3

#### Problem 3
    3 0|2 1
    -     -
    3 2|3 1
    
    2|1 0|3

#### Problem 4
    1|4 3|1 2
            -
    4 2 0|3 1
    - -
    0 2 2|4 3
            -
    0|0 0|2 3

#### Problem 5
    1|1 0 1|3
        -
    0 4 0 0|1
    - -
    4 4 2 3 3
        - - -
    4|2 0 3 2

#### Problem 6
    3|3 2|2 3
            -
    4 4 4 0 2
    - - - -
    4 3 0 0 1
            -
    1|1 0|2 0

#### Problem 7
    4 0|0 0|3
    -
    1 4 4|3 2
      -     -
    3 0 4|4 2
    -
    2 3|3 1|2

#### Problem 8
    2 2|3 0|2
    -
    1 0|3 4|4
    
    0|4 1|3 3
            -
    1|4 2|2 3

#### Problem 9
    0|0 1|2 1
            -
    1|3 3|3 0
    
    1|4 0|2 4
            -
    1|1 0|4 4

#### Problem 10
    2|3 1|1 3
            -
    4|4 0|0 3
    
    1 3 3|4 3
    - -     -
    0 0 1|2 1

#### Problem 11
    0|4 2|2 4
            -
    0 1 0|2 1
    - -
    0 0 1 3 3
        - - -
    2|3 1 3 0

#### Problem 12
    2 3 5 0|0 5
    - - -     -
    0 0 0 4|3 1
    
    3|3 5|5 2|5
    
    3|5 2|4 2|2
    
    0|1 1|2 1|3

#### Problem 13
    5|5 1 1|2 3
        -     -
    1 1 5 0 4 2
    - -   - -
    4 1 5 3 0 5
        -     -
    2|0 0 4|4 4
    
    4|2 2|5 1|3

#### Problem 14
    4 2 4 2 5|5
    - - - -
    2 1 1 5 1|1
    
    4|5 0|5 4|4
    
    0|4 3 0|1 3
        -     -
    0|2 2 0|0 0

#### Problem 15
    0 0 5 5 4 4 1
    - - - - - - -
    5 6 6 1 1 3 6
    
    5|3 3|6 6 2|6
            -
    2|4 4|4 6 0|2
    
    5|5 2|5 6 1|0
            -
    1|2 0|4 4 3|1

#### Problem 16
    5 3 3|6 0 5 3
    - -     - - -
    1 4 1|2 6 0 5
    
    1 6 4|2 5 6 2
    - -     - - -
    1 1 6 3 4 6 0
        - -
    4|6 2 3 0|0 5
                -
    0|4 2|2 6|5 2

#### Problem 17
    6 0 4 3 3 5 1
    - - - - - - -
    3 2 4 4 2 2 5
    
    6|4 0 4 0|1 2
        - -     -
    6|2 5 5 1|4 4
    
    6 6 1 1 1 3|3
    - - - - -
    0 6 6 1 2 0|3

#### Problem 18
    1 0 4 1 4 4|2 2
    - - - - -     -
    1 5 4 4 0 3|6 5
    
    3|1 0 4 3|3 6|5
        - -
    0|0 1 6 0|3 5|5
    
    3|5 5|1 6|2 2|2
    
    5 3 3 1 6 6 6 2
    - - - - - - - -
    4 4 2 2 6 1 0 0

#### Problem 19
    1|4 4|6 6|6 1|3
    
    4 3|4 1|5 4 6|1
    -         -
    2 0|0 6|3 5 5|6
    
    2|2 2|6 5|5 4|4
    
    2|3 3|0 0|4 2 0
                - -
    2|5 1|2 3|3 0 1
    
    5|3 0|6 5|0 1|1

#### Problem 20
    2|5 4 3 2|2 1|1
        - -
    4|6 0 0 6 0 3|6
            - -
    6 2 0 0 5 0 6|1
    - - - -
    6 3 5 6 4 2 2|1
            - -
    5|5 5|4 4 4 4|3
    
    3|1 1|0 0|2 2|6
    
    3|3 3|5 5|1 1|4

You'll need patience for this one. Did I go too far?

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
* For a domino move, the second letter is "d" for (d)omino.
* The last letter shows the direction: (L)eft, (R)ight, (U)p, or (D)own.
* If the move gets repeated, there's a number to show how many times.

For the small example given in the rules, the solution is BdD, BL, RdU.

Here are the Mirror Donimoes solutions:

1. PD, BL, BD, BdD, BL, RL
2. PD, BD, BL, BdD, BL, RL
3. NdL, PD, BD, RdL, RU, PdU, RdL2, NU, NdR2, PdD
4. PdL, PR, PD, BD, NR2, PD2, PR, NR, PR, RU, RdD, BdD
5. BdR, NU, NR, PR, NU, RU, BL, BD, RL, BdR, RdU2, RD, RdU, BdL, BL2, BdU
6. PdL, BdU, RdU, PR, NR, RL, BD, RL, RU, RL, RdU2, PR, PdD, BL, PdD, BdL, BL
7. NdD, PdD, PR, BL2, BdL2, PdU2, BR, BdD2, PR, PD, NU, NR2, RL
8. NR, NU, RU, RL, NdL, RdL, RU, PdU, RdL2, NL, NU, NdR2, PdD, PR2, BL
9. RdD, PR, RU, RL2, BD, RU, RR, RdR2, BD, BdL2, NU, BD, RdR, NdR, RdR, NdR, BR,
    BU, NdL, RdL, NdL, RdL, NU, NR, RL
10. RdD, NR, NU, NR, NdR2, RU, NR, RU, RdL2, RL, BD, NdR2, BD, BdL2, RD, BL, RL,
    BdD, NdL, BU, RdD, BdL, RU, NU, NL
11. NdL, RdD, BdD, NR, PD2, PR, PdD2, PU, PR, PdD, PU, PL, PdD, NdR, BD, PR,
    PdU, RU, RL, RU, RdD, RR, RdD, RL, RU, BdD
12. RdR, NR2, NdR, PD, PR2, PdU, PR, NR, NU, PR, NU, NdR, ND, NL, NdR, NU, RL,
    NdR, BdD, ND, NdR, BdD, RU, RdU, NdL, PdR, NdL
13. BdU, PR, BD, BL3, BdU, PR, PdD, PD, BD, PD, BD, PL, BD, PL, NdL, PD, NdR,
    PR, NR, RL, PR, NR
14. PdU, NR2, NdD, PD, PR, PD, PR, RL2, RU, RdL, NU, RU, BL, RR, RU, RdU, RU,
    BL, BdD, BD, RD, BL, RD, BD, RL
15. NR, PR, PD, PR, PU, PR, PD, PR, PU, PR, RL, BD2, BdR, PdD, BL, BD, BL, BdR,
    BD, BL, PdD, BdR, BD, PdD, RdR, PdD, RL, RdD, PL, RdU, BL, RU, BL, PL, BdD,
    RL, BU, PL, RL, BL
16. NdL, BdU, NR, NU, NdL, PD3, PR, PdD, BD, BL, BdU, BD, BL, BdU, BD, BL3, BdD,
    BD, BR, NR, BR, BU, BdR3, BD2, PdD, NR, PdU, NR, ND, PU, PR, ND, PD, NR, PD,
    RU, RdD, RL2, BdD, BL2
17. NU, NR, NdD, NR, NdD, NU, NR, NU, NR, NdD, NL, NdD, NU, NR, NdD, RdL, RU,
    RdL, RR, RD, NL, NU, NL, ND, NL, NdD, NU, NR, NdD, NU, NR, NdD, RdL, RU,
    RdL, RR, RD, RdL, RU, RdL, RR, RD, RdL, RL2, RU3, NdU, NR, NdU2, NU, NR2,
    NU, BdU, BD, NdU, NL2, NU, NL, ND2, BL, BD, BL, BU, BL, BD, BdU, BL, BdU2,
    ND, NL, NdU2, NU, NL, ND, RdL, NdD, ND, NdL, RD, RdR, NU2, RR, RU, RdU2, BD
18. RU2, RdR, RL, RD2, RL, RU, RL2, RU, RdR, RR2, RD2, RL, RU, RL2, RdU, BD3,
    BdR, BL, BU, BL, BU, BL, BD2, BdR, RdU, RL, NR, NU, NR, ND, NR, NU2, NL2,
    NdL, ND2, NR, NU, NR, ND, NR, NU2, NdL, RdD, RR, RdD, RU, RL, RdU, RU2, RL,
    RdU, NU, NdU, NL2, NdL, PD2, NdR, PR, PU, NR2, NdD, RdD, RR, RD2, BdL, BL
19. PdL, PR, PD5, PdL, NU, PdR, PU2, PR2, NL, NU2, NdL, PdL, PL, PD, PR3, NR,
    ND, NR, NdL, PdL, NR, NdR, PR, NdL, PdL, NL2, NU, NR, NU3, NL, PL4, PU, PR,
    PU3, NdR, PR4, NR4, BdR, NdR, PD, PR, NR, ND, NdR, ND, NL2, ND, NdL, PL,
    PdL, BL, BD, PdR, PD, PL2, PU, PdD, NR, NdD, PR2, NU, NR, BL, BD, RU2
20. NU, NR6, RL7, RU, RR4, NdR, RdR, NL, RdL, RL2, NdR, RdR, NL2, RdL, RL2, NdR,
    RdR, RD, RR5, NL3, ND, NR3, RdR2, NdR2, RL, NdL2, NL2, RdR2, NdR2, RL2,
    NdL2, NL2, RdR2, NdR2, RL2, NdL, NU, NR6, RL, RU, RR4, NdR2, RdR2, NL, RdL2,
    RL2, NdR2, RdR2, NL2, RdL2, RL2, NdR2, RdR, RD, RdR, RL, RU, RdR, RD, RR5,
    NL3, ND, NR3, RdR2, NdR2, RL, NdL2, NL2, RdR2, NdR2, RL2, NdL2, NL2, RdR2,
    NdR2, RL2, NdL, NU, NR6, RL, RU, RR4, NdR2, RdR2, NL, RdL2, RL2, NdR2, RdR2,
    NL2, RdL2, RL2, NdR2, RdR, RD, RdR, RL, RU, RdR, RD, RR5, NL3, ND, NR3, RdR,
    NdR, RL, NdL, NL2, RdR, NdR, RL2, NdL, NL2, RdR, NdR, NU, NR6, RL3, RU, RR4,
    NdR, RdR, NL, RdL, RL2, NdR, RdR, NL2, RdL, RL2, NdR, RdR, RD, RR5, NL3, ND,
    NR3, RdR, NdR, RL, NdL, NL2, RdR, NdR, RL2, NdL, NL2, RdR, NdR, NU, NR6,
    RL3, RU, RR4, NdR, RdR, NL, RdL, RL2, NdR, RdR, NL2, RdL, RL2, NdR, RdR, RU,
    RL5, RU3, NL3, NU, NL5, NU2, RdU, NdU, NR, ND, RD, RR, RdU2, NdU2, NL, ND,
    RD, RL, RdU2, NdU2, PR2, PdD3, RdD3, PD, PR3, PU, PR2, PU, PL, ND2, NR3, NU,
    NR2, NU, PdR, PU, NL, RD3, RR3, RU, RR2!

## Adding Donimoes Solutions
Here are the solutions to the Adding Donimoes problems. For each step, move the
listed domino left, right, up, or down. Adding moves contain the domino
numbers, (H)orizontal or (V)ertical direction, and the position to place it.
The top left corner is 11, one space to the right is 21, and one space below is 12.

1. 36D, 23V21, 33D, 53V32, 25H21, 36D, 23D, 22H13, 33D, 53D, 22R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/
