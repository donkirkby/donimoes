---
title: Dominosa
---
The domino puzzle I most often see in books or online is called either Dominosa
or Domino Solitaire. It was invented by O.S. Adler in 1874, and each problem
starts with a grid of numbers. You have to lay out the dominoes so they match
the numbers, without duplicated or missing dominoes.

One thing I find interesting about this puzzle is that it's easier to solve with
pencil and paper than with a set of dominoes. I created this separate file for
you to print out, if you don't want to write in the book. It doesn't include the
strategy hints or the solutions from the book.

#### Example
Here's a small problem to start with.

    0 0 1
    
    1 1 0

Every problem uses a complete set of dominoes up to the highest number you see.
In this small problem, the highest number is one, so there are three dominoes:

    0 x 0 x 1
    -   -   -
    0 x 1 x 1

When you start solving, most dominoes will usually have more than one place they
could go. For example, the blank/one domino could go in a few different places,
including these three:

    0 0 1 x 0 0|1 x 0 0 1
    -                 -
    1 1 0 x 1 1 0 x 1 1 0

However, some dominoes will only have one possible place, like the double blank:

    0|0 1
    
    1 1 0

Once you've placed a domino, check to see if it forces any other dominoes. In
this case, the top right corner only has one space it can connect to:

    0|0 1
        -
    1 1 0

That makes the final domino obvious, and the solution looks like this:

    0|0 1
        -
    1|1 0

I took a long time to add this puzzle to the
collection, because I found it tedious to keep searching for unique numbers.
After some research, though, I learned that people have found many other
techniques for solving that aren't as tedious. Try to work out your own
techniques as you solve these problems, then read my techniques in the book. Let
me know if you find any new ones. Even with all those tricks, it's not trivial
to solve. (In computer science, it's called [NP-hard][np].)

If you like this style of puzzle, Reiner Knizia published some puzzles called
[Domino Knobelspass][knizia] that are very similar to Dominosa.

[np]: http://cs.stackexchange.com/q/16850/40884
[pdf]: https://donkirkby.github.io/donimoes/donimoes.pdf
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass

#### Problem 1
    2 2 1 2
           
    0 0 1 0
    
    1 2 0 1

#### Problem 2
    0 1 0 1 3
    
    3 1 0 2 2
    
    3 2 1 0 3
    
    2 3 1 0 2

#### Problem 3
    3 0 1 1 0 4
    
    2 4 4 1 1 2
    
    2 4 2 2 1 4
    
    3 3 4 0 0 3
    
    3 0 2 1 3 0

#### Problem 4
    0 2 1 1 2
    
    0 0 1 3 2
    
    0 0 3 1 3
    
    3 3 1 2 2

#### Problem 5
    3 4 0 1 1 2
    
    1 2 2 2 4 4
    
    1 0 0 3 2 3
    
    1 4 2 4 0 4
    
    0 0 3 3 1 3

#### Problem 6
    1 2 3 3 0 3
    
    0 3 0 4 4 4
    
    0 2 4 2 3 3
    
    1 4 1 4 1 2
    
    2 2 1 0 0 1

#### Problem 7
    2 5 0 0 2 4 3
    
    4 1 5 0 3 3 2
    
    0 1 2 2 4 1 4
    
    4 1 0 5 1 5 3
    
    4 0 2 0 1 5 5
    
    3 3 1 2 3 5 4

#### Problem 8
    3 5 0 1 3 4 5
    
    3 1 4 1 3 3 0
    
    3 1 5 0 0 2 4
    
    0 4 0 2 5 5 2
    
    2 2 1 5 2 4 4
    
    3 0 1 5 1 2 4

#### Problem 9
    1 2 4 2 3 4
    
    1 4 4 1 3 3
    
    2 2 0 1 0 3
    
    0 4 0 3 3 1
    
    2 4 0 1 0 2

#### Problem 10
    1 2 4 2 3 1
    
    1 3 2 0 0 1
    
    4 4 3 3 2 2
    
    3 0 4 0 1 4
    
    0 2 4 0 3 1

#### Problem 11
    5 1 3 2 3 1 1
    
    0 5 4 5 2 2 5
    
    4 2 4 1 2 4 3
    
    3 4 2 0 0 4 3
    
    5 0 1 4 0 3 3
    
    5 1 5 2 0 0 1

#### Problem 12
    3 4 3 3 1 5 2
    
    0 4 0 0 2 3 0
    
    0 5 2 2 4 1 5
    
    3 4 5 4 3 5 2
    
    2 1 0 3 1 5 5
    
    4 4 1 2 0 1 1

#### Problem 13
    6 0 6 4 1 3 4 5
    
    4 6 4 4 1 2 2 2
    
    6 2 2 0 2 0 3 3
    
    3 5 6 6 0 4 5 1
    
    5 1 2 6 5 5 3 0
    
    0 3 3 2 3 1 6 0
    
    1 5 5 4 0 1 1 4

#### Problem 14
    1 5 6 2 2 2 6 2
    
    4 1 5 5 3 3 2 6
    
    3 0 2 2 0 3 5 4
    
    1 3 1 4 4 3 6 3
    
    0 5 4 5 3 1 1 6
    
    4 0 6 4 0 0 0 6
    
    0 5 5 1 1 6 2 4

#### Problem 15
    0 0 1 3 1 1
    
    4 0 2 2 3 2
    
    3 4 3 3 3 2
    
    4 4 2 4 0 4
    
    0 0 1 1 2 1

#### Problem 16
    2 3 2 2 3 3
    
    3 0 1 4 1 1
    
    0 2 3 4 4 1
    
    2 1 0 4 2 0
    
    0 4 4 1 3 0

#### Problem 17
    0 2 3 1 2 5 5
    
    3 5 0 4 1 1 3
    
    4 4 4 2 0 5 3
    
    1 1 3 2 3 2 5
    
    4 5 0 0 0 4 2
    
    1 5 3 4 0 1 2

#### Problem 18
    3 4 0 5 2 3 3
    
    0 0 2 4 5 0 3
    
    3 0 4 1 3 0 5
    
    5 5 3 5 1 1 2
    
    4 4 1 2 2 2 4
    
    1 5 1 4 2 0 1

#### Problem 19
    2 3 4 4 1 3 2 5
    
    6 6 0 5 5 5 3 3
    
    6 4 3 6 1 4 6 0
    
    2 3 2 4 2 5 1 1
    
    5 6 5 4 1 2 6 0
    
    0 0 5 0 2 2 4 6
    
    1 1 3 3 0 1 4 0

#### Problem 20
    0 6 0 1 4 4 3 6
    
    2 6 6 0 5 2 6 3
    
    3 4 1 1 2 2 5 0
    
    3 5 5 3 6 6 0 4
    
    1 1 1 3 4 2 3 6
    
    1 5 0 2 1 5 4 4
    
    0 0 3 5 2 4 2 5

### Contributing
Found some interesting problems to solve? Ideas to share? Get in touch at
[https://donkirkby.github.io/donimoes][github].

These problems for O.S. Adler's Dominosa were designed by [Don Kirkby][don].

[github]: https://donkirkby.github.io/donimoes
[don]: https://donkirkby.github.io/
