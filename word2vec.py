from elasticsearch import Elasticsearch
from gensim.models import Word2Vec

from queries import get_more_like_this_query
from utilities import check_arguments, query_gen

if __name__ == '__main__':

    file_path = check_arguments("<queries.txt path>")
    es = Elasticsearch()  # connecting to ES
    model = Word2Vec.load("word2vec.model")
    for size in [5, 10, 15, 20, 30, 50]:
        print(size)
        with open(str(size) + '_results.txt', 'w') as results:
            for query_index, (_, query) in enumerate(query_gen(file_path, model=model), 1):
                query_body = get_more_like_this_query(size, query)
                result = es.search(index="json_docs", body=query_body)
                for index, hit in enumerate(result['hits']['hits'], 1):
                    id = hit['_id']
                    if query_index < 10:  # making sure it looks nice
                        q = 'Q0'
                    else:
                        q = 'Q'
                    results.write(f"{q}{query_index} 0 {id} {index} {hit['_score']} standard\n")
