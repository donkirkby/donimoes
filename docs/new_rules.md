---
title: New Rules for Donimoes
---
# Experiments in Progress
These are new puzzles that aren't finished yet. You can try them out and let me
know what you think.

## Tetradominoes
The game of life, the universe, and everything, for 2, 3, or 4 players.

### Equipment
* a set of double-six dominoes
* for 3 players, a set of 3 tokens in each of 3 colours
* for 2 or 4 players, a set of 2 or 4 tokens, half light and half dark
* seven cardboard tetrominoes (white on one side, black on the other)

The tokens are only needed when playing with three players, and they should be
small enough to fit on top of a domino.

To make your own set of tetrominoes, draw these seven shapes on a piece of
plain cardboard, and cut them out. Use a marker to colour one side of each
shape. Each shape should be big enough fit on top of four domino numbers, with a
small gap around the outside.

    ###  ##  ####
    #   ##
             #
    #   ##  ## ##
    ###  ##  # ##

### Object
Play the most tetrominoes, or block your opponents from playing.

### Setup
Shuffle the dominoes face down, and each player flip one face up. Add the
numbers, and check if there are any ties. Continue flipping and adding until
there are no ties, then sit around the table from highest total down to lowest
total, in a clockwise direction. The player with the highest total will play
first.

In a 2-player game, the player with the highest total takes the light token and
plays first. The other player takes the dark token. In a 3-player game, the
player with the highest total plays first, and each player takes all the tokens
of one colour. In a 4-player game, the player with the highest total takes a
light token and plays first. The other players take a dark token, a light token,
and a dark token, alternating around the table. Players with the same colour
tokens will play as partners.
 
Shuffle the dominoes face down, and draw four for each player, keeping them
hidden from the other players. Put the remaining dominoes and the tetrominoes
within reach.

### Playing Dominoes
On the first turn, play any domino you like. On each turn after that, you must
play a domino so that at least one of its numbers is adjacent to a matching
number on a domino that was already played, and isn't covered. If there are no
numbers uncovered at the start of your turn, you lose. If none of your dominoes
match the available numbers, reveal two of your hidden dominoes, and draw one
more, keeping it hidden from the other players. If you still can't play, repeat
until you can. If you still can't play when there are no more dominoes to draw
or when you don't have two hidden dominoes, you lose. Leave any revealed
dominoes face up.

### Playing Tetrominoes
After playing a domino, see if you can play a tetromino. It must cover at least
one number on the domino you just played, and the rest of it must cover numbers
that match one of the numbers on the domino you just played. Also, two of your
tetrominoes can't be right next to each other. (Diagonal is OK.)

With 2 or 4 players, if you have a light token, you must play tetrominoes with
the light side up. If you have a dark token, you must play with the dark side
up. With three players, all players play tetrominoes with the light side up, and
then place one of their tokens on the tetromino.

### Game End
With 2 or 4 players, the game ends when one player or team plays four
tetrominoes and wins. With 3 players, the game ends when one player plays three
tetrominoes and wins.

Otherwise, a player can lose by being unable to play, either because there are
no numbers to match or because none of the dominoes match the available numbers.

With 3 players, a player who leaves no numbers uncovered wins the game. If a
player doesn't have any matching numbers and can't draw any, they are eliminated
and the other two players continue without them.

### Variant
Tournament play is a series of games until one player wins seven points. One
point for each tetromino, plus a bonus point if your opponent is unable to play.


## The Adding Puzzle's Goal ##
The goal is to add all the dominoes from the queue onto the board. Each problem
shows the queue of dominoes to add, from left to right.

## Start ##
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

## Moves ##
There are only two ways a domino can move.

### Adding ###
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

### Sliding ###
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

### Stay Connected ###
All the dominoes on the board must stay in one connected group, you can't split the group
after moving a domino.

## Problems ##
Here are the starting positions for several Capturing Donimoes problems. The
solutions are listed at the end.

### Problem 1 ###
    2 3 5 4 5 2
    - - - - - -
    1 5 1 5 5 4

## Adding Solutions ##
Here are the solutions to the Adding Donimoes problems. For each step, move the
listed domino left, right, up, or down. Adding moves contain the domino
numbers, (H)orizontal or (V)ertical direction, and the position to place it.
The top left corner is 11, one space to the right is 21, and one space below is 12.

1. 36D, 23V21, 33D, 53V32, 25H21, 36D, 23D, 22H13, 33D, 53D, 22R

Donimoes is an original puzzle designed by [Don Kirkby][don].

[don]: https://donkirkby.github.com/
