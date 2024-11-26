from chromosome_2 import Chromosome

import functools
from In_Package_2 import in_package
from item_2 import item


import random
import bisect
import math
import time
import tkinter as tk


class GeneticsAlgoritham:

    def __init__(self, sign, generation_size, recombination, mutation, max_generations, stop_criterium, squares,
                 package_order, cut_in_y,label):
        self.squares = squares  # 输入的Item列表
        self.chromosomes = []
        self.package_order = package_order
        self.generation_size = generation_size  # 产生基因数量
        self.number_of_squares = len(squares)
        self.cut_in_y = cut_in_y
        # self.number_of_bins=number_of_bins
        for index in range(0, generation_size):
            if index == 0:
                a = Chromosome(self.number_of_squares)
                sequence = item.order_len(self.squares)
                a.gene = sequence
                self.chromosomes.append(a)
            elif index == 1:
                a = Chromosome(self.number_of_squares)
                sequence = item.order_square(self.squares)
                a.gene = sequence
                self.chromosomes.append(a)
            elif index == 2:
                a = Chromosome(self.number_of_squares)
                sequence = item.order_totallen(self.squares)
                a.gene = sequence
                self.chromosomes.append(a)
            else:
                self.chromosomes.append(Chromosome(self.number_of_squares))
        self.recombination = recombination
        self.mutation = mutation
        # self.size_down=size_down
        self.max_generations = max_generations
        self.stop_criterium = stop_criterium ** 2
        self.best_chromosome = None
        self.best_fitness = 1
        # self.bin_size_x=bin_size_x
        # self.bin_size_y=bin_size_y
        self.log = []
        self.sign =sign
        self.label = label

    def find_best_solution(self, ):
        TIME1 = time.perf_counter()
        number_of_generation = 0
        self.find_best_fitness_for_generation()
        TIME2 = time.perf_counter()
        self.log.append(self.best_fitness)  # 将最好的利用率存入

        while (self.max_generations > number_of_generation and self.stop_criterium >= self.best_fitness):  # 当利用率最大或所有染色体都判断完后，结束循环

            self.chromosomes.sort(reverse=True)

            # frame1 = tk.Frame(root)
            # frame1.pack()
            #
            # label2 = tk.Label(frame1,text="0")
            # label2.pack()
            # label2['text'] = f'Generation {number_of_generation}: Best fitness: {self.best_fitness}'
            if number_of_generation % 20 == 0:
                print(f'Generation {number_of_generation}: Best fitness: {self.best_fitness}')
                self.sign.emit(f'Generation {number_of_generation}: Best fitness: {self.best_fitness}')
            # if(number_of_generation%5==0):

            number_of_generation += 1

            elite_number = int(self.generation_size - self.generation_size * self.recombination)  # 0.2的重组概率
            new_generation = self.chromosomes[:elite_number]  # 保留前面利用率好的部分

            roulette_wheel = self.generate_roulette_wheel()  # 轮盘赌法，确定各个染色体重组的概率
            new_generation_size = len(new_generation)

            while (new_generation_size < self.generation_size):  # 直到产生150个染色体组
                parents = self.generate_parents(roulette_wheel)  # 按正态分布抽取父母染色体
                child = self.generate_children(parents, self.mutation)  # 利用基因重组等到子染色体
                new_generation.append(child)
                # new_generation.append(child2)
                new_generation_size += 1

            if (new_generation_size < self.generation_size):
                new_generation_size.pop()

            self.chromosomes = new_generation
            self.find_best_fitness_for_generation()  # 从新的染色体组中找到最好的染色体
            self.log.append(self.best_fitness)
        TIME3 = time.perf_counter()
        print(TIME2-TIME1,TIME3-TIME2)
        return self.best_chromosome

    # def find_usage(self):
    #     value=math.modf(self.best_fitness)
    #     return (1+value[0])

    def find_best_fitness_for_generation(self):

        generation_best_fitness = 1
        best_chromosome_in_generation = None
        for chromosome in self.chromosomes:

            # max_bin=max(chromosome.gene)+1 #找到所有染色体上最多需要的盒子数
            # pack=BinPacking(self.squares,max_bin,chromosome.gene,self.bin_size_x,self.bin_size_y)
            chromosome.fitness, _, _ = in_package(self.squares, chromosome.gene, self.cut_in_y, self.package_order, False)
            # pack.pack_squares_in_bins()#将所有的小盒子放在大盒子里面
            # chromosome.fitness=pack.fitness_check()

            if (
                    generation_best_fitness == 1 or generation_best_fitness < chromosome.fitness):  # 找到fitness（利用率）最大的那一组染色体
                generation_best_fitness = chromosome.fitness
                best_chromosome_in_generation = chromosome

        if (generation_best_fitness > self.best_fitness or self.best_fitness == 1):  # 找到历次最好的fitness
            self.best_fitness = generation_best_fitness
            self.best_chromosome = best_chromosome_in_generation

        return generation_best_fitness

    def generate_roulette_wheel(self):
        roulette_wheel = []
        edge = 0
        min_value = math.floor(self.chromosomes[-1].fitness)
        sum_of_fitness = sum(chromosome.fitness for chromosome in self.chromosomes) - (
                min_value * len(self.chromosomes))
        for index, chromosome in enumerate(self.chromosomes):
            edge += ((chromosome.fitness - min_value) / sum_of_fitness)
            roulette_wheel.append(edge)
        return roulette_wheel

    def generate_parents(self, roulette_wheel):
        selector = random.uniform(0, 1)
        a = self.chromosomes[bisect.bisect_left(roulette_wheel, selector)]
        # selector=random.uniform(0, 1)
        # b=self.chromosomes[bisect.bisect_left(roulette_wheel, selector)]
        return a

    def generate_children(self, parent, mutation):
        child = Chromosome(self.number_of_squares)
        # child2=Chromosome(self.number_of_squares,self.number_of_bins)
        break_point = random.randint(0, self.number_of_squares - 1)  # 将染色体分为两半
        child.set_gene(parent.gene[break_point:] + parent.gene[:break_point])  # 重组

        rand_mutation = random.uniform(0, 1)
        if (rand_mutation < mutation):  # 变异的概率为0.5，每次变异只改变一位
            rand_position1 = random.randint(0, self.number_of_squares - 1)  # 随机变异的位置
            rand_position2 = random.randint(0, self.number_of_squares - 1)
            while (rand_position1 == rand_position2):
                rand_position2 = random.randint(0, self.number_of_squares - 1)

            # last_bin=max(child1.gene)
            child.gene[rand_position1], child.gene[rand_position2] = child.gene[rand_position2], child.gene[
                rand_position1]
            # rand_position=random.randint(0,self.number_of_squares-1)
            # last_bin=max(child2.gene)
            # child2.gene[rand_position]=random.randint(0,last_bin)

        # rand_size_down=random.uniform(0, 1) #根据最少的盒子数来随机
        # if(rand_size_down<size_down):
        #     if(self.best_fitness>0):
        #         print('a')
        #     max_bin=math.floor(-self.best_fitness)+1 #找到最少需要的盒子数
        #     child1=Chromosome(self.number_of_squares,max_bin) #随机生成一组队列

        return child

#
# def printf(self, mes):
#     self.textBrowser.append(mes)  # 在指定的区域显示提示信息
#     self.cursot = self.textBrowser.textCursor()
#     self.textBrowser.moveCursor(self.cursot.End)
#     QApplication.processEvents()
