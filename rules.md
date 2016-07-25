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
    2 1|4 1
    -     -
    3 2|5 0

### Problem 2 ###
    1 0|5 3
    -     -
    2 5|3 6
    
    1|0 6|0


### Problem 3 ###
    3|3 2|1
    
    1 6 0|2
    - -
    6 2 3 1
        - -
    4|5 4 5

### Problem 4 ###
    0|3 4|6
    
    3 6 0|5
    - -
    3 2 3 0
        - -
    4|5 4 6

### Problem 5 ###
    4 3|6 5|4
    -
    6 4 3 6 5
      - - - -
    2 4 3 6 5
    -
    0 2|6 0|6

### Problem 6 ###
    3|4 6|4 6
            -
    4 6 1|6 0
    - -
    1 2 5|5 3
            -
    5|0 1|3 5

### Problem 7 ###
    3|6 2|0 2
            -
    5 3 1|2 3
    - -
    3 1 4|3 6
            -
    5|5 6|6 1

### Problem 8 ###
    0|2 0|0 2|6
    
    6 0|1 5 0 2
    -     - - -
    4 2|5 0 6 2
    
    2|4 6|5 3|0

### Problem 9 ###
    2 3|5 6 5|4
    -     -
    3 2|2 5 0 3
            - -
    1|5 3 4 1 0
        - -
    4|3 6 0 4|4

### Problem 10 ###
    2|5 3 6|4 1
        -     -
    6 2 0 5|6 5
    - -
    0 2 6|3 1 3
            - -
    4|1 0|2 0 3
    
    0|0 2|4 1|2

### Problem 11 ###
    2|1 3|0 6|4
    
    1 0|1 4|2 3
    -         -
    6 2|3 6|0 3
    
    1|3 0|5 6|5
    
    0|0 5|1 4|3

### Problem 12 ###
    5|3 1|2 4|2
    
    6 1|5 1 2|5
    -     -
    4 6|3 6 3|2
    
    2 1|4 3 2|0
    -     -
    2 3|3 0 5|4

### Problem 13 ###
    4|4 6|5 2|4
    
    0 1|5 4|0 6
    -         -
    3 4 6|6 2 4
      -     -
    1 3 5|2 1 2
    -         -
    3 6|1 0|6 3
    
    6|3 0|1 5|0

### Problem 14 ###
    2 1|2 5|2 0
    -         -
    2 3 1 2|6 1
      - -
    3 2 1 6 3|0
    -     -
    6 3|5 0 2|4
    
    3 4 6 4|6 5
    - - -     -
    4 5 6 5|5 0

### Problem 15 ###
    0 2 1|3 1|2
    - -
    6 0 4|4 6|1
    
    0 5|5 3 2|4
    -     -
    5 3|0 3 4|5
    
    4 0|4 2|3 1
    -         -
    6 5|6 3|6 5

### Problem 16 ###
    3|5 6|0 3|3 6
                -
    4 0|1 5|2 1 2
    -         -
    6 3 4|4 3 5 4
      -     -   -
    1 2 6|5 4 2 1
    -         -
    1 3|1 4|2 0 3
                -
    2|1 6|1 0|4 0

### Problem 17 ###
    2 0|2 0|1 2|3 1
    -             -
    5 4|1 5|5 6|2 5
    
    3 0|5 6 2|4 1 0
    -     -     - -
    0 3|1 6 4|0 1 0
    
    5 6|0 1|6 1|2 4
    -             -
    4 5|6 2|2 4|6 4

### Problem 18 ###
This problem uses all the dominoes.

    4|1 5|3 6 5|5 2
            -     -
    3|4 0 5 2 6|6 5
        - -
    4|2 5 4 6|5 2|2
    
    5|1 3 2|1 2|0 1
        -         -
    0 3 1 3|3 1|1 0
    - -
    3 2 6|1 6 0|0 4
            -     -
    6|0 4|6 3 4|4 0

## Contributing ##
Found some interesting problems to solve? Ideas to share? Get in touch at
[donkirkby.github.com/moonside][github].

[github]: http://donkirkby.github.com/moonside

## Solutions ##
Here are the solutions. For each step, move the listed domino left, right, up,
or down. Then make captures for any matching numbers.

1. 10D, 14R, 23D, 14R
2. 60R, 10R, 12D, 12D, 53R
3. 21R, 34U, 45R, 34U, 16U
4. 03L, 46L, 05R, 34U, 45R, 46L, 45R
5. 54R, 20D, 46D, 06L, 36R
6. 34L, 64L, 55L, 35D, 50R, 60D
7. 61D, 43R, 55R, 53D, 53D, 20R, 36R
8. 26R, 24L, 65L, 01L, 30L, 06U, 30L
9. 40D, 65D, 54L, 01D, 36D, 15R, 23D
10. 30U, 56L, 30D, 10U, 10U, 63R, 30D, 41R, 60D, 25R, 41R, 41R
11. 21L, 23L, 60L, 05L, 65L, 33D, 42R, 42R, 01R, 30L, 60R
12. 30D, 54L, 20L, 54L, 54L, 20L, 20L, 64D, 25R, 15L, 15L, 12R
13. 63L, 01L, 50L, 50L, 21D, 66R, 64D, 40R, 40R, 15R, 43U
14. 50D, 45D, 36D, 22D, 66U, 46R, 46R, 60D, 30L, 01D, 01D, 26R, 12R
15. 12R, 44R, 44R, 33U, 20U, 05U, 46U, 56L, 56L, 30L, 45L, 15U, 36R, 15U
16. 21L, 61L, 04L, 04L, 20D, 15D, 52R, 01R, 32U, 46D, 65L, 41U, 34U, 01R, 35R
17. 54D, 60L, 60L, 25D, 02L, 02L, 01L, 01L, 55L, 62L, 11U, 11U, 40R, 44U, 46R,
    22R, 46R, 22R, 16L
18. 25U, 40D, 10D, 63D, 60R, 60R, 32D, 20R, 31D, 65R, 62D, 21R, 51R, 34L, 53R,
    51R

Moonside is an original puzzle designed by Don Kirkby, and an anagram of
"dominoes".
