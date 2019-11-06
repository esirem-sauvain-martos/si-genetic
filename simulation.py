# -*- coding: utf-8 -*-

from population import Population
from individual import Individual
from random import random

class Simulation:
    
    def __init__(self, population_size, individual_size, delta = 0.01, mutation_probability = 0.5):
        self.population_size = population_size
        self.population = Population(population_size, individual_size)
        self.global_fitness_records = []
        self.convergence_value = 0
        self.delta = delta
        self.mutation_probability = mutation_probability

    def run_simulation(self):
        self.population.genesis()
        generation = 1
        self.population.eval_population()
        while not self.has_converged():
            selection = self.selection()
            children = self.crossing(selection)
            self.mutation(children)
            self.replace_population(children)
            self.population.eval_population()
            global_fitness = self.population.get_global_fitness(normalized=True)
            self.global_fitness_records.append(global_fitness)
            print("Gen {}, global fitness : {}".format(generation, global_fitness))
            generation += 1


    def has_converged(self):
        """ Calcul la convergence de l'algorithme """

        has_converged = True if self.population.get_global_fitness(normalized = True) == 1.0 else False

        if len(self.global_fitness_records) != 0 and not has_converged:
            new_convergence_value = sum(self.global_fitness_records) / len(self.global_fitness_records)
        
            if abs(new_convergence_value - self.convergence_value) < self.delta:
                has_converged = True
            self.convergence_value = new_convergence_value
        
        return has_converged


    def replace_population(self, children):
        """ Réalise l'opération de remplacement """

        new_population = [None] * self.population_size

        self.population.individuals.sort(key = lambda i: i.fit_score)
        children.sort(key = lambda i: i.fit_score, reverse = True)

        limit_new_population = (int)(self.population_size * 0.8)
        new_population[:limit_new_population] = children[:limit_new_population]

        need = self.population_size - limit_new_population
        new_population[limit_new_population:] = self.population.individuals[need:2 * need]

        self.population.individuals = new_population
        


    def selection(self):
        """ Réalise l'opération de séléction """

        selection = []
        for _ in range(2):
            self.population.shuffle()
            for i in range(self.population_size - 1):
                selection.append(Individual.oppose(
                    self.population.individuals[i],
                    self.population.individuals[i + 1]
                ))

                i += 1

        return selection


    
    def crossing(self, selection):
        """ Réalise l'opération de croisement """

        children = []
        for i in range(len(selection) - 1):
            children.extend(Individual.reproduce(
                selection[i],
                selection[i + 1],
                break_point_count = 2
            ))

            i += 1

        return children


    def mutation(self, individuals):
        """ Réalise les mutations """

        for individual in individuals:
            if individual.get_fitness(normalized = True) < 0.5 and random() < self.mutation_probability:
                individual.mutate()
                
