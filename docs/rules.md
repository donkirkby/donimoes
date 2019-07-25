---
title: The Rules of Donimoes
---

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
          4  
          -
    2|3 2 6  
        -
        4 0|2

### Problem 3 ###
      3|0     5|3
    
        3 6 2|4  
        - -
    4|6 4 3      

### Problem 4 ###
    0|4 0 5      
        - -
        5 4   2|0
    
          6|3 6|2

### Problem 5 ###
            1  
            -
    0|4 3 5 4  
        - -
      6 4 3 5  
      -     -
      0     2  
    
      1     6|5
      -
      0        

### Problem 6 ###
        0      
        -
    4|3 4      
    
      5     0|2
      -
      0   0|6  
    
      5 2|2 0  
      -     -
      1     0  

### Problem 7 ###
    1           0|6
    -
    0     4   5|4
          -
    6     3 4|6
    -
    3 6|5 1
          -
          6

### Problem 8 ###
          5     2
          -     -
          0 3|3 5
    
          3   5|4
          -
      4|6 4     2
                -
    2|2         0

### Problem 9 ###
              0  
              -
    1|6 0|6   3  
    
        2|1   1  
              -
        6|2   3  
    
      6 2|4 0 1|1
      -     -
      4     4

### Problem 10 ###
      5
      -
      4   6|3 6|0
    
    1|2     6   1|6
            -
      6 5|5 2 1
      -       -
      5 6|6   0

### Problem 11 ###
        0 1|0 4|5 6|0
        -
        5   4|0 4|1  
    
        2|3     6|4  
    
    3|4 1|2 5|2   6  
                  -
                  5  

### Problem 12 ###
      2|6 3 4|0
          -
      6   6    
      -
      1        
    
    0|0 3|0    
    
        5      
        -
        3 2    
          -
          5 3  
            -
            1 4
              -
              3

### Problem 13 ###
      6         2
      -         -
      1 5|0 4|0 2
    
      2 0 2|0 6 1
      - -     - -
      3 1 3|1 3 1
    
    2|1     3|5

### Problem 14 ###
                4  
                -
    3|1   4|6 4 1  
              -
      2 4     4 2|5
      - -
      3 2   4|0 5  
                -
      5 0|0 1|1 4  
      -
      6 5|5 3|3 6|3

### Problem 15 ###
        6          
        -
    3|3 5   2|2 0|5
    
      4 2|1 5|5    
      -
      3       0 4|4
              -
      6   2|5 0 1  
      -         -
      6 4|5 3|5 1  
    
    4|0 3|2 1|3 6  
                -
                1  

### Problem 16 ###
      4|2 4|6 5|0  
    
        1|2 5|6 5  
                -
      3 0|4 2|0 2  
      -
      2 1 3 6|3 5  
        - -     -
    5|5 3 4     3  
    
      6 2|6 3|3 4|5
      -
      6            

### Problem 17 ###
      6            
      -
      4 1|1 5|1 6|6
    
    0|6 4|2     1  
                -
      0   0|0 1 0  
      -       -
      2   2|5 4 6  
                -
      4|5   3|5 1  
    
    4|0 6   6|2 3|3
        -
        5          

### Problem 18 ###
    6|0   1|5 4|3
    
      4 2|5 2|6  
      -
      0 4 2|1 2  
        -     -
      4 6 0|0 2 5
      -         -
      2 0|5 4|1 3
    
    0|3 6|1 3|2 1
                -
                3

### Problem 19 ###
                      4  
                      -
          1|0 6|2 6|0 3  
    
      6|4 0     5|2 5 4  
          -         - -
    4|5   5       1 5 0  
                  -
          6 0|3 4 5   6  
          -     -     -
          1 2|0 1 2|2 6  
    
          2|1 2|3   3 1|3
                    -
                    5    

### Problem 20 ###
                    2  
                    -
    4|2 5|0 4|4 6|0 2  
    
      3   6|6 2|3   5|3
      -
      3 5 3|1 0 2|6    
        -     -
      5 1 4|3 0 1|2    
      -
      2 5 3|0 2|0 1    
        -         -
    5|5 4     6|3 6 4  
                    -
      1 0|1 6|5 6|4 0  
      -
      1             4  
                    -
                    1  

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
2. 24U, 02L, 02L, 02L, 24D, 46D
3. 53L, 53L, 63D, 24L, 34D, 24L, 24L, 24L, 34U, 63U, 30L, 53L
4. 20L, 63L, 62L, 54U, 20L, 63L, 62L, 05U, 20L, 20L, 20L, 05D, 54D, 63L, 62L
5. 65L, 65L, 52D, 14D, 53D, 34D, 04R, 04R, 60U, 10U
6. 04D, 04D, 43R, 43R, 43R, 04U, 50U, 06L, 51U, 02L, 00U
7. 06L, 54L, 06L, 06L, 06L, 06L, 43U, 46L, 43U, 54L, 46L, 46L, 16U, 54L, 54L, 43D
8. 22R, 22R, 22R, 22R, 34D, 50D, 54L, 25D, 50U, 54L, 54L, 34D, 46R, 54R, 54R, 50D,
   46R, 46R, 34U
