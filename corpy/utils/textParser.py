from MeCab import Tagger
import re
import unicodedata
import numpy as np


# 正規表現のコンパイルやTaggerの生成などの繰り返し処理をコンストラクタでやりたい
class TextParser():
    def __init__(self, sep=' '):
        self.tagger = Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/ -Ochasen")
        self.pat = re.compile('[!-/:-@≠\[-`{-~\t\s\n　]')
        self.sep = sep

    def cleanse(self, text):
        normalized = lambda: unicodedata.normalize('NFKC', text).upper()
        cleansed = lambda: re.sub(self.pat, ' ', normalized()) # 記号をけすと変な感じで文字がくっつく
        return cleansed()

    def parseToFeature(self, text):
        cleansed = lambda: self.cleanse(text)
        p = self.tagger.parseToNode(cleansed())

        while p != None:
            feature = tuple(p.feature.rsplit(','))
            yield (p.surface, feature[6], feature[0], feature[1])
            p = p.next

    # 使える品詞のものだけ原型で返すジェネレータ
    def parse(self, text):
        cleansed = lambda: self.cleanse(text)
        p = self.tagger.parseToNode(cleansed())

        while p != None:
            feature = tuple(p.feature.rsplit(','))
            if feature[0] == '名詞':
                if feature[1] != '数':
                    yield p.surface

            elif feature[0] == '動詞':
                if feature[1] not in ['接尾', '非自立']:
                    yield feature[6]

            elif feature[0] == '形容詞':
                yield feature[6]

            elif feature[0] == '副詞':
                yield feature[6]

            p = p.next

    def parseToArray(self, text):
        out = lambda: np.array([w for w in self.parse(text)])
        return out()

    def parseToString(self, text):
        out = lambda: self.sep.join([w for w in self.parse(text)])
        return out()

    # 入力テキストをbag of words(tupple)に変換する
    def parseToBow(self, text):
        arr = self.parseToArray(text)
        bow = [(w, sum(arr == w)) for w in np.unique(arr)]
        return bow


class ParsedConverter():
    @staticmethod
    def stringToBow(string, sep=' '):
        arr = np.array(string.split(sep))
        bow = [(w, sum(arr == w)) for w in np.unique(arr)]
        return bow

    @staticmethod
    def bowToString(bow, sep=' '):
        getRepeat = lambda x: ((x[0] + sep) * x[1]).rstrip()
        string = sep.join([getRepeat(b) for b in bow])
        return string
