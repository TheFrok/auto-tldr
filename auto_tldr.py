from collections import Counter

from morph_xml import MorphArticle, JAR_SRC_FILE
from words_count import WordCounter, Sentence


def main():
    article = MorphArticle(r"source.txt")
    word_count = WordCounter(article)
    sentences_score = Counter()
    for sentence in article.sentences:
        sentences_score.update({sentence: sentence.score})
    with open("output.test", "wb") as f:
        for sentence in sentences_score.most_common(5):
            f.write(sentence[0].to_text())
            f.write(b"\n")
    print("number of sentences: ", len(article.sentences))
    print("number of words: ", len(article.words))
    print("Five most common words are: ", word_count._words.most_common(5))
    with open("count.csv", "wb") as f:
        for word, score in word_count.get_all_scores():
            f.write(b",".join([word.encode("utf8"), str(score).encode("utf8")]))
            f.write(b"\r\n")


if __name__ == '__main__':
    main()
