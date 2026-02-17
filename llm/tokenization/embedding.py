# import gensim
# model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
#
# print(f"The embedding size: {model.vector_size}")
# print(f"The vocabulary size: {len(model)}")
#
# # italy - rome + london = england
# model.most_similar(positive=['london', 'italy'], negative=['rome'])
#
# ### OUTPUT ###
# [('england', 0.5743448734283447),
#  ('europe', 0.537047266960144),
#  ('liverpool', 0.5141493678092957),
#  ('chelsea', 0.5138063430786133),
#  ('barcelona', 0.5128480792045593)]
#
# model.most_similar(positive=['woman', 'doctor'], negative=['man'])
# ### OUTPUT ###
# [('gynecologist', 0.7093892097473145),
#  ('nurse', 0.6477287411689758),
#  ('doctors', 0.6471460461616516),
#  ('physician', 0.6438996195793152),
#  ('pediatrician', 0.6249487996101379)]


from gensim.models import Word2Vec
import nltk


sentences = [
    "the cat sat on the mat".split(),
    "the dog sat on my rug".split(),
    "the quick brown fox jumps over the lazy dog".split()
]


model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0) # sg=0 for CBOW, sg=1 for Skip-gram

# Access word vectors
word_vector = model.wv['cat']

# Find most similar words
similar_words = model.wv.most_similar('cat')
print(similar_words)

model.save("word2vec.model")

