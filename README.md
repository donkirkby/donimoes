# Donimoes: Puzzles with Dominoes
There are two kinds of puzzles: blocking and capturing. The goal of the
blocking puzzle is to slide all the dominoes into a rectangle, without sliding
any matching numbers next to each other. Each problem to solve is a pattern of
dominoes for you to start from, like this:

![Blocking example]

The goal of the capturing puzzle is to collect all the dominoes by sliding
matching numbers next to each other. You can only move dominoes that either
make a capture or add up to six. Here's an example:

![Capturing example]

To try the puzzle, get a set of dominoes. Then either [read the rules][rules],
or download [the PDF][pdf]. Choose the PDF if you want to print out pretty
diagrams of the problems, like these:

![Example problem and solution][solution example]

On the rules web page, the example problems above look like this:

      2    
      -
      3 1|2
    
    2|4    

and this:

    5 2|4
    -
    2 2|6

The example problem and solution looks like this:

    5 2|4   5 2|4     5 2|4   5 2*4
    -       -         -       *
    2 2|6   2   2>6   2 2<6   2 2*6

Donimoes is an original puzzle designed by Don Kirkby.

[rules]: https://donkirkby.github.com/donimoes/rules.html
[Blocking example]: https://donkirkby.github.com/donimoes/blocking_example.png
[Capturing example]: https://donkirkby.github.com/donimoes/capturing_example.png
[solution example]: http://donkirkby.github.com/donimoes/solution_example.png
[pdf]: https://donkirkby.github.com/donimoes/donimoes.pdf

## Other Domino Puzzles
The only other domino puzzle I could find is called either Dominosa or Domino
Solitaire. You start with a grid of numbers, and you have to lay the dominoes
on them. It was invented by O.S. Adler in 1874. There's an
[interesting proof][proof] that this puzzle is NP-hard.

Reiner Knizia published some puzzles called [Domino Knobelspass][knizia]
that are very similar to Dominosa.

[proof]: http://cs.stackexchange.com/q/16850/40884
[knizia]: https://boardgamegeek.com/boardgame/36738/domino-knobelspass
