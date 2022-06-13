# Soviet Romani morphological analyzer
This is a rule-based morphological analyzer for Soviet Romani (the macrolanguage has the ISO code ``rom``; Indo-European > Indo-Aryan). It is based on a formalized description of literary Soviet Romani morphology and uses [uniparser-morph](https://github.com/timarkh/uniparser-morph) for parsing. It performs full morphological analysis of Soviet Romani words (lemmatization, POS tagging, grammatical tagging).

## How to use
### Python package
The analyzer is available as a Python package. If you want to analyze Soviet Romani texts in Python, install the module:

```
pip3 install uniparser-soviet-romani
```

Import the module and create an instance of ``SovietRomaniAnalyzer`` class. Set ``mode='strict'`` if you are going to process text in standard orthography, or ``mode='nodiacritics'`` if you expect some words to lack the diacritics. After that, you can either parse tokens or lists of tokens with ``analyze_words()``, or parse a frequency list with ``analyze_wordlist()``. Here is a simple example:

```python
from uniparser_udmurt import SovietRomaniAnalyzer
a = SovietRomaniAnalyzer(mode='strict')

analyses = a.analyze_words('Морфологиез')
# The parser is initialized before first use, so expect
# some delay here (usually several seconds)

# You will get a list of Wordform objects
# The analysis attributes are stored in its properties
# as string values, e.g.:
for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm, ana.gloss)

# You can also pass lists (even nested lists) and specify
# output format ('xml' or 'json')
# If you pass a list, you will get a list of analyses
# with the same structure
analyses = a.analyze_words([['А'], ['Мон', 'тонэ', 'яратӥсько', '.']],
	                       format='xml')
analyses = a.analyze_words(['Морфологиез', [['А'], ['Мон', 'тонэ', 'яратӥсько', '.']]],
	                       format='json')
```

Refer to the [uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/) for the full list of options.

### Word lists
Alternatively, you can use a preprocessed word list. The ``wordlists`` directory contains a list of words from a 720-thousand-word [Soviet Romani corpus](http://web-corpora.net/RomaniCorpus/search/) (``wordlist.csv``), list of analyzed tokens (``wordlist_analyzed.txt``; each line contains all possible analyses for one word in an XML format), and list of tokens the parser could not analyze (``wordlist_unanalyzed.txt``). The recall of the analyzer on the corpus texts is about XX%.

## Description format
The description is carried out in the ``uniparser-morph`` format and involves a description of the inflection (paradigms.txt), a grammatical dictionary (rom_lexemes.txt files), a description of productive derivations (rom_derivations.txt), and a list of clitics (rom_clitics.txt). The dictionary contains descriptions of individual lexemes, each of which is accompanied by information about its stem, its part-of-speech tag and some other grammatical/borrowing information, its inflectional type (paradigm), and Russian translation. See more about the format [in the uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/format.html).
