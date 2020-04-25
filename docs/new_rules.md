---
title: New Rules for Donimoes
---
# Experiments in Progress
These are new puzzles that aren't finished yet. You can try them out and let me
know what you think.

* **Dominosa** is the dominoes puzzle where you have to fit the set of dominoes
    into a grid of numbers.
* **Adding Donimoes** is a puzzle I designed where you add dominoes in the given
    order.

## Dominosa
The domino puzzle I often see is called either Dominosa or Domino Solitaire. You
start with a grid of numbers, and you have to lay the dominoes on them. It was
invented by O.S. Adler in 1874. There's an [interesting proof][proof] that this
puzzle is NP-hard.

Reiner Knizia published some puzzles called [Domino Knobelspass][knizia] that
are very similar to Dominosa.

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass

### Problem 1
    2 2 1 2
           
    0 0 1 0
    
    1 2 0 1

### Problem 2
    3 2 4 4 4 4
               
    0 1 3 0 4 0
             
    0 2 1 0 3 2
               
    3 3 1 2 2 1
    
    1 0 1 4 2 3


### Problem 3
    1 0 3 4 4 0 2
                 
    1 5 0 2 4 1 0
               
    4 5 1 4 4 3 2
                 
    0 2 2 3 1 3 2
               
    0 5 3 0 1 2 1
                 
    5 4 3 5 3 5 5

### Problem 4
    3 2 2 1 3
     
    2 0 0 0 2
    
    1 0 2 0 1
         
    1 3 1 3 3

### Problem 5
    1 2 4 0 0 3
               
    4 4 3 1 3 2
    
    0 2 1 0 3 0
    
    4 2 2 1 1 4
               
    1 3 3 2 4 0

### Problem 6
    0 5 3 5 2 1 1
             
    4 3 2 4 1 4 4
                 
    2 3 4 2 2 0 3
         
    2 5 1 0 0 5 1
                 
    0 5 3 1 5 2 0
         
    3 5 1 4 4 0 3

### Problem 7
    6 2 2 3 0 6 2 4
                   
    1 6 6 6 3 4 5 2
                 
    3 0 0 2 6 6 2 4
                   
    2 0 5 2 5 4 4 0
                 
    1 1 4 1 0 0 4 5
                   
    3 6 1 1 5 3 5 5
    
    0 1 4 5 1 3 3 3

### Problem 15
    4 1 1 0 1 2
               
    0 3 3 4 0 0
             
    1 3 4 1 0 4
               
    2 4 4 2 2 3
    
    2 3 0 3 1 2

### Problem 16
    0 1 0 2 0 3
    
    3 3 1 4 2 4
    
    1 1 0 0 1 3
    
    2 0 4 2 2 4
               
    1 2 3 4 4 3

### Problem 17
    0 3 2 6 2 5 1 6
    
    3 0 2 3 5 5 5 2
                   
    1 3 6 2 4 3 4 1
    
    5 0 4 5 0 6 0 0
           
    0 2 2 1 4 3 6 0
                   
    3 3 1 1 1 2 5 1
    
    6 6 4 6 4 5 4 4

### Problem 18
    6 2 6 2 3 6 2 2
               
    5 2 2 4 4 6 6 5
                   
    6 1 1 6 1 1 4 5
               
    0 1 3 0 0 0 1 1
    
    3 3 4 5 0 5 3 6
    
    0 2 5 4 1 5 3 5
                   
    0 4 3 4 0 3 4 2

### Problem 19
    0 5 1 3 2 6 0 4
    
    4 0 6 5 3 6 0 6
                   
    3 2 5 1 1 6 0 6
    
    4 5 4 5 5 0 2 1
                   
    2 2 4 2 3 4 1 1
    
    5 6 4 6 3 2 4 2
               
    0 1 3 5 3 1 3 0

### Problem 20
    0 4 2 6 2 5 0 5
    
    3 5 6 1 3 6 3 1
                   
    2 1 2 6 4 4 0 1
                 
    0 2 3 1 5 5 0 5
                   
    0 6 0 6 5 2 2 4
             
    3 4 1 4 1 6 6 5
                   
    2 4 0 3 3 1 4 3

### Dominosa Strategy
There are several methods to deduce where the dominoes must be placed, and it's
helpful to record on the puzzle, not only where the dominoes can be, but also
where they can't be. Here are some rules to help you make progress:

1. Look for a cell that only has one neighbour, and join it with its neighbour.
    Particularly check near the last pair you joined.
2. If you have a newly joined pair of numbers, check if the same pair appears
    elsewhere. Split the other location, because you can't have two dominoes
    the same. Also check all of the other neighbours that the newly joined pair
    might have joined with. Those pairs of numbers might now be unique.
