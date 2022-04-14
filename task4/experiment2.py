import os
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# Эксперимент 2
# Используем предобработку текста: знаки препинания и приведем слова в предложениях к нижнему регистру
path = '/Users/nuriya/PycharmProjects/infopoisk32/sites/'

# собираем из файлов датасет
dataset = []
text = ''
#получаем количество файлов в каталоге
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
#Вывод: Первый текст - Еще о российском научном экспорте(38.txt), в тексте упоминаются санкции.
# Второй текст - Капитализм как подсистема, существующая при любой "формации"(92.txt), в тексте упоминается экономика
# Третий текст - Нефтерубль(33.txt), в тексте упоминаются санкции и частично охвачивается экономика
# Четвертый текст - Скромная попытка заглянуть в ближайшее будущее экономики и рынков(27.txt), в тексте упоминается экономика
# Пятый текст - Роботизация(53.txt), текст описывает влияние роботизации и частично затрагивает экономику
# Таким образом, в данном эксперименте все тексты соответствуют тематике запроса, но стоит отметить, что текстов охватывающих и санкции, и экономику в результате не оказалось
# Стоит также отметить, что результаты без предобработки показали лучшие результаты.