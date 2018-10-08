from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.LineSentence(u'./wiki_00cleantoken_nopunc')
model = word2vec.Word2Vec(sentences,size=200,window=5,min_count=5,workers=4)
model.save('./WikiKOModel')
