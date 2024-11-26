import random


class Chromosome:  # 染色体，每一个染色体就代表一组不同的小箱子的索引
    def __init__(self, size):  # size是小盒子个数，bin是大盒子的个数
        a = [i for i in range(size)]
        random.shuffle(a)
        self.gene = a  # 将小箱子排序
        self.fitness = 1

    def set_gene(self, gene):
        self.gene = gene

    def size_down_gene(self):  # 缩小大盒子个数
        last_bin = max(self.gene)  # 最后一个大盒子
        new_gene = []
        if (last_bin > 0):
            new_gene = list(map(lambda x: x if x < last_bin else random.randint(0, last_bin - 1),
                                self.gene))  # 如果在最后一个大盒子里，就将它放在前面的大盒子里
        self.gene = new_gene

    def __lt__(self, other):
        if (self.fitness < other.fitness):
            return True
        return False

    def __eq__(self, other):
        return self.fitness == other.fitness

