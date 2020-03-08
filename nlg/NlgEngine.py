from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *


class NlgEngine:

    def __init__(self):
        self.realise = Realiser(host='nlg.kutlak.info', port=40000)

    def example(self):
        p = Clause(NP('Solar System'), VP('be discover'), NP('in the 16th Century'))
        p['TENSE'] = 'PAST'
        print(self.realise(p))

nlg = NlgEngine()
nlg.example()