import os
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# Финальный код с наилучшими результатами
path = '/Users/nuriya/PycharmProjects/infopoisk32/sites/'
# собираем из файлов датасет
dataset = []
text = ''
# получаем количество файлов в каталоге
num_files = sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))
for i in range(0, num_files):
    with open(f'/Users/nuriya/PycharmProjects/infopoisk32/sites/{i}.txt', "r", encoding="utf-8") as file:
        for line in file:
            text = text + line + ' '
        dataset.append(text)
        text = ''
    file.close()

# удаляем знакие препинания и специальные символы, токенизируем текст
corpus = [re.sub("[^A-Za-zА-Яа-я]", " ", text) for text in dataset]
corpus = [text.lower() for text in corpus]
# строим модель
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(corpus)]
model = Doc2Vec(documents, vector_size=100, workers=2, epochs=20)
vector_to_search = model.infer_vector(["санкции", "экономика"])

# 5 наиболее похожих
similar_documents = model.dv.most_similar([vector_to_search], topn=5)
for s in similar_documents:
    print(corpus[s[0]])
# ОБЩИЕ ВЫВОДЫ:
# 1. Предобработка не всегда влияет на положительный результат, более того, без обработки результаты стали лучше
# 2. Подобрать точные параметры vector_size и epochs является очень сложной задачей, для моих текстов оптимальными значениями
# оказались vector_size=100, epochs=20
# 3. Модель ведет себя нестабильно, сильно завязана на значениях параметров. Модель способна выдавать нужные результаты,
# однако для этого необходимо провести большое количество экспериментов
