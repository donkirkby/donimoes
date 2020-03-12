## Contributing ##
If you like Donimoes and want to make it better, help out. It could be as
simple as sending [@donkirkby][] a nice note on Twitter, you could report a bug,
or pitch in with some development work.

### Bug Reports and Enhancement Requests ###
Be as specific as possible. Which version are you using? What did you do? What
did you expect to happen? Are you planning to submit your own fix in a pull
request?

### New Domino Puzzles ###
Do you have an idea for another type of puzzle to include in Donimoes? Create
an issue, and describe how it would work.

### Development ###
Donimoes's software to generate puzzles is written in Python. It also depends
on the [NetworkX library][nx] and the
[Distributed Evolutionary Algorithms in Python library (DEAP)][deap], so those
need to be installed via pip or your package manager.

### Building a Release ###
Before publishing a release, check the following:

* The unit tests pass.
* All the instructions are up to date in the README and CONTRIBUTING files.

To publish a release:

* Run the `donimoes.py` script to generate the PDF version in the `docs` folder.
* Commit the changes and check that the new version works on the web site.
* Go to the GitHub [releases page][releases], create a new release using a tag
    like `vX.Y`.
* Close the milestone.

[@donkirkby]: http://twitter.com/donkirkby
[nx]: http://networkx.github.io/
[deap]: https://pypi.python.org/pypi/deap
[releases]: https://github.com/donkirkby/donimoes/releases
