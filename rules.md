# Moonside: Mining Puzzles with Dominoes #
Run a moonside mine, and collect explosive moonstones. Each puzzle is a pattern
of dominoes for you to start from.

## Goal ##
The different numbers on the dominoes are different kinds of moonstones, and
the goal is to collect all the dominoes by sliding matching numbers next to
each other.

## Moves ##
There are only two ways a domino can move.

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
four above it to make six.

    2|4     2|4
    
    2|6       2>6

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

### Stay Connected ###
Keep the mine connected so it doesn't collapse. All the dominoes must be in
one connected group, you can't split the group after moving or after
removing the matching dominoes.

## Problems ##
Here are the starting positions for several Moonside problems. The solutions
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
    0|2 0|6
    
    5|5 3|6
    
    0 0|1 5
    -     -
    4 1|3 6

### Problem 5 ###
    6|0 1|5
    
    4|0 1 0
        - -
    2|1 6 3
    
    2|6 1|0

### Problem 6 ###
    0|4 0 0|3
        -
    6|4 2 4|1
    
    3|2 2|4 0
            -
    3|6 2|6 6

### Problem 7 ###
    4 2|4 2|1
    -
    0 0|3 4|1
    
    6|0 1|0 2
            -
    1|5 6|3 6

### Problem 8 ###
    3|0 2 1 6 2
        - - - -
    3|5 4 4 6 1
    
    2 1 1|0 6|0
    - -
    0 5 2|5 3|1

### Problem 9 ###
    0|4 6|5 5|5
    
    0|2 2 5|1 1
        -     -
    3 3 2 6|1 0
    - -
    1 4 2|4 5|0

### Problem 10 ###
    1|5 6|5 0|6
    
    1|3 2|5 0 4
            - -
    1|0 1|4 3 2
    
    1|2 6|3 5|0
    
    6|6 2|0 2|2

### Problem 11 ###
    4 4|4 5|4 4
    -         -
    1 0|2 3|2 2
    
    2 0 1|5 0|6
    - -
    6 0 1 6|5 2
        -     -
    6|4 1 0|1 1

### Problem 12 ###
    2 5|2 0|2 1
    -         -
    3 4|2 0|6 3
    
    0|4 5|0 5|3
    
    5 1|1 6 6|2
    -     -
    1 6|5 4 4|5

### Problem 13 ###
    5|3 0|4 0|2
    
    5 4|2 1 5|2
    -     -
    4 1|1 5 4 1
            - -
    0|5 4|6 4 6
    
    3|1 5|6 0|6
    
    3|0 3|6 4|1

### Problem 13B ###
    4 3|4 4|0 6
    -         -
    2 4|1 4|4 3
    
    5 5|6 6 2|3
    -     -
    1 0|6 1 1 5
            - -
    3 0 2|6 1 0
    - -
    3 3 6|4 4|5

### Problem 13C ###
    0 4|6 4|0 6
    -         -
    6 4|2 4|4 3
    
    3 0|0 1 2|3
    -     -
    3 6|5 2 0 5
            - -
    6|6 5|5 1 0
    
    3|0 1|6 4|5


### Problem 14 ###
This puzzle uses all the dominoes.

    6|1 3 0|4 2|3 3
        -         -
    0|1 1 0 0|2 6 6
          -     -
    6|6 4 3 4 5 4 0
        -   - -   -
    0|5 4 4 2 4 1 6
          -     -
    2 0|0 3 3|3 5 1
    -             -
    5 2|6 3|5 5|5 2
    
    1|1 1|4 2|2 6|5

## Contributing ##
Found some interesting problems to solve? Ideas to share? Get in touch at
[donkirkby.github.com/moonside][github].

[github]: http://donkirkby.github.com/moonside

## Solutions ##
Here are the solutions. For each step, move the listed domino left, right, up,
or down. Then make captures for any matching numbers.

1. 15D, 66R, 06U, 15U
2. 42L, 41L, 15D, 15D, 04D, 05R, 42R, 05R
3. 43D, 05D, 05U, 53L, 03U, 53R
4. 06R, 06L, 55R, 04U, 56U, 13R
5. 40L, 21L, 40R, 15L, 21R, 10L, 03D, 15R, 03D
6. 02U, 06D, 06U, 24R, 41R, 64R, 32R, 36R, 64L, 02D
7. 41R, 41L, 26U, 63R, 63R, 15R, 15R, 60R, 40D, 24L, 03R, 24L
8. 14U, 14D, 35R, 35L, 15U, 25L, 20D, 15D, 60L, 21D, 60R
9. 55R, 55L, 04R, 04L, 34U, 34D, 24L, 24R, 61L, 50L, 50R, 61R
10. 15L, 15R, 25L, 65L, 06L, 06R, 14R, 10R, 10L, 63L, 50L, 42D, 50L
11. 42U, 42D, 44R, 02R, 44L, 26U, 26D, 02L, 15L, 15R, 06L, 21U, 01R, 06L
12. 45R, 45L, 11R, 65R, 11L, 62L, 65R, 11R, 11R, 11R, 53R, 50R, 11L, 11L, 11L,
    04R, 51U, 23D, 52L, 52L, 04L, 06L, 50L, 06R, 53L
13. 06R, 44D, 56R, 52R, 56L, 05R, 54D, 06L, 54U, 31R, 30R, 15D, 42R, 42R, 52L
14. 31U, 01R, 11L, 14L, 25D, 00L, 44D, 66R, 03D, 01R, 33L, 54D, 42D, 42D, 65L,
    15D, 64D, 64D, 66R, 66R, 04L, 66R, 02R, 66R, 36D, 02L

Moonside is an original puzzle designed by Don Kirkby, and an anagram of
"dominoes".
