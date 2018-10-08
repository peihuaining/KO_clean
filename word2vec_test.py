from gensim.models import word2vec

model = word2vec.Word2Vec.load('./WikiKOModel')

print(model.wv.similarity('공산당','정당')) #两个词的相关性

print(model.wv.most_similar(['공산당','중국'])) # 北京is to中国 as 伦敦is to？
