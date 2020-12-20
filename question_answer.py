from py2neo import Graph

class Question_Answer:
    def __init__(self):
        #连接数据库
        self.graph = Graph('http://localhost:7474/browser/', username='neo4j', password='Serena')
        #每一种问题类型用一种函数来处理
        self.func_dict={ 
            0: self.get_stock_introduction,
            1: self.get_executive_introduction
        }

    def get_answer(self, question_id, key_dict):
        if question_id >= len(self.func_dict):
            return '问题的回答超出我的能力范围!'
        return self.func_dict[question_id](key_dict)

    def get_stock_introduction(self, key_dict):
        #异常处理
        if 'ns' not in key_dict.keys():
            return '问题的回答超出我的能力范围!'
        cql = 'match (p:企业) where p.name=\'{}\' return p.code'.format(key_dict['ns'])
        result = self.graph.run(cql).data()
        code = result[0]['p.code']
        cql = 'match (p:企业)-[:行业属于]->(i:行业) where p.name=\'{}\' return i.name'.format(key_dict['ns'])
        result = self.graph.run(cql).data()
        industry = result[0]['i.name']
        cql = 'match (p:企业)-[:概念属于]->(c:概念) where p.name=\'{}\' return c.name'.format(key_dict['ns'])
        result = self.graph.run(cql).data()
        concept = result[0]['c.name']
        cql = 'match (n:高管)-[:董事会成员]->(p:企业) where p.name=\'{}\' return n.name'.format(key_dict['ns'])
        result = self.graph.run(cql).data()
        executives = '、'.join([item['n.name'] for item in result])
        answer = '{}企业的企业代码为{};\n该企业的高管团队成员有{};\n该企业从事{}和属于{}概念。'.format(key_dict['ns'], code, executives, industry, concept)
        return answer


    def get_executive_introduction(self, key_dict):
        if 'ne' not in key_dict.keys():
            return '问题的回答超出我的能力范围!'
        cql = 'match (n:高管) where n.name=\'{}\' return n.sex'.format(key_dict['ne'])
        result = self.graph.run(cql).data()
        sex = result[0]['n.sex']
        cql = 'match (n:高管) where n.name=\'{}\' return n.age'.format(key_dict['ne'])
        result = self.graph.run(cql).data()
        age = result[0]['n.age']
        cql = 'match (n:高管) where n.name=\'{}\' return n.job'.format(key_dict['ne'])
        result = self.graph.run(cql).data()
        job = result[0]['n.job']
        cql = 'match (n:高管)-[:董事会成员]->(s:企业)  where n.name = \'{}\' return s.name'.format(key_dict['ne'])
        result = self.graph.run(cql).data()
        stock = result[0]['s.name']
        answer = '{}，性别{}, 年龄{}, 现就职于{}企业担任{}'.format(key_dict['ne'], sex, age, stock, job)
        return answer

if __name__ == "__main__":
    key_dict = {'ne': '胡晓东'}
    graph = Graph('http://localhost:7474/browser', username='neo4j', password='Serena')
    cql = 'match (n:高管) where n.name=\'{}\' return n.sex'.format(key_dict['ne'])
    result = graph.run(cql).data()
    sex = result[0]['n.sex']
    cql = 'match (n:高管) where n.name=\'{}\' return n.age'.format(key_dict['ne'])
    result = graph.run(cql).data()
    age = result[0]['n.age']
    cql = 'match (n:高管) where n.name=\'{}\' return n.job'.format(key_dict['ne'])
    result = graph.run(cql).data()
    job = result[0]['n.job']
    cql = 'match (n:高管)-[:董事会成员]->(s:企业)  where n.name = \'{}\' return s.name'.format(key_dict['ne'])
    result = graph.run(cql).data()
    stock = result[0]['s.name']
    answer = '{}，性别{}, 年龄{}, 现就职于{}企业担任{}'.format(key_dict['ne'], sex, age, stock, job)
    print(answer)
    # question_answer = Question_Answer()
    # answer = question_answer.get_answer(1, key_dict)
    # print(answer)

    