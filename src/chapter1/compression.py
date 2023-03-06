from sys import getsizeof
from time import perf_counter_ns


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1  # start with sentinel
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # shift left two bits
            if nucleotide == "A":  # change last two bits to 00
                self.bit_string |= 0b00
            elif nucleotide == "C":  # change last two bits to 01
                self.bit_string |= 0b01
            elif nucleotide == "G":  # change last two bits to 10
                self.bit_string |= 0b10
            elif nucleotide == "T":  # change last two bits to 11
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide:{}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):  # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11  # get just 2 relevant bits
            if bits == 0b00:  # A
                gene += "A"
            elif bits == 0b01:  # C
                gene += "C"
            elif bits == 0b10:  # G
                gene += "G"
            elif bits == 0b11:  # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene[::-1]  # [::-1] reverses string by slicing backwards

    def __str__(self) -> str:  # string representation for pretty printing
        return self.decompress()


def compress_gene(gene: str) -> int:
    bit_string: int = 1  # start with sentinel
    for nucleotide in gene.upper():
        bit_string <<= 2  # shift left two bits
        if nucleotide == "A":  # change last two bits to 00
            bit_string |= 0b00
        elif nucleotide == "C":  # change last two bits to 01
            bit_string |= 0b01
        elif nucleotide == "G":  # change last two bits to 10
            bit_string |= 0b10
        elif nucleotide == "T":  # change last two bits to 11
            bit_string |= 0b11
        else:
            raise ValueError("Invalid Nucleotide:{}".format(nucleotide))

    return bit_string


def benchmark():
    trails = 100
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100

    class_start = perf_counter_ns()
    for i in range(trails):
        class_compression = CompressedGene(original)

    class_stop = perf_counter_ns()

    function_start = perf_counter_ns()
    for i in range(trails):
        function_compression = compress_gene(original)

    function_stop = perf_counter_ns()

    class_time = class_stop-class_start
    function_time = function_stop-function_start

    print("Class\tFunction")
    print("{}ns\t{}ns".format(class_time, function_time))

    print("The function was faster by {}ns".format(class_time-function_time))


if __name__ == "__main__":
    BENCHMARK = True
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100

    class_start = perf_counter_ns()
    class_compression = CompressedGene(original)
    class_stop = perf_counter_ns()

    function_start = perf_counter_ns()
    bit_string = compress_gene(original)
    function_stop = perf_counter_ns()

    print("With class size is {}, and took {}ns".format(
        getsizeof(class_compression.bit_string), class_stop-class_start))

    print("With function size is {}, and took {}ns".format(
        getsizeof(bit_string), function_stop-function_start))

    if BENCHMARK:
        benchmark()
