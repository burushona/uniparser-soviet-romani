try:
    from importlib.resources import files, as_file
except ImportError:
    from importlib_resources import files, as_file
from uniparser_morph import Analyzer
from uniparser_morph.wordform import Wordform

from .borrowings import BorrowingAnalyzer


class SovietRomaniAnalyzer(Analyzer):
    def __init__(self, mode='strict', verbose_grammar=False,
                 analyse_borrowings=False):
        """
        Initialize the analyzer by reading the grammar files.
        If mode=='strict' (default), load the data as is.
        If mode=='nodiacritics', load the data for (possibly) diacriticless texts.
        If analyse_borrowings==False (default), analyze unknown Russian noun
        borrowings with pymorphy3.
        """
        super().__init__(verbose_grammar=verbose_grammar)
        self.mode = mode
        self.analyseBorrowings = analyse_borrowings
        if mode not in ('strict', 'nodiacritics'):
            return
        self.dirName = 'uniparser_soviet_romani.data_' + mode
        with as_file(files(self.dirName) / 'paradigms.txt') as self.paradigmFile,\
             as_file(files(self.dirName) / 'lexemes.txt') as self.lexFile,\
             as_file(files(self.dirName) / 'lex_rules.txt') as self.lexRulesFile,\
             as_file(files(self.dirName) / 'derivations.txt') as self.derivFile,\
             as_file(files(self.dirName) / 'stem_conversions.txt') as self.conversionFile,\
             as_file(files(self.dirName) / 'clitics.txt') as self.cliticFile,\
             as_file(files(self.dirName) / 'bad_analyses.txt') as self.delAnaFile:
            self.load_grammar()
        if self.analyseBorrowings:
            self.borrowingAnalyzer = BorrowingAnalyzer(self.g)

    def analyze_words(self, words, format=None, disambiguate=False):
        """
        Analyze a single word or a (possibly nested) list of words. Return either a list of
        analyses (all possible analyses of the word) or a nested list of lists
        of analyses with the same depth as the original list.
        If format is None, the analyses are Wordform objects.
        If format == 'xml', the analyses for each word are united into an XML string.
        If format == 'json', the analyses are JSON objects (dictionaries).
        """
        # if disambiguate:
        #     with as_file(files(self.dirName) / 'soviet_romani_disambiguation.cg3') as cgFile:
        #         cgFilePath = str(cgFile)
        #         return super().analyze_words(words, format=format, disambiguate=True,
        #                                      cgFile=cgFilePath)
        analyses = super().analyze_words(words, format=None, disambiguate=False)
        if self.analyseBorrowings:
            self._add_borrowing_analyses(analyses)
        if format == 'xml':
            self.analyses_to_xml(analyses)
        elif format == 'json':
            self.analyses_to_json(analyses)
        elif format == 'conll':
            analyses = self.analyses_to_conll(analyses)
        return analyses

    def _add_borrowing_analyses(self, analyses):
        if not isinstance(analyses, list):
            return
        if (len(analyses) == 1 and isinstance(analyses[0], Wordform)
                and not analyses[0].lemma):
            borrowing = self.borrowingAnalyzer.analyze(analyses[0].wf)
            if borrowing is not None:
                analyses[0] = borrowing
            return
        for item in analyses:
            self._add_borrowing_analyses(item)


if __name__ == '__main__':
    pass
