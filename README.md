# Moonside: Mining Puzzles with Dominoes #
Domino puzzles where you collect explosive moonstones.

Each puzzle is a pattern of dominoes for you to start from. The different
numbers on the dominoes are different kinds of moonstones, and the goal is to
collect all the dominoes by sliding matching numbers next to each other.

![Beginner puzzle][example1]

To try the puzzles, get a set of dominoes. Then either [read the rules][rules],
or download [the PDF][pdf]. Choose the PDF if you want to print out pretty
diagrams of the puzzles, like these:

![Example puzzle and solution][example2]

On the rules web page, the beginner puzzle above looks like this:

    0|5 0 1
        - -
    4|6 4 5
    
    4|2 4|1

The example puzzle and solution look like this:

    5 2|4   5 2|4     5 2|4   5 2*4
    -       -         -       *
    2 2|6   2   2>6   2 2<6   2 2*6

Moonside is an original puzzle designed by Don Kirkby.

[rules]: http://donkirkby.github.com/moonside/rules.html
[example1]: http://donkirkby.github.com/moonside/example1.png
[example2]: http://donkirkby.github.com/moonside/example2.png
[pdf]: http://donkirkby.github.com/moonside/moonside.pdf

## Other Domino Puzzles ##
The only other domino puzzle I could find is called either Dominosa or Domino
Solitaire. You are provided a grid of numbers, and you have to lay the dominoes
on them. It was invented by O.S. Adler in 1874. There's an
[interesting proof][proof] that this puzzle is NP-hard.

Reiner Knizia published some puzzles called [Domino Knobelspass][knizia]
that are very similar to Dominosa.

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass
