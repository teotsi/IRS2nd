from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from utilities import query_gen, check_arguments, parse_docs

if __name__ == '__main__':
    file_path = check_arguments("<ir2020_files.txt path>")
    es = Elasticsearch()

    for ok, result in streaming_bulk(
            es,
            parse_docs(file_path),  # parse docs generates JSON docs
            index='json_docs',
            chunk_size=50,  # setting the batch size
    ):
        action, result = result.popitem()
        doc_id = f"Document with ID {result['_id']} was indexed successfully"
        if not ok:  # printing status
            print(f"Failed to {action} document {doc_id}: {result}")
        else:
            print(doc_id)
