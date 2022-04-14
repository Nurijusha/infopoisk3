import os
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# Эксперимент 4
# Параметры модели. В прошлом эксперименте мы установили vector_size= 10, результаты были не очень хорошими
# Попробуем изменить параметр vector_size в большую сторону. Установим значение 200

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
model = Doc2Vec(documents, vector_size=200, workers=2, epochs=20)
vector_to_search = model.infer_vector(["санкции", "экономика"])

# 5 наиболее похожих
similar_documents = model.dv.most_similar([vector_to_search], topn=5)
for s in similar_documents:
    print(corpus[s[0]])
#Вывод: Первый текст - Как искусственный интеллект повлиял на рынок труда(82.txt), в тексте рассматривается экономика
# Второй текст - Нобелевский лауреат на пропагандистском фронте(84.txt), в тексте упоминается экономика
# Третий текст - Исход битвы зависит и от «диванных войск»(44.txt), в тексте не упоминается ни экономика, ни санкции
# Четвертый текст - О Николае Втором(97.txt), текст не связан с входными запросами
# Пятый текст - И снова стагфляция, не прошло и полвека(28.txt), в тексте не упоминается экономика
# Таким образом, в результате появились тексты связанные с входными запросами
# Стоит также отметить, что результаты с vector_size=100 были лучше

# В качестве эксперимента я также запускала код со значениями vector_size = 300
# Первый текст - "Повторяя слова, Лишенные всякого смысла, Но без напряженья..."(64.txt), в тексте рассматривается экономика
# Второй текст - Об одной "беспроигрышной" стратегии в трейдинге(88.txt), в тексте присутвует вопрос экономики
# Третий текст - Август в Севастополе(90.txt), в тексте не упоминается ни экономика, ни санкции
# Четвертый текст - Нобелевский лауреат на пропагандистском фронте(84.txt), в тексте упоминается экономика
# Пятый текст - Кому нужна блокировка Youtube(19.txt), в тексте не упоминается ни экономика, ни санкции
# Таким образом, в результате появились тексты связанные с входными запросами
# Стоит также отметить, что результаты с vector_size=100 были лучше, результаты vector_size = 200 и 300 примерно одинаковы

# Также я решила попробовать установить значение vector_size = 50
# Первый текст - Экономический рост: как его понимали в прошлом, и как сейчас(101.txt), текст тесно связан с экономикой
# Второй текст - Бесконечен ли экономический рост?(93.txt), в тексте присутвует тема экономики
# Третий текст - "Революционная ситуация": как ее определяет наука сегодня?(17.txt), в тексте не упоминается ни экономика, ни санкции
# Четвертый текст - Влияние демократии на экономический рост: так ли оно неопределенно?(74.txt), в тексте рассматривается экономика
# Пятый текст - Что нынче вызывает рост неравенства(81.txt), в тексте рассматривается экономическая сторона вопроса
# Таким образом, в результате появились тексты связанные с входными запросами и только один текст не подошел под запрос,
# можно отметить, что vector_size = 50 показывает лучше результаты, чем vector_size = 200 и 300 и хуже, чем vector_size = 100
# Именно поэтому оставим vector_size = 100