9. 21L, 06R, 16R, 21R, 62R, 64U, 64U, 24L, 62L, 04U, 04U, 11L, 11L, 13D, 03D
10. 43U, 31U, 43U, 31U, 43U, 31U, 43U, 31U, 43U, 31U, 43U, 25U, 30R, 53U, 30R, 25U,
    53U, 53U, 00R, 25U
11. 23L, 52R, 12R, 34R, 23R, 23R, 05D, 10L, 40L, 45L, 60L, 41L, 64L, 65U, 65U, 52R,
    12R, 34R
12. 12R, 66R, 10D, 16L, 63L, 12R, 54D, 63R, 16R, 10U, 66L, 62D, 10D, 16L, 12R, 63L,
    60L, 12L, 16L, 10U
13. 11D, 22D, 11D, 22D, 40R, 40R, 63U, 63U, 20R, 50R, 01U, 21R, 21R, 01D, 50L, 23D,
    61D, 20L, 63D, 63D, 40L, 40L, 22U, 11U
14. 31R, 40L, 44D, 46R, 31R, 23U, 56U, 55L, 55L, 33L, 33L, 63L, 63L, 54D, 54D, 11R,
    11R, 44D, 25L, 25L, 41D, 25L, 44U, 11L, 11L, 54U, 54U, 63R, 33R, 55R
15. 55R, 21R, 65D, 65D, 33R, 33R, 43U, 66U, 45L, 25L, 35L, 00D, 44L, 44L, 44L, 11U,
    61U, 00U, 35R, 25R, 45R, 66D, 65D, 21L, 55L, 11U, 61U, 13R, 32R, 40R, 43D, 33L,
    22L, 05L
16. 32U, 42L, 46L, 32D, 12L, 56L, 50L, 52U, 52U, 20R, 20R, 04R, 04R, 34U, 13U, 55R,
    55R, 66U, 55R, 13D, 55R, 34D, 04L, 20L, 52D, 04L, 20L, 52D, 50R, 56R, 12R, 32U,
    66U, 26L, 33L, 45L, 46R, 42R
17. 45R, 42R, 02D, 42R, 06R, 06R, 64D, 64D, 11L, 51L, 66L, 11L, 51L, 66L, 10U, 10U,
    42R, 42R, 61U, 14U, 35R, 25R, 45R, 65U, 65U, 65U, 40R, 45L, 25L, 14D, 35L, 42L,
    61D, 42L, 62L, 33L, 10D, 10D, 66R, 51R, 11R
18. 60R, 53U, 53U, 43R, 15R, 60R, 40U, 40U, 25L, 25L, 46U, 42U, 05L, 41L, 13U, 13U,
    41R, 05R, 42D, 46D, 32R, 61R, 03R, 25R, 25R, 40D, 40D, 60L, 15L, 43L
19. 41U, 22L, 35U, 35U, 13L, 13L, 66D, 40D, 43D, 66D, 40D, 43D, 60R, 60R, 55U, 55U,
    52R, 62R, 10R, 05U, 45R, 61U, 05U, 64R, 61D, 45R, 64R, 64R, 45R, 05D, 45R, 05D,
    10L, 62L, 52L, 55D, 55D, 60L, 60L, 43U, 40U, 66U
20. 53L, 66L, 23L, 53L, 22D, 22D, 60R, 44R, 50R, 60R, 42R, 44R, 50R, 42R, 33U, 33U,
    66L, 66L, 51U, 52U, 54U, 55R, 55R, 11U, 11U, 01L, 65L, 63L, 64L, 16D, 20R, 16D,
    40U, 41U, 16U, 20L, 40U, 41U, 16U, 64R, 63R, 65R, 55R, 54D, 01R, 11D, 52D, 51D,
    66R, 66R, 33D, 33D, 42L, 50L, 44L, 60L

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
