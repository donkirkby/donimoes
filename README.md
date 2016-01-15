# Domiculture #
Domino puzzles where you weed explosive plants out of your garden.

Each puzzle is a pattern of dominoes for you to start from. The goal is to
remove all the dominoes by sliding matching numbers next to each other. There
are two ways a domino can move:

1. **Harvest** - move a domino one space along its long axis so that it ends
    up matching at least one of its numbers to an adjacent number on another
    domino. Then remove the moved domino and any dominoes with a number that
    matches an adjacent number on the moved domino.
2. **Replant** - move a domino one space along its long axis so that it ends
    up with at least one of its numbers next to an adjacent number that adds
    up to six. For example, a two can end up next to a four. No dominoes are
    removed.

There are two restrictions on domino movement:
1. All the dominoes must be in one connected group, you can't split the group
    after moving or after removing the matching dominoes.
2. The only way to move a domino is with a harvest or a replant.

This project is to build software that will generate interesting problems to
solve.

Domiculture is an original puzzle designed by Don Kirkby.

## Problems ##
Here are the starting positions for several Domiculture problems. The solutions
are listed at the end.

Problem 1

    0|5 0 1
        - -
    4|6 4 5
    
    4|2 4|1

Problem 2

    0 6 2|0
    - -
    5 5 5|3
    
    4 1|5 0
    -     -
    3 4|1 3

Problem 3

    6|0 1|5
    
    4|0 1 0
        - -
    2|1 6 3
    
    2|6 1|0



## Solutions ##
Here are the solutions. For each step, move the listed domino left, right, up,
or down. Then make captures for any matching numbers.

1. 42L, 41L, 15D, 15D, 04D, 05R, 42R, 05R
2. 43D, 05D, 05U, 53L, 03U, 53R
3. 40L, 21L, 26L, 10L, 40R, 15L, 03D, 15R, 03D

## Other Domino Puzzles ##
The only other domino puzzle I could find is called either Dominosa or Domino
Solitaire. You are provided a grid of numbers, and you have to lay the dominoes
on them. It was invented by O.S. Adler in 1874. There's an
[interesting proof][proof] that this puzzle is NP-hard.

Reiner Knizia published some puzzles called Domino Knobelspass on his web site
that are very similar to Dominosa. They've been taken down, but are still
available from the [Internet Archive][knizia].

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://web.archive.org/web/20140902223452/http://www.convivium.org.uk/kgcoolstuff.htm
