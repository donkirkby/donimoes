# Moonside: Mining Puzzles with Dominoes #
Domino puzzles where you collect explosive moonstones.

Download [the PDF][pdf] if you want to print out pretty diagrams of the puzzles.

Each puzzle is a pattern of dominoes for you to start from. The different
numbers on the dominoes are different kinds of moonstones, and the goal is to
collect all the dominoes by sliding matching numbers next to each other. There
are two safe ways a domino can move.

[pdf]: http://donkirkby.github.com/moonside.pdf

### Matching ###
Move a domino one space along its long axis so that it ends up with at least
one of its numbers matching an adjacent number on a neighbouring domino. Then
collect the domino you moved and any dominoes that match it, by removing them
from the pattern. In this example, the threes match, so you collect both
dominoes and solve the puzzle.

    2|3     2|3       2*3
    
    3|4       3>4       3*4

### Adding ###
Move a domino one space along its long axis so that it ends up with at least
one of its numbers next to an adjacent number that adds up to six. With an
adding move, no dominoes are removed. In this example, the two adds up with the
four above it to make six. After the second move, the twos match, so you
collect both dominoes and solve the puzzle.

    2|4     2|4       2|4     2*4
    
    2|6       2>6     2<6     2*6

Sometimes, you can collect more than two dominoes at once. In the first
example, the two matches twos on both of the other dominoes, and you collect
all three dominoes. In the second example, the two matches the two to the left,
and the four matches the four above it. You collect all three dominoes.

    5 2|4   5 2|4     5 2|4   5 2*4
    -       -         -       *
    2 2|6   2   2>6   2 2<6   2 2*6
    
    
    
    5 3|4   5 3|4     5 3|4   5 3*4
    -       -         -       *
    2 2|4   2   2>4   2 2<4   2 2*4

There are two restrictions on domino movement to keep your moonstone mine safe:

1. Keep the mine connected so it doesn't collapse. All the dominoes must be in
    one connected group, you can't split the group after moving or after
    removing the matching dominoes.
2. Use small explosions to avoid a chain reaction. The only way to move a
    domino is by matching numbers or adding to six. Matching numbers create a
    small explosion, and adding to six stabilizes the unmatched numbers. Any
    other type of movement will blow up your mine. If the moved domino matches
    any neighbouring numbers, you must collect it, as well as
    any neighbours that matched it. If there are no matching numbers, there
    must be at least one pair of neighbouring numbers that add up to six, but
    you don't have to make all the pairs of neighbouring numbers add up.

## Problems ##
Here are the starting positions for several Domiculture problems. The solutions
are listed at the end.

### Problem 1 ###
    6|6 1 0
        - -
    4|5 5 6

### Problem 2 ###
    0|5 0 1
        - -
    4|6 4 5
    
    4|2 4|1


### Problem 3 ###
    0 6 2|0
    - -
    5 5 5|3
    
    4 1|5 0
    -     -
    3 4|1 3

### Problem 4 ###
    6|0 1|5
    
    4|0 1 0
        - -
    2|1 6 3
    
    2|6 1|0

### Problem 5 ###
    0|4 0 0|3
        -
    6|4 2 4|1
    
    3|2 2|4 0
            -
    3|6 2|6 6

### Problem 6 ###
    3|0 2 1 6 2
        - - - -
    3|5 4 4 6 1
    
    2 1 1|0 6|0
    - -
    0 5 2|5 3|1

### Problem 7 ###
    1|5 6|5 0|6
    
    1|3 2|5 0 4
            - -
    1|0 1|4 3 2
    
    1|2 6|3 5|0
    
    6|6 2|0 2|2

### Problem 8 ###
    5|3 0|4 0|2
    
    5 4|2 1 5|2
    -     -
    4 1|1 5 4 1
            - -
    0|5 4|6 4 6
    
    3|1 5|6 0|6
    
    3|0 3|6 4|1

## Other Domino Puzzles ##
The only other domino puzzle I could find is called either Dominosa or Domino
Solitaire. You are provided a grid of numbers, and you have to lay the dominoes
on them. It was invented by O.S. Adler in 1874. There's an
[interesting proof][proof] that this puzzle is NP-hard.

Reiner Knizia published some puzzles called [Domino Knobelspass][knizia]
that are very similar to Dominosa.

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass

## Solutions ##
Here are the solutions. For each step, move the listed domino left, right, up,
or down. Then make captures for any matching numbers.

1. 15D, 66R, 06U, 15U
2. 42L, 41L, 15D, 15D, 04D, 05R, 42R, 05R
3. 43D, 05D, 05U, 53L, 03U, 53R
4. 40L, 21L, 26L, 10L, 40R, 15L, 03D, 15R, 03D
5. 02U, 06D, 06U, 24R, 41R, 64R, 32R, 32L, 64L, 02D
6. 14U, 24U, 35R, 35L, 15U, 25L, 20D, 15D, 60L, 21D, 60R
7. 15L, 15R, 25L, 25R, 06L, 06R, 14R, 10R, 10L, 63L, 50L, 42D, 20R
8. 52R, 52L, 06R, 56R, 31R, 31L, 56L, 05R, 54D, 54U, 04L, 04L, 15D, 44D, 06L

Moonside is an original puzzle designed by Don Kirkby, and an anagram of
"dominoes".
