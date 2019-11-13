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

# Domino Puzzles By Other Designers #
## Dominosa ##
The domino puzzle I often see is called either Dominosa or Domino Solitaire. You
start with a grid of numbers, and you have to lay the dominoes on them. It was
invented by O.S. Adler in 1874. There's an [interesting proof][proof] that this
puzzle is NP-hard.

Reiner Knizia published some puzzles called [Domino Knobelspass][knizia] that
are very similar to Dominosa.

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass

## Mountains and Valleys ##
Sid Sackson included this in his [Beyond Solitaire][solitaire] book, and I
adapted it from paper, pencil, and dice to use dominoes.

To start, shuffle a set of double-six dominoes face down, then turn 18 of them
face up. The remaining 10 aren't used. Then arrange the dominoes into a 6x6
square of numbers that represents a map of mountains and valleys, where blanks
are at sea level, and sixes are the highest peaks. The goal is to make a map
where you can walk to every square. You can walk from one square to its
neighbour if the two heights are the same or differ by one. (You can't climb
cliffs.)

For example, this set of 18 dominoes:

    4 1 3   2 5 2
    - - -   - - -
    2 0 1   0 4 2
    
    3 6 5   5 6 4
    - - -   - - -
    0 0 5   1 3 4
    
    6 1 3   0 1 1
    - - -   - - -
    5 4 3   4 6 2

Can be arranged into this solution:

    0|1 2|1 0|4
    
    2 1|5 4|1 4
    -         -
    0 0|6 4|2 4
    
    0|3 3|3 4|5
    
    1 2 3|6 5|5
    - -
    3 2 1|6 5|6

I like this solitaire, because it can almost always be solved, though finding a
solution can be very difficult. There's usually more than one solution. For
example, you can flip the 56 domino, above. There is a trivially unsolvable
situation whenever one of the numbers from 1 to 5 is completely missing, but
that can be quickly checked, and I haven't found any other unsolvable
combinations.

[solitaire]: https://boardgamegeek.com/game/3940

## Fujisan ##
James Droscha designed this for the piecepack game system, and then adapted it
for dominoes and pawns in a paper on
[using entangled components in solitaire games][droscha].

Four Shinto Priests have traveled from their various prefectures in pilgrimage
to the top of Mount Fuji. You must find pathways for them to move up and down
the mountain until they can all achieve the peak. Often, this will require you
to guide them into positions from which they can assist each other.

### Setup ###
Remove all dominoes with the number six and all doubles from a standard set of
double-six dominoes. Shuffle the remaining 15 dominoes face down, then place
twelve face-up dominoes side by side. Leave the three remaining dominoes face
down, and use them to lift up the two middle dominoes as the peak of Mount Fuji.
Here's an example layout:

    5 5 4 3 5 1 2 1 1 2 4 0
    - - - - - - - - - - - -
    3 0 1 4 2 2 0 0 3 4 5 3

Place a Priest (pawn) beside each number at both ends of the mountain.

### Moving a Priest ###
1. A Priest may move onto a space if the number matches the number of unoccupied
  spaces the Priest must move in a straight line to get there (including the
  destination space itself, but not including the space the Priest's starting
  space). For example, a Priest may move onto a space containing a value 4 coin
  if there are 3 unoccupied spaces between it and the Priest.
2. Occupied spaces (containing intervening Priests) are not counted when
  determining if a Priest may move onto a particular space. For example, a
  Priest may move onto a space containing a value 2 coin if there are 3 occupied
  spaces and one unoccupied space between it and the Priest.
3. A Priest may move freely between the two spaces on a domino. This is the only
  manner in which a Priest may move onto a blank space.
4. Once a Priest lands on the peak of the mountain, he will refuse to leave it,
  but he can move back and forth (in the same domino) or to and fro (between the
  two dominoes). Clarification: A Priest may pass over the peak dominoes as part
  of a move.
5. A Priest must enter the mountain from his own starting row; that is, he
  cannot move back or forth while he remains on the ground.

### Goal ###
The Priests will be content when they all reach the top of the mountain.

### Variant ###
Country Road: Once all four Priests have reached the peak, move the dominoes
at the peak to the Priests' original setup positions at the two ends of the
mountain and continue until all four Priests have left the mountain.

Treat the spaces at the peak as blanks. Once a Priest leaves the mountain, he
will not step back on.

[droscha]: https://arxiv.org/abs/1810.01926

## Problems ##
Shuffling the dominoes generates a nice set of problems. In 1000 randomly
generated problems, 92% were solvable. Of those, the median solution length
was 14, with half of them between 12 and 16. Here are some more challenging
problems for you to try. The solutions are listed at the end.

