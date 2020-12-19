    dict_key = {'ns', '华纺股份'}
    graph = Graph('http://localhost:7474', username='neo4j', password='Serena')
    cql = 'match (n:高管)-[:董事会成员]->(p:企业{name:\'华纺股份\'}) return n'
    result = graph.run(cql)
    print(result)