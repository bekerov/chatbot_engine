import pickle
from datetime import datetime
import collections

import numpy as np
from sklearn import svm, grid_search, datasets
from sklearn.decomposition.pca import PCA
from konlpy.tag import Twitter

VOCABULARY_SIZE = 50000

# 3가지
# BOW & SVM
# CNN
# Doc2Vec

class QueryClassifier(object):

    def __init__(self):
        self.pos_tagger = Twitter()
        self.classifier = None
        self.dictionary = None
        self.reverse_dictionary = None

    def classify(self, query):
        query = self.convert_sentence_BOW(query)
        result = int(self.classifier.predict(query.reshape(1,-1))[0])

        return result

    def build_dataset(self, words, vocabulary_size):
        
        count = [['UNK', -1]]
        count.extend(
            collections.Counter(words).most_common(
                vocabulary_size - 1))
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)

        data = list()
        unk_count = 0
        for word in words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
                unk_count = unk_count + 1
            data.append(index)
        count[0][1] = unk_count
        reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        del words  # Hint to reduce memory.

        return data, count, dictionary, reverse_dictionary

    def train(self, sentence_list, label_list, vocabulary_size=VOCABULARY_SIZE):

        X_train = []
        for sentence in sentence_list:
            X_train.append(self.tokenize(sentence))

        words = [ word for line in X_train for word in line]
        # memory of words is deleted after build_dataset function
        data, count, self.dictionary, self.reverse_dictionary = self.build_dataset(words, vocabulary_size)

        train_x = np.array([ self.convert_word_list_to_BOW(x) for x in X_train])
        train_y = np.array(label_list)

        parameters = {'kernel':['linear','rbf'], 'C':[0.1,1,2,3,4,5,6,7,8,9 ,10]}
        classifier_origin = svm.SVC()
        self.classifier = grid_search.GridSearchCV(classifier_origin, parameters)
        self.classifier.fit(train_x, train_y)
 

    def read_txt_and_train(self, file_path, vocabulary_size=VOCABULARY_SIZE):

        def read_data(path):
            with open(path, "rt") as f:
                lines = f.readlines();
                result = []
                for line in lines:
                    result.append(self.tokenize(line))  
            
            return result

        data_set = read_data(file_path)
        self.train(data_set, vocabulary_size)

    def tokenize(self, doc):
        return [t[0] for t in self.pos_tagger.pos(doc, norm=True, stem=True)]


    def convert_word_list_to_BOW(self, sentence):
        bow = np.zeros(len(self.dictionary))
        for word in sentence:
            if word in self.dictionary:
                bow[self.dictionary[word]] = 1

        return bow


    def convert_sentence_BOW(self, sentence):
        sentence = self.tokenize(sentence)
        bow = self.convert_word_list_to_BOW(sentence)
                
        return bow

    def save(self, file_path=None):
        if file_path == None:
            pass
        else:
            save_path = file_path

        save_data = {
                        'classifier' : self.classifier,
                        'dictionary' : self.dictionary,
                        'reverse_dictionary' : self.reverse_dictionary,
                    }

        with open(save_path, "wb") as f: 

            pickle.dump(save_data, f)

        return save_path

    def load(self, file_path):
        with open(file_path, "rb") as f:
            load_data = pickle.load(f)

            self.classifier = load_data['classifier']
            self.dictionary = load_data['dictionary']
            self.reverse_dictionary = load_data['reverse_dictionary']


def test_case_save_load_run():
    import os 

    def test_case_save_and_run():
        print("save_run test case : ...")
        query_classifier = QueryClassifier()
        query_classifier.read_txt_and_train("./data/train.txt")
        save_path = query_classifier.save()

        test_case_query(query_classifier)
        print("done!")

        return save_path

    def test_case_load_and_run(file_path):
        print("load_run test case : ...")
        query_classifier = QueryClassifier()
        query_classifier.load(file_path)

        test_case_query(query_classifier)

        print("done!")

    def test_case_query(query_classifier):
        assert(query_classifier.classify("2015년 12월부터 3일까지 삼성전자 주식 알려줘") == 1)
        assert(query_classifier.classify("요즘 엘지 주가 어떤지 아세요?") == 1)
        assert(query_classifier.classify("현대 증권 주가 보여줘") == 1)
        assert(query_classifier.classify("토니모리 요즘 주가 어때?") == 1)
        assert(query_classifier.classify("대한민군 안녕하세요 뭘 테스트라고적지") == 0)
        assert(query_classifier.classify("어느 순간 퇴근 하하하") == 0)
        assert(query_classifier.classify("하하하하하 엘지 요즘 어떤지 아냐") == 0)
        assert(query_classifier.classify("이상한 소리 들은것 같아 ㅋㅋㅋ") == 0)
        assert(query_classifier.classify("다들 너무하시네 등을 돌릴 수가 있지?") == 0)
        assert(query_classifier.classify("오늘 신문 보여줘") == 2)
    data_path = test_case_save_and_run()
    test_case_load_and_run(data_path)

    #os.remove(data_path)


if __name__ == '__main__':
    test_case_save_load_run()
