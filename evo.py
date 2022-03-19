# Based on https://github.com/Garve/Evolutionary-Algorithm
from abc import ABC, abstractmethod
from datetime import datetime


class Individual(ABC):
    def __init__(self, value: dict = None, init_params: dict = None):
        if value is not None:
            self.value = value
        else:
            self.value = self._random_init(init_params)

    @abstractmethod
    def pair(self, other, pair_params):
        pass

    @abstractmethod
    def mutate(self, mutate_params):
        pass

    @abstractmethod
    def _random_init(self, init_params):
        pass


class Population:
    def __init__(self, size, fitness, individual_class, init_params):
        self.fitness = fitness
        self.individuals = [individual_class(init_params=init_params) for _ in range(size)]
        self.sort()
        self.replace_count = 0
        self.unimproved_count = 0  # Number of times replace() didn't improve.

    @property
    def best_fitness(self):
        return self.fitness(self.individuals[-1])

    @property
    def is_stale(self):
        return (10 < self.replace_count and
                (self.replace_count // 2) < self.unimproved_count)

    def sort(self):
        self.individuals.sort(key=lambda x: self.fitness(x))

    def replace(self, new_individuals):
        start_best = self.best_fitness
        size = len(self.individuals)
        self.individuals.extend(new_individuals)
        self.sort()
        self.individuals = self.individuals[-size:]
        end_best = self.best_fitness
        self.replace_count += 1
        if start_best < end_best:
            self.unimproved_count = 0
        else:
            self.unimproved_count += 1

    def get_parents(self, n_offsprings):
        mothers = self.individuals[-2 * n_offsprings::2]
        fathers = self.individuals[-2 * n_offsprings + 1::2]

        return mothers, fathers


class Evolution:
    def __init__(self,
                 pool_size,
                 fitness,
                 individual_class,
                 n_offsprings,
                 pair_params,
                 mutate_params,
                 init_params,
                 pool_count: int = 1):
        self.pair_params = pair_params
        self.mutate_params = mutate_params
        self.pool_size = pool_size
        self.fitness = fitness
        self.individual_class = individual_class
        self.init_params = init_params
        self.pool_count = pool_count
        self.pools = []
        self.add_pools()
        self.n_offsprings = n_offsprings
        self.history = []

    @property
    def pool(self):
        return self.pools[0]

    def add_pools(self):
        while len(self.pools) < self.pool_count:
            self.pools.append(Population(self.pool_size,
                                         self.fitness,
                                         self.individual_class,
                                         self.init_params))

    def step(self):
        is_stale = False
        for pool in self.pools:
            mothers, fathers = pool.get_parents(self.n_offsprings)
            offsprings = []

            for mother, father in zip(mothers, fathers):
                offspring = mother.pair(father, self.pair_params)
                offspring.mutate(self.mutate_params)
                offsprings.append(offspring)

            pool.replace(offsprings)
            is_stale = is_stale or pool.is_stale

        if 1 < self.pool_count and is_stale:
            self.pools.sort(key=lambda p: (-p.best_fitness, p.unimproved_count))
            while 1 < len(self.pools) and self.pools[-1].is_stale:
                self.pools.pop()
            self.add_pools()

    @staticmethod
    def is_finished():
        """ Called after each epoch of evolution. Return true to stop. """
        return False

    def run(self, max_epochs: int):
        start_time = datetime.now()
        self.history.clear()
        for epoch_count in range(max_epochs):
            top_individual = self.pool.individuals[-1]
            top_fitness = self.pool.fitness(top_individual)
            mid_fitness = self.pool.fitness(
                self.pool.individuals[-len(self.pool.individuals) // 5])
            summaries = []
            for pool in self.pools:
                pool_fitness = pool.fitness(pool.individuals[-1])
                total = pool_fitness
                summaries.append(f'{total}')
            self.history.append(top_fitness)
            self.print_step_summaries(top_individual,
                                      top_fitness,
                                      mid_fitness,
                                      summaries)
            self.step()
            if self.is_finished():
                break

        duration = datetime.now() - start_time
        self.print_final_summary(duration)

    def print_final_summary(self, duration):
        best = self.pool.individuals[-1]
        for problem in self.pool.individuals:
            print(self.pool.fitness(problem))
        solution = best.value['start']
        print(solution)
        print(f'Finished {len(self.history)} epochs in {duration}.')

    def print_step_summaries(self, top_individual, top_fitness, mid_fitness, summaries):
        print(len(self.history),
              top_fitness,
              mid_fitness,
              repr(top_individual.value['start']),
              ', '.join(summaries))
