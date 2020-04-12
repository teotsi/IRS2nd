import sys
from utilities import query_gen, check_arguments
from elasticsearch import Elasticsearch

if __name__ == '__main__':

    file_path = check_arguments("<queries.txt path>")
    es = Elasticsearch()  # connecting to ES

    for size in [20, 30, 50]:
        with open(str(size) + '_results.txt', 'w') as results:
            for query_index, (_, query) in enumerate(query_gen(file_path), 1):
                query_body = {  # body of MLT query
                    "from": 0, "size": size,  # specifying the number of texts to be retrieved
                    "query": {
                        "more_like_this": {
                            "fields": [
                                "text"
                            ],
                            "like": query,
                            "min_term_freq": 1,
                            "max_query_terms": 25
                        }
                    }
                }
                result = es.search(index="json_docs", body=query_body)
                for index, hit in enumerate(result['hits']['hits'], 1):
                    id = hit['_id']
                    if query_index < 10:  # making sure it looks nice
                        q = 'Q0'
                    else:
                        q = 'Q'
                    results.write(f"{q}{query_index} 0 {id} {index} {hit['_score']} standard\n")
