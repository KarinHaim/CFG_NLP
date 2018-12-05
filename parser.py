import nltk
from generate import PCFG
import sys


if __name__ == '__main__':
    pcfg = PCFG.from_file(sys.argv[1])

    stringGrammar = ""
    for lhs, rules_by_lhs in pcfg._rules.items():
        stringGrammar += lhs + " -> "
        for i, rule in enumerate(rules_by_lhs):
            stringGrammar += " ".join(rule[0])
            if len(rules_by_lhs) != i+1:
                stringGrammar += " | "
        stringGrammar += "\n"


    grammar = nltk.CFG.fromstring(stringGrammar)
    rd_parser = nltk.RecursiveDescentParser(grammar)
    sent = "Sally ate a sandwich"
    results = rd_parser.parse(sent)
    for tree in results:
        print(tree)

    #nltk.parse_cfg()