### Problem 1 ###
    3 2 1 0 0 1 0 3 1 2 3 1
    - - - - - - - - - - - -
    4 0 0 4 5 2 3 2 5 5 1 4

### Problem 2 ###
    2 5 5 1 0 2 3 3 1 4 5 1
    - - - - - - - - - - - -
    1 1 2 4 5 0 2 4 3 0 4 0

### Problem 3 ###
    5 1 0 3 1 1 2 2 0 4 0 0
    - - - - - - - - - - - -
    2 2 5 5 5 3 0 4 4 3 1 3

### Problem 4 ###
    3 1 2 3 4 2 0 1 0 1 5 0
    - - - - - - - - - - - -
    4 3 1 5 2 0 5 0 4 4 2 3

### Problem 5 ###
    5 5 0 1 3 1 1 0 1 1 4 4
    - - - - - - - - - - - -
    2 0 2 2 5 4 5 3 0 3 0 2

### Problem 6 ###
    5 5 2 0 1 1 3 2 0 0 3 4
    - - - - - - - - - - - -
    2 1 4 4 2 4 2 0 1 5 1 5

### Problem 7 ###
    3 2 5 4 3 1 4 0 1 2 2 1
    - - - - - - - - - - - -
    4 5 0 1 0 0 0 2 2 4 3 3

### Problem 8 ###
    4 3 1 5 2 2 0 1 1 0 3 3
    - - - - - - - - - - - -
    0 1 0 4 0 3 5 4 2 3 5 4

### Problem 9 ###
    5 0 4 2 4 5 4 1 2 4 3 5
    - - - - - - - - - - - -
    3 3 5 1 0 0 1 0 5 2 1 1

### Problem 10 ###
    5 3 1 1 0 2 0 0 1 0 5 2
    - - - - - - - - - - - -
    4 5 5 3 2 3 1 4 2 3 0 5

### Problem 11 ###
    2 3 1 0 2 0 0 2 1 0 4 0
    - - - - - - - - - - - -
    3 4 4 2 5 5 4 4 3 1 5 3

### Problem 12 ###
    5 3 1 1 0 0 0 1 1 0 4 3
    - - - - - - - - - - - -
    4 4 5 3 2 5 1 4 2 3 0 5

### Problem 13 ###
    1 0 0 2 3 5 5 2 0 0 1 1
    - - - - - - - - - - - -
    4 3 4 0 2 2 3 1 5 1 3 5

### Problem 14 ###
    4 3 1 5 0 2 4 1 0 1 1 2
    - - - - - - - - - - - -
    1 4 3 2 2 3 0 2 5 0 5 4

### Problem 15 ###
    2 4 3 3 3 0 0 2 0 5 4 3
    - - - - - - - - - - - -
    5 5 0 2 1 5 4 1 1 1 1 5

### Problem 16 ###
    4 3 3 2 0 4 3 3 5 1 1 5
    - - - - - - - - - - - -
    5 4 1 5 2 0 0 2 0 4 0 3

### Problem 17 ###
    4 4 5 1 0 0 1 0 0 1 3 5
    - - - - - - - - - - - -
    5 3 2 2 1 5 4 2 4 3 0 1

### Problem 18 ###
    2 4 2 5 3 5 1 2 4 2 3 4
    - - - - - - - - - - - -
    5 5 1 0 1 1 0 0 1 4 0 0

### Problem 19 ###
    2 4 1 0 0 5 1 2 4 2 4 0
    - - - - - - - - - - - -
    5 5 2 5 3 1 0 0 1 4 3 4

### Problem 20 ###
    5 5 0 2 0 1 1 0 1 5 4 0
    - - - - - - - - - - - -
    1 3 3 4 2 4 2 1 3 2 0 5

# Solutions #
## Blocking Donimoes Solutions ##
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

## Capturing Donimoes Solutions ##
Here are the solutions to the Capturing Donimoes problems. For each step, move the
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

## Fujisan Solutions ##
Here are the solutions to the Fujisan problems. To distinguish the four different
pawns, the top left is labelled as a (P)awn, the bottom is a k(N)ight, the top
right is a (B)ishop, and the bottom right is a (R)ook.

1. NR4, NR2, PR2, PR1, PD, PR3(+1), BL1, BL2, BD, RL5(+3), RU, RR1, PU, BL3
2. NR1, NU, BL1, BD, BL3, RL4(+1), RU, BU, BL5(+1), RL5(+1), PR1(+3), NR2(+3),
   ND, PR2, RR3(+2), RD, BR3(+1)
3. NR5, NR4, RL4(+1), NL5(+1), NU, PR3(+1), NR1(+1), PD, PR4(+1), RR3(+1), RU,
   PU, NR4(+1), BL2(+3), RL2(+3), PL1(+2), PD, RD, NL2(+1), BL1(+1)
