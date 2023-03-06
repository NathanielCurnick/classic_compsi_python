from enum import IntEnum
from typing import Tuple, List
from time import perf_counter_ns
from numpy.random import choice

Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]  # type alias for codons
Gene = List[Codon]  # type alias for genes


def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):  # don't run off end!
            return gene
        #  initialize codon out of three nucleotides
        codon: Codon = (Nucleotide[s[i]],
                        Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)  # add codon to gene
    return gene


def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if codon == key_codon:
            return True
    return False


def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high:  # while there is still a search space
        mid: int = (low + high) // 2
        if gene[mid] < key_codon:
            low = mid + 1
        elif gene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False


def benchmark(trails: int):
    gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT" * 1000
    my_gene: Gene = string_to_gene(gene_str)

    linear_contains_start = perf_counter_ns()
    for _ in range(trails):
        codon = (choice(Nucleotide), choice(Nucleotide), choice(Nucleotide))
        linear_contains(my_gene, codon)
    linear_contains_end = perf_counter_ns()

    my_sorted_gene: Gene = sorted(my_gene)

    binary_contains_start = perf_counter_ns()
    for _ in range(trails):
        codon = (choice(Nucleotide), choice(Nucleotide), choice(Nucleotide))
        binary_contains(my_sorted_gene, codon)
    binary_contains_end = perf_counter_ns()

    linear_time = linear_contains_end-linear_contains_start
    binary_time = binary_contains_end-binary_contains_start

    print("Linear search took {}ns".format(linear_time))
    print("Binary time took {}ns".format(binary_time))

    percent = (linear_time - binary_time) / linear_time

    print("Binary search is {}% faster".format(percent * 100))


if __name__ == "__main__":
    BENCHMARK = True

    if BENCHMARK:
        benchmark(100)
    else:
        gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"
        my_gene: Gene = string_to_gene(gene_str)
        acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
        gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
        print(linear_contains(my_gene, acg))  # True
        print(linear_contains(my_gene, gat))  # False
        my_sorted_gene: Gene = sorted(my_gene)
        print(my_sorted_gene)
        print(binary_contains(my_sorted_gene, acg))  # True
        print(binary_contains(my_sorted_gene, gat))  # False
