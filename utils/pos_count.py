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
        ADVERB = ['RB', 'RBR', 'RBS']

        # calculate total division
        and_count = []
        verb_count = []
        noun_count = []
        adj_count = []
        pp_count = []

        # calculate VP
        verb_prep_count = []
        adv_verb_count = []
        adv_coord_count = []
        veb_np_count = []

        # calculate NP
        adj_noun_count = []
        noun_noun_count = []
        det_noun_count = []
        noun____noun_count = []
        noun_prep_count = []
        noun_and_count = []

        adj_adv_count = []
        sbar_and = 0
        sbar_that = 0

        word_counter = 0
        all_pos = []
        src_file = open(self._source, "rt")                                          # open file
        for line in src_file:
            t1 = t2 = t3 = START
            w_pos = []
            for w_p in line.split():                                                 # break line to [.. (word, POS) ..]
                word, pos = w_p.rsplit("/", 1)
                w_pos.append((word, pos))
            # ALL
            verb = 0
            and_ = 0
            noun = 0
            adj = 0
            prep = 0

            # VP
            verb_prep = 0
            adv_verb = 0
            verb_np = 0
            adv_coord = 0

            # NP
            adj_noun = 0
            noun_noun = 0
            det_noun = 0
            noun____noun = 0
            noun_prep = 0
            noun_and = 0

            adj_adv = 0
            adj_adv_appear = NOUN
            for i, (word, pos) in enumerate(w_pos):
                all_pos.append(pos)
                word_counter += 1
                # ------- ALL ---------
                if pos in VERB:
                    verb += 1
                if pos in NOUN:
                    noun += 1
                if pos in ADJECTIVE:
                    adj += 1
                if pos in PREP:
                    prep += 1
                if word == "and" or word == "that":
                    and_ += 1

                # ------- VP ---------
                if t1 in VERB and pos in PREP:
                    verb_prep += 1
                if t1 in ADVERB and pos in VERB:
                    adv_verb += 1
                if (t2 in VERB and pos in NOUN) or (t1 in VERB and pos in NOUN):
                    verb_np += 1
                if word == "and" or word == "that":
                    adv_coord += 1

                # ------- VP ---------
                if t1 in VERB and pos in PREP:
                    verb_prep += 1
                if t1 in ADVERB and pos in VERB:
                    adv_verb += 1
                if (t2 in VERB and pos in NOUN) or (t1 in VERB and pos in NOUN):
                    verb_np += 1
                if t1 in VERB and (word == "and" or word == "that"):
                    adv_coord += 1

                # ------- NP ---------
                if t1 in ADJECTIVE and pos in NOUN:
                    adj_noun += 1
                if t1 in NOUN and (pos in DET or pos in ADJECTIVE):
                    noun_noun += 1
                if t1 in DET and pos in NOUN:
                    det_noun += 1
                if t2 in NOUN and pos in NOUN:
                    noun____noun += 1
                if t1 in NOUN and pos in PREP:
                    noun_prep += 1
                if t1 in NOUN and word == "and":
                    noun_and += 1

                if (t1 in ADVERB and pos in ADJECTIVE) or (t1 in ADJECTIVE and pos in ADVERB):
                    adj_adv += 1
                if pos in ADVERB or pos in ADJECTIVE:
                    adj_adv_appear = 1
                if word == "and":
                    sbar_and += 1
                if word == "that":
                    sbar_that += 1


                t3 = t2
                t2 = t1
                t1 = pos
            sum_all = verb + noun + and_ + prep + adj
            if sum_all:
                verb_count.append(verb / sum_all)
                noun_count.append(noun / sum_all)
                adj_count.append(adj / sum_all)
                and_count.append(and_ / sum_all)
                pp_count.append(prep / sum_all)

            sum_vp = verb_prep + adv_verb + verb_np
            if sum_vp:
                sum_vp += adv_coord
                verb_prep_count.append(verb_prep / sum_vp)
                adv_verb_count.append(adv_verb / sum_vp)
                adv_coord_count.append(adv_coord / sum_vp)
                veb_np_count.append(verb_np / sum_vp)

            sum_np = noun_and + noun_prep + noun____noun + det_noun + noun_noun + adj_noun
            if sum_np:
                adj_noun_count.append(adj_noun / sum_np)
                noun_noun_count.append(noun_noun / sum_np)
                det_noun_count.append(det_noun / sum_np)
                noun____noun_count.append(noun____noun / sum_np)
                noun_prep_count.append(noun_prep / sum_np)
                noun_and_count.append(noun_and / sum_np)

            if adj_adv_appear:
                adj_adv_count.append(adj_adv)


            # if det:
            #     npnp_count.append(npnp)
            # if noun:
            #     nn_count.append(nn)

        import numpy as npy
        vp = npy.mean(verb_count)
        np = npy.mean(noun_count)
        desk = npy.mean(adj_count)
        pp = npy.mean(pp_count)
        sbar = npy.mean(and_count)

        print("VP", vp, "%")
        print("NP", np, "%")
        print("DESC", desk, "%")
        print("PP", pp, "%")
        print("SBAR", sbar, "%")
        print("\n\n")

        verb_prep = int(100 * npy.mean(verb_prep_count) * vp * 0.4)
        adv_verb = int(100 * npy.mean(adv_verb_count) * vp * 0.4)
        adv_coord = int(100 * npy.mean(adv_coord_count) * vp * 0.4)
        veb_np = int(100 * npy.mean(veb_np_count) * vp * 0.4)

        print("VP PP", verb_prep, "%")
        print("ADV VP", adv_verb, "%")
        print("COORD/SBAR", adv_coord, "%")
        print("VP NP", veb_np, "%")
        print("\n\n")

        adj_noun = int(100 * npy.mean(adj_noun_count) * np * 0.4)
        noun_noun = int(100 * npy.mean(noun_noun_count) * np * 0.4)
        det_noun = int(100 * npy.mean(det_noun_count) * np * 0.4)
        noun____noun = int(100 * npy.mean(noun____noun_count) * np * 0.4)
        noun_prep = int(100 * npy.mean(noun_prep_count) * np * 0.4)
        noun_and = int(100 * npy.mean(noun_and_count) * np * 0.4)

        print("DESC NP", adj_noun, "%")
        print("NOUN NP", noun_noun, "%")
        print("DET NP", det_noun, "%")
        print("NP NP", noun____noun, "%")
        print("NP PP", noun_prep, "%")
        print("NP COORD", noun_and, "%")
        print("\n\n")

        adj_adv = int(100 * npy.mean(adj_adv_count) ** 0.5)
        and_that = sbar_and + sbar_that
        sbar_and = int(100 * sbar_and / and_that)
        sbar_that = int(100 * sbar_that / and_that)

        print("ADJ+ADV DESC", adj_adv, "%")
        print("SBAR COMP", sbar_that, "%")
        print("ADJ+ADV COORD", sbar_and, "%")

        print(list(sorted(set(all_pos))))


if __name__ == "__main__":
    import os
    g_count = GrammerCount(os.path.join("..", "src_files", "ass1-tagger-train"))
