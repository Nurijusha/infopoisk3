import os
import re
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk import word_tokenize, SnowballStemmer
# Эксперимент 1
# Используем предобработку текста: удаление знаков препинания и небуквенных символов, токеницзацию,
# удаление стоп-слов, стемминг и лемматизацию.
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
corpus = [word_tokenize(text) for text in corpus]

# убираем стоп-слов
nltk.download('stopwords')
tmp = []
for text in corpus:
    text = [word for word in text if word not in set(nltk.corpus.stopwords.words("russian"))]
    tmp.append(text)
corpus = tmp

# стемминг
stemmer = SnowballStemmer("russian")
tmp = []
for text in corpus:
    text = [stemmer.stem(word) for word in text]
    tmp.append(text)
corpus1 = tmp

# лемматизация
nltk.download('wordnet')
lemmatizer = nltk.stem.WordNetLemmatizer()
tmp = []
for text in corpus:
    text = [lemmatizer.lemmatize(word) for word in text]
    tmp.append(text)
new_corpus = tmp
# Построим модель
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(corpus)]
model = Doc2Vec(documents, vector_size=100, workers=2, epochs=20)
vector_to_search = model.infer_vector(["санкции", "экономика"])

# 5 наиболее похожих
similar_documents = model.dv.most_similar([vector_to_search], topn=5)
for s in similar_documents:
    print(corpus[s[0]])
#Вывод: Первый текст - Дефицит как неустранимый порок любого социализма(77.txt), текст напрямую связан с экономикой, слово "экономика" встречается в тексте 2 раза.
# Второй текст - Как теперь сохранять и приумножать нажитое(5.txt), текст также напрямую связан с экономикой, слово "экономика" встречается 4 раза
# Третий текст - Достоевский о слабости, требующей себе привилегий(71.txt), текст повествует о писателе и никак не связан с входным запросом
# Четвертый текст - Льготная ипотека: небольшое облегчение сегодня за счет наших детей(2.txt), текст описывает экономию, а не экономику
# Пятый текст - Успехи российских фермеров и подорожание продуктов(21.txt), текст напрямую связан с экономикой
# Таким образом, 3 текста напрямую совпали с запросом "экономика", однако ни один текст не удовлетворяет запросу "санкции"
# Поэтому в следующем эксперименте попробуем использовать не все методы предобработки текста. Оставим знаки препинания и приведем слова в предложениях к нижнему регистру.
