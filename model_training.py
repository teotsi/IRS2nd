from gensim.models import Word2Vec

from indexing import parse_docs
from utilities import check_arguments

file_path = check_arguments("<ir2020_files.txt path>")
docs = list(parse_docs(file_path))  # parsing collection
docs = [doc["text"] for doc in docs]  # extracting text
training_set = [doc.split(" ") for doc in docs]  # creating lists-in-list format for Word2Vec
model = Word2Vec(training_set, size=200, workers=4)  # creating model
model.save("word2vec.model")  # saving to disk
