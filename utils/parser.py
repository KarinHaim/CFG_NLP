import nltk
import sys
from utils.generate import PCFG
from utils.parameters import DEBUG

if __name__ == '__main__':
    args = sys.argv
    if DEBUG:
        args = ["nn", "../Part1/grammar"]
    pcfg = PCFG.from_file(args[1])

    stringGrammar = ""
    for lhs, rules_by_lhs in pcfg._rules.items():
        stringGrammar += lhs + " -> "
        for i, rule in enumerate(rules_by_lhs):
            cfg_format_rule = ["'" + t + "'" if pcfg.is_terminal(t) else t for t in rule[0]]
            stringGrammar += " ".join(cfg_format_rule)
            if len(rules_by_lhs) != i+1:
                stringGrammar += " | "
        stringGrammar += "\n"

    grammar = nltk.CFG.fromstring(stringGrammar)
    rd_parser = nltk.RecursiveDescentParser(grammar)
    sent = ['the', 'president', 'kissed', 'a', 'pickle', '!']
    results = rd_parser.parse(sent)
    for tree in results:
        print(tree)

    #nltk.parse_cfg()


