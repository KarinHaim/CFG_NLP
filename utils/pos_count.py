import sys
sys.path.insert(0, "..")
START = "START"


class GrammerCount:
    def __init__(self, source_file):
        self._source = source_file
        # counters
        self._transition_count = self._get_data()

    def _get_data(self):
        NOUN = ['NN', 'NNP', 'NNPS', 'NNS']
        VERB = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        PREP = ['IN']
        DET = ['DT']
        ADJECTIVE = ['JJ', 'JJR', 'JJS']

        option2 = ([NOUN, VERB, NOUN], "VP, VERB, NP")
        option3 = ([VERB, PREP, NOUN], "NP, DET, NOUN")
        option4 = ([NOUN, NOUN, DET], "NP, NP, PP")     # VERB NP NP PP PP ->
        option5 = ([PREP, PREP, NOUN], "PP, PREP, NP")
        option6 = ([NOUN, ADJECTIVE, NOUN], "NOUN, ADJECTIVE, NOUN")

        npnp_count = []
        nn_count = []

        transition = {}
        word_counter = 0
        all_pos = []
        src_file = open(self._source, "rt")                                          # open file
        for line in src_file:
            t1 = t2 = t3 = START
            w_pos = []
            for w_p in line.split():                                                 # break line to [.. (word, POS) ..]
                word, pos = w_p.rsplit("/", 1)
                w_pos.append((word, pos))
            npnp = 0
            nn = 0
            noun = None
            det = None
            for i, (word, pos) in enumerate(w_pos):
                all_pos.append(pos)
                word_counter += 1
                # ------- TRANSITION ---------
                if pos in DET:
                    det = 1
                if pos in NOUN:
                    noun = 1
                transition[(t2, t1, pos)] = transition.get((t2, t1, pos), 0) + 1  # count(POS_0, POS_1, POS_2)
                if t3 in DET and t2 in NOUN and t1 in DET and pos in NOUN:
                    npnp += 1
                if t3 in ADJECTIVE and t2 in NOUN and t1 in ADJECTIVE and pos in NOUN:
                    nn += 1
                t3 = t2
                t2 = t1
                t1 = pos
            if det:
                npnp_count.append(npnp)
            if noun:
                nn_count.append(nn)

        import numpy as npy
        npnp = npy.mean(npnp_count)
        nn = npy.mean(nn_count)

        print("NP NP", npnp ** 0.5)
        print("ADJ NOUN ADJ NOUN", nn ** 0.5)

        print(list(sorted(set(all_pos))))
        return transition


if __name__ == "__main__":
    import os
    g_count = GrammerCount(os.path.join("..", "src_files", "ass1-tagger-train"))
