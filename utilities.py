import sys


def check_arguments(message):
    if len(sys.argv) != 2:
        print(f"USAGE:{sys.argv[0]} {message}")
        exit(1)
    else:
        return sys.argv[1]


# opens file and returns a list of documents
def parse_file(file_path):
    with open(file_path, encoding="utf8") as file:
        documents = file.read().split('///')
        return [document.strip() for document in documents]


# generates tuples of id, query
def query_gen(filename):
    queries = parse_file(filename)
    for query in queries:
        if query:  # checking if empty
            id = query.split('\n')[0].strip()
            yield (id, query[len(id):].strip())
