from unittest.case import TestCase
from unittest.mock import patch

from hall_of_fame import MappedHallOfFame
from functools import total_ordering


@total_ordering
class DummyFitness(object):
    def __init__(self, *values):
        self.values = values

    def __lt__(self, other):
        return self.values < other.values

    def __eq__(self, other):
        return self.values == other.values

    def __repr__(self):
        return 'DummyFitness({}, {})'.format(*self.values)


class DummyIndividual(object):
    def __init__(self, fitness, solution_length):
        self.fitness = DummyFitness(fitness, solution_length)

    def __repr__(self):
        return 'DummyIndividual({}, {})'.format(*self.fitness.values)

    def __eq__(self, other):
        return (isinstance(other, DummyIndividual) and
                self.fitness == other.fitness)


@patch.object(MappedHallOfFame, 'log')
class MappedHallOfFameTest(TestCase):
    def test_logged(self, mock_log):
        hall = MappedHallOfFame(10)
        ind = DummyIndividual(100, 1)
        mock_log.assert_not_called()

        hall.update([ind])

        mock_log.assert_called_once_with(ind)

    def test_only_best_logged(self, mock_log):
        hall = MappedHallOfFame(10)
        ind1 = DummyIndividual(100, 1)
        ind2 = DummyIndividual(200, 2)
        mock_log.assert_not_called()

        hall.update([ind1, ind2])

        mock_log.assert_called_once_with(ind2)

    def test_not_logged_when_no_change(self, mock_log):
        hall = MappedHallOfFame(10)
        ind1 = DummyIndividual(200, 2)
        hall.update([ind1])
        ind2 = DummyIndividual(100, 1)
        mock_log.reset_mock()

        hall.update([ind2])

        mock_log.assert_not_called()

    def test_different_lengths_both_saved(self, mock_log):
        hall = MappedHallOfFame(10)
        ind1 = DummyIndividual(100, 1)
        ind2 = DummyIndividual(200, 2)

        hall.update([ind1, ind2])

        self.assertEqual(2, len(hall))

    def test_same_length_replaces(self, mock_log):
        hall = MappedHallOfFame(10)
        ind1 = DummyIndividual(100, 1)
        ind2 = DummyIndividual(200, 1)

        hall.update([ind1, ind2])

        self.assertEqual(1, len(hall))