3. If you have a newly split pair of numbers, look for the same pair elsewhere
    on the board to see if there is only one pair like them. If so, join them.
4. If all of a space's available neighbours are the same, you know it will join
    one of them. Look for the same pair of numbers elsewhere on the board, and
    mark them as split.
5. If a pair of undecided numbers appears more than once on the board, but all
    of the pairs share one space, then you know that space must join to the
    other number. Mark any other available neighbours as split.
6. Look for unique pairs of numbers, and mark them as joined. (This is the
    tedious part, so I try to only require it once or twice in each puzzle.)
7. If two unsolved areas are joined by a narrow neck, you know that both areas
    must have an even number of spaces in them. That will tell you where you can
    split or join the spaces in the neck.
8. If none of the other rules apply, guess at a domino's placement by marking a
    pair as joined.  If it later causes a contradiction, backtrack and mark it
    split. (This would be very frustrating when solving, so none of the problems
    in this collection require it.)

The easiest puzzles in this collection only require a couple of these rules, and
then the later puzzles require more and more different rules to solve.

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
## Dominosa Solutions
### Solution 1
    2|2 1 2
        - -
    0|0 1 0
    
    1|2 0|1

### Solution 2
    3 2|4 4|4 4
    -         -
    0 1|3 0 4 0
          - -
    0|2 1 0 3 2
        -     -
    3|3 1 2|2 1
    
    1|0 1|4 2|3

### Solution 3
    1|0 3 4 4|0 2
        - -     -
    1 5 0 2 4 1 0
    - -     - -
    4 5 1 4 4 3 2
        - -     -
    0 2 2 3 1 3 2
    - -     - -
    0 5 3 0 1 2 1
        - -     -
    5|4 3 5 3|5 5

### Solution 4
    3 2|2 1|3
    -
    2 0|0 0|2
    
    1 0 2 0|1
    - - -
    1 3 1 3|3

### Solution 5
    1|2 4 0|0 3
        -     -
    4|4 3 1|3 2
    
    0|2 1|0 3|0
    
    4 2|2 1|1 4
    -         -
    1 3|3 2|4 0

### Solution 6
    0|5 3 5 2 1|1
        - - -
    4 3 2 4 1 4 4
    - -       - -
    2 3 4 2|2 0 3
        -
    2 5 1 0|0 5 1
    - -       - -
    0 5 3 1|5 2 0
        -
    3|5 1 4|4 0|3

### Solution 7
    6 2|2 3|0 6|2 4
    -             -
    1 6 6|6 3|4 5 2
      -         -
    3 0 0|2 6 6 2 4
    -       - -   -
    2 0|5 2 5 4 4 0
          -     -
    1|1 4 1 0|0 4 5
        -         -
    3|6 1 1|5 3|5 5
    
    0|1 4|5 1|3 3|3

### Solution 15
    4 1|1 0|1 2
    -         -
    0 3|3 4 0 0
          - -
    1|3 4 1 0 4
        -     -
    2|4 4 2|2 3
    
    2|3 0|3 1|2

### Solution 16
    0|1 0|2 0|3
    
    3|3 1|4 2|4
    
    1|1 0|0 1|3
    
    2 0|4 2|2 4
    -         -
    1 2|3 4|4 3

### Solution 18
    6 2|6 2|3 6 2|2
    -         -
    5 2 2|4 4 6 6 5
      -     -   - -
    6 1 1|6 1 1 4 5
    -         -
    0 1|3 0|0 0 1|1
    
    3|3 4|5 0|5 3|6
    
    0|2 5 4 1|5 3 5
        - -     - -
    0|4 3 4 0|3 4 2

### Solution 19
    0|5 1|3 2|6 0|4
    
    4 0|6 5 3|6 0 6
    -     -     - -
    3 2|5 1 1|6 0 6
    
    4|5 4 5|5 0|2 1
        -         -
    2|2 4 2|3 4|1 1
    
    5|6 4|6 3 2 4|2
            - -
    0|1 3|5 3 1 3|0

### Solution 20
    0|4 2|6 2|5 0|5
    
    3 5|6 1|3 6|3 1
    -             -
    2 1|2 6 4|4 0 1
          -     -
    0|2 3 1 5|5 0 5
        -         -
    0|6 0 6 5 2|2 4
          - -
    3|4 1 4 1 6|6 5
        -         -
    2|4 0 3|3 1|4 3

## Adding Donimoes Solutions
Here are the solutions to the Adding Donimoes problems. For each step, move the
listed domino left, right, up, or down. Adding moves contain the domino
numbers, (H)orizontal or (V)ertical direction, and the position to place it.
The top left corner is 11, one space to the right is 21, and one space below is 12.

1. 36D, 23V21, 33D, 53V32, 25H21, 36D, 23D, 22H13, 33D, 53D, 22R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/
