'''
整个系统的思路为:
(1) 构建好知识图谱
(2) 对question_str实体抽取, 得到关键词, 将关键词和实体类型(词性/词义)存在一个数据结构,
然后把question_str中的关键词用对应实体类型替换得到question_str1。举个例子，例如：
“周星驰是谁" 可以得到(周星驰，nr)，然后替换得到”nr是谁“这个更抽象的问题。
(3) 对于同一个语义问题，可以得到很多不同的表达形似，比如”nr是谁“，”谁是nr"都是一个意思。
我们把这个意思称为问题模板，我们先看看需要回答那些问题，建立问题模板集合。如何让实体抽取后的
问题映射到对应的模板上呢？我们先构建训练集，即每种模板可能的抽象实体问题，用分类器去训练它
最后，我们使用训练好的分类器就可以得到去实体问题的问题模板
(4)其实一个问题模板+实体关键词对应一个cql语句，查询并润色语言输出答案。
'''
import re
import jieba
import jieba.posseg
from classifier_model import Question_classify
from question_answer import Question_Answer

class Core:
    def __init__(self):
        '''
        加载自定义字典，里面存放了电影名、电影类型、演员和对应的词性nr、ng、nr
        因为电影问答的实体都是电影名、电影类型、演员名，种类有限，并且我们知道具体的内容，所以可以通过自定义
        字典在分词的方法来进行实体抽取工具;但是这种方法费事费力，并且条件苛刻，所以应该改进。
        '''
        jieba.load_userdict('data/mydict.txt')
        self.question_classify = Question_classify()
        self.question_answer = Question_Answer()

    #总函数
    def run(self, raw_question_str):
        clean_question_str = self.cleanQuestionStr(raw_question_str)
        extracted_question, key_dict = self.entityExtraction(clean_question_str)
        question_id = self.attributeMapping(extracted_question)
        answer = self.get_answer(question_id, key_dict)
        print(answer)

    #将脏问题字符串变成干净问题字符串
    def cleanQuestionStr(self, raw_question_str):
        clean_question_str = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+","",raw_question_str)
        return clean_question_str


    #对问题字符串进行实体抽取，返回抽取后的问题序列和(关键实体：实体类型)关键词字典
    def entityExtraction(self, question_str):
        key_dict = dict()
        extracted_question = []
        for token, pos in jieba.posseg.cut(question_str):
            if pos in {'nc', 'ni', 'ns', 'ne'}: 
                extracted_question.append(pos)
                key_dict[pos] = token
            else:
                extracted_question.append(token)
        return extracted_question, key_dict

    #对抽取后的问题进行属性映射得到问题模板编号
    def attributeMapping(self, extracted_question):
        return self.question_classify.predict_id(extracted_question)

    #根据问题模板编号+关键词字典得到答案
    def get_answer(self, question_id, key_dict):
        return self.question_answer.get_answer(question_id, key_dict)


if __name__ == "__main__":
    core = Core()
    raw_question_str = '华纺股份介绍'
    core.run(raw_question_str)