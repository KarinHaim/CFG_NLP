from collections import defaultdict
import random
from utils.parameters import DEBUG


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol, to_break=False):
        if self.is_terminal(symbol):
            return symbol, " " + symbol if to_break else symbol
        else:
            expansion = self.random_expansion(symbol)
            out_origin = []
            out_part3 = " (" + symbol
            for s in expansion:
                ext = self.gen(s, to_break=to_break)
                out_part3 += ext[1]
                out_origin.append(ext[0])
            out_part3 += ")"
            return " ".join(out_origin), out_part3 if to_break else " ".join(out_origin)

    def random_sent(self, to_break=False):
        return self.gen("ROOT", to_break=to_break)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r


if __name__ == '__main__':
    import sys
    args = sys.argv
    if DEBUG:
        args = ["nn", "../Part1/grammer", "-n", "5", "-t"]

    # check if -t entered
    break_flag = False
    if "-t" in args:
        break_flag = True
        args.remove("-t")

    # check if -n entered
    grammer_file = args[1]
    num_sentences = 1
    if len(args) > 2 and args[2] == "-n":
         num_sentences = int(args[3])

    # create PCFG object
    pcfg = PCFG.from_file(args[1])

    for _ in range(num_sentences):
        sentence, seq = pcfg.random_sent(to_break=break_flag)
        print(sentence)
        print(seq)

