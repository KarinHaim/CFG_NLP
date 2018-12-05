
class GrammerNode:
    def __init__(self, phrase):
        self._phrase_name = phrase

    def tostring(self):
        raise NotImplementedError()


class PhraseNode(GrammerNode):
    def __init__(self, phrase: str, right: GrammerNode, left: GrammerNode):
        super(PhraseNode, self).__init__(phrase)
        self._right = right
        self._left = left

    def tostring(self):
        return "( " + self._phrase_name + self._left.tostring() + " " + self._right.tostring() + " )"


class TerminalNode(GrammerNode):
    def __init__(self, term_type: str, word: str):
        super(TerminalNode, self).__init__(term_type)
        self._word = word

    def tostring(self, gap=0):
        w_str = "(" + self._phrase_name + " " + self._word + ")"
        return w_str

class GrammerTree:
    def __init__(self, root):

