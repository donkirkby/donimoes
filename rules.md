# Donimoes: Puzzles with Dominoes #
There are two kinds of puzzles: blocking and capturing.

## The Blocking Puzzle's Goal ##
The goal is to slide all the dominoes into a rectangle, without sliding any
matching numbers next to each other.

## Moves ##
Move a domino one space along its long axis so that none of its numbers match
an adjacent number on a neighbouring domino. In this example, the lower domino
can move to the right, because the three doesn't match the two, and the four
doesn't match the 3. You couldn't move it another space to the right, because
then the threes would be right next to each other.

      2|3     2|3
    
    3|4       3>4

## Stay Connected ##
All the dominoes in the puzzle have to be connected in one solid group, diagonal
connections don't count. When you move a domino, it can be disconnected during
the move, as long as it is connected at the start and the end of the move.
Remember that it can only move one space at a time, though.

## Problems ##
Here are the starting positions for several Blocking Donimoes problems. The
solutions are listed at the end.

### Problem 1 ###
      2    
      -
      3 1|2
    
    2|4    

### Problem 2 ###
      3|0     5|3
    
        3 6 2|4  
        - -
    4|6 4 3      

### Problem 3 ###
    1           0|6
    -
    0     4   5|4
          -
    6     3 4|6
    -
    3 6|5 1
          -
          6

### Problem 4 ###
      5
      -
      4   6|3 6|0
    
    1|2     6   1|6
            -
      6 5|5 2 1
      -       -
      5 6|6   0

### Problem 5 ###
      6         2
      -         -
      1 5|0 4|0 2
    
      2 0 2|0 6 1
      - -     - -
      3 1 3|1 3 1
    
    2|1     3|5


## The Capturing Puzzle's Goal ##
The goal is to collect all the dominoes by sliding matching numbers next to
each other.

## Moves ##
There are only two ways a domino can move.

### Matching ###
Move a domino one space along its long axis so that it ends up with at least
one of its numbers matching an adjacent number on a neighbouring domino. Then
collect the domino you moved and any dominoes that match it, by removing them
from the pattern. In this example, the threes match, so you collect both
dominoes: solution found!

    2|3     2|3       2*3
    
    3|4       3>4       3*4

### Adding ###
Move a domino one space along its long axis so that it ends up with at least
one of its numbers next to an adjacent number that adds up to six. With an
adding move, no dominoes are removed. In this example, the two adds up with the
four above it to make six.

    3|4     3|4
    
    2|1       2>1

Sometimes, you can collect more than two dominoes at once. In the first
example, the two matches twos on both of the other dominoes, and you collect
all three dominoes. In the second example, the two matches the two to the left,
and the four matches the four above it. You collect all three dominoes.

    5 2|4     5 2|4   5 2*4
    -         -       *
    2   2|6   2 2<6   2 2*6
    
    
    
    5 3|4     5 3|4   5 3*4
    -         -       *
    2   2|4   2 2<4   2 2*4

### Stay Connected ###
All the dominoes must stay in one connected group, you can't split the group
after moving or after removing the matching dominoes.

## Problems ##
Here are the starting positions for several Capturing Donimoes problems. The
solutions are listed at the end.

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
    0 1|0 2 5 3|2 3
    -     - -     -
    4 6|5 4 1 2|0 6
    
    0 5 2|6 4 5 4|1
    - -     - -
    3 4 5|5 4 0 2 6
                - -
    6 0|0 3|1 3 2 6
    -         -
    1 6|4 6|0 4 1|2

### Problem 19 ###
    4|2 5|6 3|3 5|4
    
    6 3|4 5|5 6|4 0
    -             -
    6 1|5 3 1|1 0 1
          -     -
    2|3 2 5 6|3 6 0
        -         -
    1|2 6 2|2 1|3 0
    
    6 5|2 0|4 0|5 4
    -             -
    1 2|0 3|0 4|4 1

### Problem 20 ###
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
[donkirkby.github.com/donimoes][github].

[github]: http://donkirkby.github.com/donimoes

## Blocking Solutions ##
Here are the solutions to the Blocking Donimoes problems. For each step, move
the listed domino left, right, up, or down. 

1. 24R, 24R, 23D
2. 53L, 53L, 63D, 24L, 34D, 24L, 24L, 24L, 34U, 63U, 30L, 53L
3. 06L, 54L, 06L, 06L, 06L, 06L, 43U, 46L, 43U, 54L, 46L, 46L, 16U, 54L, 54L, 43D
4. 12R, 66R, 10D, 16L, 63L, 12R, 54D, 63R, 16R, 10U, 66L, 62D, 10D, 16L, 12R, 63L,
   60L, 12L, 16L, 10U
5. 11D, 22D, 11D, 22D, 40R, 40R, 63U, 63U, 20R, 50R, 01U, 21R, 21R, 01D, 50L, 23D,
   61D, 20L, 63D, 63D, 40L, 40L, 22U, 11U

## Capturing Solutions ##
Here are the solutions to Capturing Donimoes problems. For each step, move the
listed domino left, right, up, or down. Then make captures for any matching
numbers.

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
18. 61D, 60L, 60L, 31L, 31L, 03D, 04D, 10L, 54D, 26L, 10L, 26L, 24D, 51D, 51D,
    41L, 36D, 41R, 34U, 34U, 12L, 20R, 34U
19. 41D, 30R, 12L, 61U, 61U, 20R, 26D, 13L, 34L, 06D, 34L, 55L, 35U, 35U, 11R,
    64R
20. 25U, 40D, 10D, 63D, 60R, 60R, 32D, 20R, 31D, 65R, 62D, 21R, 51R, 34L, 53R,
    51R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/

