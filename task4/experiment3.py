import os
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# Эксперимент 3
# Параметры модели. Параметр workers = 2, тк на машине 2 ядра, этот параметр оставим без изменений.
# Попробуем изменить параметр vector_size в большую и меньшую сторону.
# Изначально я его оставила равному 100. Сделаем его равным 10 и посмотрим, что выдаст модель.
# Тк предобработка текста ухудшила результаты, уберем только знаки препинания и приведем слова в предложениях к нижнему регистру

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
model = Doc2Vec(documents, vector_size=10, workers=2, epochs=20)
vector_to_search = model.infer_vector(["санкции", "экономика"])

# 5 наиболее похожих
similar_documents = model.dv.most_similar([vector_to_search], topn=5)
for s in similar_documents:
    print(corpus[s[0]])
#Вывод: Первый текст - Мое рок-н-ролльное поздравление(63.txt), в тексте не упоминается ни экономика, ни санкции
# Второй текст - О Николае Втором(97.txt), текст не связан с входными запросами
# Третий текст - Приемлемая доза государства(8.txt), текст сильно связан с экономикой
# Четвертый текст - Оптимисты, пессимисты и реалисты сегодня(36.txt), в тексте упоминается экономика
# Пятый текст - Сталинский завет всем диктаторам(56.txt), в тексте не упоминается ни экономика, ни санкции
# Таким образом, в результате появились тексты слабо связаные с входными запросами
# Стоит также отметить, что результаты с vector_size=100 были гораздо лучше