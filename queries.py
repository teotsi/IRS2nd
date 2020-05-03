from elasticsearch import Elasticsearch

from utilities import query_gen, check_arguments


def get_more_like_this_query(size, text):
    return {  # body of MLT query
        "from": 0, "size": size,  # specifying the number of texts to be retrieved
        "query": {
            "more_like_this": {
                "fields": [
                    "text"
                ],
                "like": text,  # specifying the string to be used
                "min_term_freq": 1,
                "max_query_terms": 25
            }
        }
    }


def get_match_query(size, text):
    return {
        "from": 0, "size": size,
        "query": {
            "match": {
                "text": {
                    "query": text
                }
            }
        }
    }


if __name__ == '__main__':

    file_path = check_arguments("<queries.txt path>")
    es = Elasticsearch()  # connecting to ES

    for size in [5, 10, 15, 20, 30, 50]:
        print(size)
        with open(str(size) + '_results.txt', 'w') as results:
            for query_index, (_, query) in enumerate(query_gen(file_path), 1):
                query_body = get_more_like_this_query(size,query)
                result = es.search(index="json_docs", body=query_body)
                for index, hit in enumerate(result['hits']['hits'], 1):
                    id = hit['_id']
                    if query_index < 10:  # making sure it looks nice
                        q = 'Q0'
                    else:
                        q = 'Q'
                    results.write(f"{q}{query_index} 0 {id} {index} {hit['_score']} standard\n")