4. RL4, RL5, RU, PR4(+1), PD, RD, NR5(+2), NU, RR4(+1), RR3, RU, PU, PR5(+1),
   BL1(+2), PL4(+2), PD, PR4, PU, BL2(+2), BD, PL2(+1), RD, RL5
5. NR5, NL2, NL2, NU, RL3, RL5, RU, RL1, PR3(+2), PD, PR3, PU, NR3(+1), RR1(+1),
   NR4(+2), ND, PR4, NU, BL1(+2), NL1(+1), NL3(+1), NR1(+1), BD, BL4, PD, PL5
6. NR4, NU, NR1, NL2, ND, NL1, NU, PR2(+1), PD, ND, NR2(+1), NR5, NU, NL2, NR4,
   ND, PR2, PR5, PU, PL2, RL1(+1), RU, NU, BL3(+3), BD, NL3(+2), PL1(+1), RD,
   RL4(+1)
7. BL1, BL2, BD, BL2, PR2, PR3, PD, PR4(+1), BR3(+1), RL2(+2), BL2(+2), BU, BL3,
   RU, RL5(+1), BL3(+1), BD, RD, PL2, PL5(+1), NR1(+3), RU, PU, PR4(+1), PD, RR4,
   NU, BU, BR3(+1), NR1(+1), ND, BR1
8. RL3, RU, RL1, RL5, RL1, RR2, RL4, RD, NR1(+1), NU, RU, PR1(+2), RR2(+2), RD,
   NR2(+1), PD, PR4(+1), RR5(+1), RL2, ND, NR3(+2), RU, RR3, PU, PR3, NU,
   BL1(+3), PL1(+2), PL2, PR, NL2(+2), ND, BL2(+1), RD, RL5
9. RL1, RL1, RU, RL2, RL4, RD, RL1, RU, PR4(+1), RD, RR5, RU, PR4(+1), PD, RL1,
   RR3, PU, BL2(+2), PL1(+1), RL4(+2), BL4(+2), PL5(+2), PD, RD, RL3, BD,
   NR1(+3), PU, PR5, PD, BU, RU, RR4(+1), RD, BR4, NL3, NU, NR5
10. RL3, RU, RR2, RD, RL4, RL5, NR3(+1), NR4, NL5(+1), NU, RR2, RL4, RU, PR1(+2),
    PD, ND, RD, RR2(+2), NR4(+2), NU, NR1, ND, PR4(+1), RR3(+2), RU, NU, NR2(+1),
    PL5, PR2, PU, PR5(+1), BL1(+3), ND, NL4, NL1, RD, PD, PL3(+2), PU, PR,
    BL2(+1), RL3(+1)
11. NR5, NU, NL3, ND, NR2, NR4, NU, NR1, ND, NR1, RL4(+1), RR3(+1), NL5, RL4,
    RL4(+1), RU, RL2, NU, NL3, PR1(+2), RR2(+2), RD, NR2(+1), PD, PR4(+1),
    RR3(+1), PR1(+1), PU, RU, NR4(+2), BL2(+3), ND, NL4, BD, RD, PD, PL4(+3), NU,
    BR3(+1), BL5(+1), BU, PR4, RR3, RL5(+1)
12. RL3, RU, RL1, RL1, RD, RL5, RR2, RL4, NR3(+1), NR4, NL5, NR2, NU, NL3, RU,
    PR1(+2), PD, ND, RD, RR2(+2), NR4(+2), NU, NR1, ND, PR4(+1), RR3(+2), RU,
    NL5(+1), PU, NR2, NU, NR4(+2), ND, PR3(+1), NU, BL1(+3), ND, PD, PL5(+1), PU,
    NL5, RL1(+1), RD, BD, BL1(+1), BU, RL1
13. BL1, BL1, BD, BL1, BU, BL2, BL3, BD, BL3, BU, PR1, PR2(+1), PD, PR5, PL1, PR3,
    PU, PR1, PD, BR2, BD, BR5, BL1, BR3, RL1(+2), RU, BU, PU, PL2(+2), PL3, PD,
    PL4, BL2(+1), BL3, BD, RL2, RD, RL4(+1), RU, BL3, RD, NR2(+3), PR2(+3), PU,
    BR3(+2), RR2(+1), NL4, NU, NR5(+1)
14. NR3, NR2, NU, NL3, ND, NR2, NR5, NU, NR1, NR2, BL1(+1), NL1(+1), ND, NL2, NU,
    BL1, BL5(+1), BL1, BD, BR2, BU, ND, NR4, NU, NL1, NL1, NL5(+1), NL1, ND, NR2,
    BL4, NU, NL3, PR1(+2), PD, ND, BD, BR2(+2), NR5(+2), NU, PR5(+1), BR5(+1),
    NR1, ND, RL2(+3), RU, RL2, PL3, PR, NL3(+1), BU, BL4
