from pymorphy3 import MorphAnalyzer
from uniparser_morph.wordform import Wordform


SUFFIXES = (
    (('obl', 'm', 'sg'), 'с'),
    (('gen', 'm', 'sg'), 'скирэ'),
    (('gen', 'm', 'sg'), 'скир'),
    (('gen', 'm', 'sg'), 'скр'),
    (('gen', 'f', 'sg'), 'кир'),
    (('gen', 'f', 'sg'), 'кр'),
    (('dat', 'm', 'sg'), 'скэ'),
    (('dat', 'f', 'sg'), 'кэ'),
    (('ins', '', 'sg'), 'са'),
    (('loc', 'm', 'sg'), 'стэ'),
    (('loc', 'f', 'sg'), 'тэ'),
    (('abl', 'm', 'sg'), 'стыр'),
    (('abl', 'f', 'sg'), 'тыр'),
    (('obl', '', 'pl'), 'н'),
    (('gen', '', 'pl'), 'нгир'),
    (('gen', '', 'pl'), 'нгр'),
    (('abl', '', 'pl'), 'ндыр'),
    (('dat', '', 'pl'), 'нгэ'),
    (('loc', '', 'pl'), 'ндэ'),
    (('ins', '', 'pl'), 'нса'),
    (('ins', '', 'pl'), 'нца'),
    (('voc', '', 'pl'), 'лэ'),
)

GENDERS = {'masc': 'm', 'femn': 'f', 'neut': 'n', None: ''}
NUMBERS = {'sing': 'sg', 'plur': 'pl', None: ''}


class BorrowingAnalyzer:
    """Analyze Russian nouns carrying Soviet Romani case suffixes."""

    def __init__(self, grammar):
        self.grammar = grammar
        self.morph = MorphAnalyzer()

    def analyze(self, word):
        word_no_yo = word.replace('ё', 'е').replace('Ё', 'Е')

        for grammar, suffix in SUFFIXES:
            if not word.lower().endswith(suffix):
                continue
            stem_end = len(word) - len(suffix)
            stems = [word[:stem_end], word[:stem_end - 1],
                     word_no_yo[:stem_end], word_no_yo[:stem_end - 1]]
            if word[:stem_end].endswith('ь'):
                stems.append(word[:stem_end - 2])
            for stem in dict.fromkeys(stems):
                analysis = self._analyze_stem(stem, grammar, word)
                if analysis is not None:
                    return analysis

        if word.lower().endswith(('ё', 'о', 'э')):
            analysis = self._analyze_stem(word[:-1], ('', '', 'dir'), word,
                                          lemma=word)
            if analysis is not None:
                return analysis

        return self._analyze_stem(word, ('', '', ''), word)

    def _analyze_stem(self, stem, grammar, word, lemma=''):
        if not stem:
            return None
        russian_stem = stem.replace('жэ', 'же').replace('жы', 'жи').replace('шы', 'ши')
        russian_stem = russian_stem.replace('Жэ', 'Же').replace('Жы', 'Жи').replace('Шы', 'Ши')
        russian = self.morph.parse(russian_stem)[0]

        if russian.tag.POS != 'NOUN':
            return None
        if not word.istitle() and (not russian.is_known or russian.score < 0.2):
            return None

        case, forced_gender, forced_number = grammar
        gender = forced_gender or GENDERS.get(russian.tag.gender, '')
        number = forced_number or NUMBERS.get(russian.tag.number, '')
        wordform = Wordform(self.grammar, wf=word)
        wordform.lemma = lemma or russian.normal_form
        wordform.gramm = ','.join(tag for tag in ('N', 'rus', gender, case, number)
                                 if tag)
        wordform.wfGlossed = word.lower()
        if case:
            wordform.wfGlossed = russian_stem + '-' + word[len(stem):]
        wordform.otherData.append(('trans_ru', russian.normal_form))
        return wordform
