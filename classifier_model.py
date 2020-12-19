import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import os
import re
import jieba

# 获取所有的文件
def getfilelist(root_path):
    file_path_list=[]
    file_name=[]
    walk = os.walk(root_path)
    for root, dirs, files in walk:
        for name in files:
            filepath = os.path.join(root, name)
            file_name.append(name)
            file_path_list.append(filepath)
    return file_path_list

class Question_classify:
    def __init__(self):
        self.X_train = []
        self.y_train = []
        self.pipeline = Pipeline(steps=[
            ('tv', TfidfVectorizer()),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        self.read_train_data();
        self.train_model_NB();

    def read_train_data(self):
        for filepath in getfilelist('./data/train_data'):
            num = int(re.sub(r'\D', "", filepath))
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    word_list = list(jieba.cut(line.strip()))
                    self.X_train.append(' '.join(word_list))
                    self.y_train.append(num)
        return self.X_train, self.y_train
                    
    def train_model_NB(self):
        self.pipeline.fit(self.X_train, self.y_train)
    
    def predict_id(self, extracted_question):
        return self.pipeline.predict([' '.join(extracted_question)])[0]


if __name__ == "__main__":
    question_classify = Question_classify()
    extracted_question = ['ns', '是', '谁']
    print(question_classify.predict_id(extracted_question))

