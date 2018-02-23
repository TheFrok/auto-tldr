import os
import shutil
import subprocess
from words_count import Sentence
from xml.etree import ElementTree

# paths
MORPH_LIB_PATH = r"D:\Files\Java\morphAnalayzer"
JAR_SRC_FILE = os.path.join(MORPH_LIB_PATH, "source.txt")
JAR_OUT_FILE = os.path.join(MORPH_LIB_PATH, "analyzed_source.xml")
TOKENIZER_JAR = os.path.join(MORPH_LIB_PATH, "tokenizer.jar")
MORPH_ANALYZER_JAR = os.path.join(MORPH_LIB_PATH, "morphAnalyzer.jar")
# cmd lines
TOKENIZER_CMD = ["java", "-Xmx1024m", "-jar", TOKENIZER_JAR]  # need to add input file and output file
MORPH_ANALYZER_CMD = ["java", "-Xmx1G", "-jar", MORPH_ANALYZER_JAR, "false"]  # need to add input file and output file


class MorphArticle(object):
    # paths
    MORPH_LIB_PATH = r"D:\Files\Java\morphAnalayzer"
    JAR_SRC_FILE = os.path.join(MORPH_LIB_PATH, "source.txt")
    JAR_OUT_FILE = os.path.join(MORPH_LIB_PATH, "analyzed_source.xml")
    TOKENIZER_JAR = os.path.join(MORPH_LIB_PATH, "tokenizer.jar")
    MORPH_ANALYZER_JAR = os.path.join(MORPH_LIB_PATH, "morphAnalyzer.jar")
    # cmd lines
    TOKENIZER_CMD = ["java", "-Xmx1024m", "-jar", TOKENIZER_JAR]  # need to add input file and output file
    MORPH_ANALYZER_CMD = ["java", "-Xmx1G", "-jar", MORPH_ANALYZER_JAR,
                          "false"]  # need to add input file and output file

    def __init__(self, text_file_path):
        self.article_xml = MorphArticle.create_morph_xml(text_file_path)
        self.sentences = []
        for sentence_xml in self.article_xml.iter("sentence"):
            order = sentence_xml.attrib["id"]
            words = [MorphWord(word_xml) for word_xml in sentence_xml.iter("token")]
            self.sentences.append(Sentence(words, order))

    @property
    def words(self):
        words = []
        for sentence in self.sentences:
            words += sentence.words
        return words

    @staticmethod
    def create_morph_xml(input_file, output_file=''):
        if input_file != JAR_SRC_FILE:
            shutil.copy(input_file, JAR_SRC_FILE)
        temp_path = os.path.join(MORPH_LIB_PATH, os.path.basename(input_file)) + ".xml"
        subprocess.run(TOKENIZER_CMD + [JAR_SRC_FILE, temp_path])
        subprocess.run(MORPH_ANALYZER_CMD + [temp_path, JAR_OUT_FILE], cwd=MORPH_LIB_PATH)
        os.remove(temp_path)
        if output_file:
            shutil.copy(JAR_OUT_FILE, output_file)
        return ElementTree.parse(JAR_OUT_FILE)


class MorphWord(object):
    def __init__(self, word_xml):
        self.xml = word_xml
        self.text = word_xml.attrib["surface"]
        self.word_type = MorphWord._get_word_type
        self.optional_bases = MorphWord._get_word_optional_base_forms(word_xml)

    @staticmethod
    def _get_word_type(word_xml):
        """
        types can be word, number, punctuation
        :param word_xml: ElementTree xml
        :return: str
        """
        if len(list(word_xml.iter("numeral"))) > 0:
            return "number"
        elif len(list(word_xml.iter("punctuation"))) > 0:
            return "punctuation"
        return "word"

    @staticmethod
    def _get_word_optional_base_forms(word_xml):
        if MorphWord._get_word_type(word_xml) == "punctuation":
            return set()
        elif MorphWord._get_word_type(word_xml) == "number":
            return word_xml.attrib["surface"]
        options = set()
        for opt_base in word_xml.iter("base"):
            attributes = opt_base.attrib
            if "transliteratedLexiconItem" in attributes:
                opt = attributes["transliteratedLexiconItem"]
                options.add(opt)
        return options