15. PR3, PL2, PR3, PD, PR1, PU, PR5, PD, PL1, PU, PR3, PD, RL1(+1), PL1(+1), PL1,
    PU, RU, RL2(+1), PL3(+1), RL3(+1), RD, PR5, PL2, PD, PL5(+1), PU, RU, RL2(+1),
    RD, PD, NR2(+2), PU, PR3, PR5, PD, PL1, NU, RU, RR3(+1), NR5(+1), PU, RR4(+2),
    BL2(+3), ND, NR1, NL4, NU, RD, RL5, BD, PD, PL5(+2), PR4(+1), BL5(+2), RU,
    BR5
16. PR3, PD, PR2, PU, PL3, PR2, PR5, PD, PR3, PU, BL1(+1), PL1(+1), PD, BL3, BD,
    PL5(+1), PU, PR5, BU, BR1(+1), PD, BD, BL5(+1), BL1, BR2, BU, BL4, BD, PL5,
    PL1, PR2, PU, PL3, PD, NR1(+2), PR2(+1), NU, BU, BR2(+1), NR5(+1), ND, NR3,
    BR5, BD, PR4(+1), RL2(+3), PU, PL3, PD, BU, RU, RR1(+1), NU, NL4(+2), ND,
    BR1(+1), BL4(+1), RL3
17. RL3, RL2, RU, RL5, RR1, RD, RR1, RL3, NR2(+1), NU, RR2, ND, NR1(+1), NR4, NU,
    NR1, ND, NL2, RR4(+1), NU, NR3, ND, RU, RR1, RD, RR1(+1), RU, NU, BL1(+2), BD,
    ND, RD, RL2(+2), RU, RL5, RR1, RD, NL2(+1), NU, NL5, ND, BL2, BL5(+2), BU, NU,
    RR1, RL3, RU, PR1(+3), PD, PR1, PU, ND, NR4, NL, NU, PR1(+1), BD, BR5, RD,
    RR4(+1)
18. BL4, BL5, BD, BL1, BU, BL2, PR2(+1), BR3(+1), BR4, BL5, PL2, PR3(+1), BR4(+1),
    BD, PD, PR4(+1), PU, PL2, PD, BU, BL5, BD, PL5(+1), BL1, BU, BL2, BD, NR1(+2),
    PU, BU, BR3(+1), BR4, BD, PR3, PD, PR4(+1), PU, PL2, PD, BU, BL5, BD, NR1(+1),
    BR4(+2), BU, BL2, BR3, BD, NR4(+1), PU, PR4, PD, RL1(+3), RU, PU, PL5(+1), BU,
    BL2(+1), NU, NL1(+2), ND, RL1(+1), BD, BL1(+1)
19. BL4, BD, BL5, BU, BL1, BL2, BD, NR2(+1), BR3(+1), BU, BR4, BD, BL5, NU, NL2,
    ND, NR3(+1), NU, BU, BR4(+1), BD, ND, NR4(+1), NU, NL2, BL5, ND, NL5(+1), NU,
    BU, BL2(+1), PR1(+2), ND, BD, BR3(+1), BU, BR4, BD, PL2, PD, PR3(+1), PU, NR3,
    NR4(+1), NU, NL2, ND, BL3(+1), BR4(+1), BU, NU, PR4(+2), ND, NR4, PD, BD,
    RL1(+3), BU, NU, NL5(+1), BL2, BL1, BD, RL3(+1), PL5(+2), PR1(+1), RU,
    RR1(+1)
20. NR3, NR2, NU, NR5, ND, RL3(+1), NL1(+1), RL4(+1), RU, NU, NL5(+1), ND, RD,
    NR2(+1), NU, RU, RR5(+1), RL1, RD, RL1, RU, RL5(+1), ND, NL3, NL1, NU,
    PR2(+2), PD, NR2(+1), RD, RR2(+1), RU, NR5(+1), NL1, ND, PU, PR5(+1), PL1,
    NL1, NU, RR4(+2), RD, PD, PL1, PL4, PU, NL5(+1), PD, ND, NR2(+1), NU, PU,
    PR5(+1), PD, ND, NR5(+2), NU, PU, RU, BL1(+3), BD, PD, PL2(+1), PU, BL2, RD,
    ND, NL4(+2), NU, RL4(+1)

# Contributing #
Found some interesting problems to solve? Ideas to share? Get in touch at
[donkirkby.github.com/donimoes][github].

Capturing and Blocking Donimoes are original puzzles designed by
[Don Kirkby][don].

[github]: https://donkirkby.github.com/donimoes
[don]: https://donkirkby.github.com/
