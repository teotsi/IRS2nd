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


def concatenate_word2vec_tuples(tuples):
    string = ""
    for tuple in tuples:
        string += f'{tuple[0]} '
    return string


# generates tuples of id, query
def query_gen(filename, model=None):
    queries = parse_file(filename)
    for query in queries:
        if query:  # checking if empty
            id = query.split('\n')[0].strip()
            text = query[len(id):].strip()
            if model:
                words = text.split()
                text = ""
                for word in words:
                    try:
                        text += concatenate_word2vec_tuples(model.most_similar(word))
                    except KeyError:
                        text += f'{word} '
            yield id, text


# generates dictionaries containing text and id keys
def parse_docs(path):
    for id, document in query_gen(path):
        yield {'_id': id,
               'text': document
               }
