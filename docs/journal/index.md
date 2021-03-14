---
title: Journal
subtitle: How we got here
hero_image: ../images/index_hero.jpg
---
## 2015 - Domiculture
I started the project with the idea that I could create something like the Rush
Hour puzzle that used a standard set of dominoes. They would move along their
long axis like the cars in Rush Hour, but instead of being constrained by a box,
they would have some restrictions on how they moved, related to their numbers.

My first idea was to require that each domino had to share a number with at
least one of their neighbours. I would generate a rectangular layout, make as
many moves as possible, and then print out the last board position. The goal
was to get the dominoes back into a rectangular layout. This was fine as a proof
of concept, but it wasn't easy to see where the legal moves were. I also wasn't
too happy with the name, Domiculture. My idea for a theme was growing plants and
harvesting them.

The second idea was to capture dominoes with matching numbers, a bit like the
old Shanghai solitaire computer game, but you have to move the tiles so that
the matching numbers touch before you can capture both dominoes. This was easier
to see, but the movement was a bit too restrictive when every move had to make
a capture. To allow for more movement options, I also allowed moves that didn't
capture if two neighbouring numbers add up to six.

## 2016 - Moonside
Until this point, I had just been generating random layouts, and reporting the
ones with the longest solutions. The next thing I tried was using evolutionary
search to make small changes to the best layouts, hoping to find similar,
slightly better layouts. I used a library called [DEAP], that offered lots of
features for evolutionary search, but I found its API very confusing.

I also started drawing diagrams, so I could eventually publish the problems
for other people to try. I think this was one of the first projects where I used
the turtle graphics support from my [live coding] project. It's fun, because it
updates the diagram as you change the code. I think it might also have been one
of the first times I used the GitHub pages feature to host a website.

I also changed the name to Moonside, an anagram of dominoes, and changed the
theme to mining on the moon. In the summer, I changed the name again, this time
to Donimoes. I decided to drop the theme.

[DEAP]: https://deap.readthedocs.io/en/master/
[live coding]: https://donkirkby.github.io/live-py-plugin/

## 2017 - Blocking Donimoes
My second successful puzzle, [Blocking Donimoes] was very similar to my first,
failed attempt. Requiring matching neighbours for all moves was too hard,
requiring matching numbers somewhere on a neighbouring domino was too hard to
see. What worked was to forbid matching neighbours. Each problem starts with a
stretched out layout, and you have to compress it into a rectangle without ever
letting matching numbers touch. This puzzle was later renamed to Unmatched
Donimoes, because there's a traditional game called Block Dominoes.

I experimented with the idea of [adding dominoes] from a queue, but it was too
hard. The idea was to make a puzzle that was faster to start solving, because
you didn't have to set up all the dominoes before starting. Instead, you added
them one at a time.

[Blocking Donimoes]: https://github.com/donkirkby/donimoes/issues/10
[adding dominoes]: https://github.com/donkirkby/donimoes/issues/15

## 2019 - Other People and Tetradominoes
During our summer travels, I found a book that included a domino game by Sid
Sackson: [Mountains and Valleys]. Around the same time, I heard that James Kyle
had ported [Fujisan] from the piecepack to dominoes. I decided to start
building a bigger game collection that included domino games and puzzles by
other designers, as well as my own.

The big task for this year was to add my first original game to the collection:
[Tetradominoes]. I was trying to come up with ways to combine the tetromino
shapes with the dominoes, and making a group of the two numbers on the domino
you just played seemed to work well. My favourite innovation was not letting
two of your tetrominoes touch. That let players build up a structure in the
shelter of their opponent's tetrominoes. It also creates a come-back mechanism.
I'd like to find more games or puzzles that use the tetrominoes.

[Mountains and Valleys]: https://github.com/donkirkby/donimoes/issues/23
[Fujisan]: https://github.com/donkirkby/donimoes/issues/24
[Tetradominoes]: https://github.com/donkirkby/donimoes/issues/16

## 2020 - Dominosa and Mirrors
I finally stopped being a snob and investigated the [Dominosa] puzzle. It turns
out, there are some interesting solving techniques that make it feel a lot like
a Sudoku. I wrote my search code to find problems at increasing sizes and also
made it find problems that required more and more of the different solving
techniques.

I also continued to adapt other people's games to use dominoes: [Cobra Paw] was
trivial to adapt from its custom dominoes to a traditional set. [Domino Finder]
was more loosely inspired by other memory games. I also included my favourite
traditional game: [All Fives].

I finally got frustrated enough with DEAP to build my own evolutionary search.
It doesn't have all the features of DEAP, but I find it much easier to use.

In the spring, during the pandemic, I worked on [Ladder Donimoes], moving
pieces on top of the dominoes for the first time, and inspired by boboquack's
[Magic Maze] on Puzzling.SE. It ended up being too hard, but it eventually
transformed into [Mirror Donimoes], a puzzle that I'm really pleased with.
Mirror Donimoes is the only puzzle where I can create problems by hand, because
it's clear enough to see the movement and goals. In fact, the hardest problems
had to be created by hand, because the computer solver can't handle them. I
enjoyed searching for the right rules, trying to balance several goals:

* Make the movement reversible, so you don't have reset the whole puzzle if you
  get stuck.
* Don't make the movement depend on numbers that are covered by the pieces. (I
  had to give up on this one.)
* Limit the number of movement options, so the choices aren't overwhelming.

[Dominosa]: https://github.com/donkirkby/donimoes/issues/22
[Cobra Paw]: https://github.com/donkirkby/donimoes/issues/43
[Domino Finder]: https://github.com/donkirkby/donimoes/issues/42
[All Fives]: https://github.com/donkirkby/donimoes/issues/28
[Ladder Donimoes]: https://github.com/donkirkby/donimoes/issues/31
[Mirror Donimoes]: https://github.com/donkirkby/donimoes/issues/52

## 2021 - Bees
[Bee Donimoes] started out as a game called Mephisto, by Christian Freeling.
I tried it out, but I didn't really like the movement mechanics. It has similar
goals and player interaction to Ricochet Robots, so I decided to keep that, and
look for a new set of movement mechanics. I settled on moving dice around on top
of the dominoes, and only letting them land on their own numbers. The key idea
is that the dice can modify each other's movement, similar to Ricochet Robots
and Fujisan. In this case, a die can turn a corner when it passes over another
die.

I originally made the blanks unusable, except for the blank on the same domino
as the queen. Looking for ways to simplify the rules, I tried to see whether
the special rules around blanks were actually helpful. I solved a thousand
problems at each size from three to six pips, and compared three possible rules
for blanks:

1. **touching** - This is the old rule, where only the blank on the queen's
   domino can be landed on. The others are all unusable.
2. **redeal** - This was an optional rule, where you can move the
   dominoes with blanks, so they don't touch each other. I implemented the test
   by redealing the layout until there weren't any touching each other.
3. **wild** - A new rule to test, where all blanks are wild, and you can land
   on them with any die.
   
I thought that making the blanks wild would be the simplest to explain, but I
was worried that it would make the solutions too easy to find. Here's what the
results looked like:

[![bee blanks]][bee blanks]

The wild blanks *did* make the solutions shorter, but only by about one move on
average. A solution length of -1 represents the unsolvable problems, and you can
see that the wild blanks make those much less likely, particularly with fewer
than six dice. I was surprised that the redeal had so little effect on the
solution length and solvability.

I decided to make the blanks wild in the standard rules for simplicity, and
add an advanced version with the queen's blank as the only wild one.

[bee blanks]: 2021/bee_blanks.png
[Bee Donimoes]: https://github.com/donkirkby/donimoes/issues/34
