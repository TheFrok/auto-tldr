from collections import Counter

WORDS_BLACKLIST = set(["hwa", "el", "la", "yl", "at", "ki", "zh"])


class WordCounter(object):
    def __init__(self, article):
        """
        creates an objects that counts the word of an
        :param article: morph_xml.MorphArticle
        """
        self._words = Counter()
        for word in article.words:
            self._words.update(word.optional_bases)
        for sentence in article.sentences:
            sentence.score = self.get_sentence_score(sentence)

    def get_all_scores(self):
        return self._words.items()

    def get_base_word_score(self, word_base):
        if word_base in WORDS_BLACKLIST:
            return 0
        return self._words[word_base]

    def get_word_score(self, word):
        """
        returns the score of the highest scored base form of a word
        :param word: morph_xml.MorphWord
        :return: int
        """
        if len(word.optional_bases) == 0:
            return 0
        return max([self.get_base_word_score(base) for base in word.optional_bases])

    def get_sentence_score(self, sentence):
        """
        return the sum of the scores of all the words in the sentence
        :param sentence: Sentence
        :return: int
        """
        return sum([self.get_word_score(word) for word in sentence.words])


class Sentence(object):
    def __init__(self, words, sentence_id):
        """
        creates a representation of a sentence in the article
        :param words: list of morph_xml.MorphWord
        :param sentence_id: int
        """
        self.order_id = sentence_id
        self.score = None
        self.words = words

    def to_text(self):
        text = ""
        for rep in self.words:
            rep = rep.text
            text += rep
            if rep.isalnum() or len(rep) > 1:
                text += u" "
        return text.encode("utf8")
