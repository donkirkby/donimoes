---
title: How Donimoes Are Made
subtitle: Evolutionary Search
---
If you try making up new Donimoes problems, you might find it hard to get the
dominoes to do what you want. Because there are two numbers on each domino and
you can only use each domino once, I found it hard to plan out a new problem.

Instead, I wrote a computer program to generate random layouts, solve them, and
then repeatedly make small changes to the best layouts, and solve them again.
This technique of making small, random changes to the best candidates is called
an evolutionary algorithm. I built mine on top of the [DEAP library].

In more detail:

1. Choose the size of layout I want to generate. For example, 4x4 cells.
    Remember, each domino has two cells.
2. Generate 1000 random layouts of dominoes that completely fill the target
    layout.
3. For each starting layout, explore the graph of all reachable positions by
    repeatedly applying all possible moves to each position. For the blocking
    puzzle, I start from the solution (a rectangle), and work backwards to the
    position farthest from the solution.
4. Calculate a score for each starting layout:
  * Could it be solved?
  * How long is the solution? (Longer is better.)
  * How many possible moves are there at each step in the solution? (Fewer is
    better.)
5. Print the best score so far. Print out the best starting layouts, if the
    user asked for it.
6. Choose the layouts with the best scores (about half of them), and generate
    new layouts. New layouts are made by removing a small number of dominoes,
    then randomly replacing them with new ones.
7. Go back to step 4 for all the new layouts.

That's it! I just run it until the scores stop improving, then I print out the
results. I also have a script to convert a text layout into a diagram. You can
see all the source code in the [repository].

[DEAP library]: https://deap.readthedocs.io/en/master/
[repository]: https://github.com/donkirkby/donimoes
