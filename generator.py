import re
import random
import pickle
import argparse


class Generator_text:

    def __init__(self, filename):
        text = open(filename, 'r', encoding='utf-8').read()
        formatted_text = re.sub('[^а-яё,.!?]', ' ', text.lower())
        # formatted_text = re.sub('[^a-z,.!?]', ' ', text.lower()) # english text
        self.splitted_text = re.split('\\s+', formatted_text)
    
    # биграммная модель
    def fit(self):
        result = {k: [] for k in self.splitted_text[:-1]}
        for i in range(len(self.splitted_text) - 1):
            if self.splitted_text[i + 1] not in result[self.splitted_text[i]]:
                result[self.splitted_text[i]].append(self.splitted_text[i + 1])

        with open('model.pkl', 'wb') as data:
            pickle.dump(result, data, protocol=pickle.HIGHEST_PROTOCOL)
    
    # генерация текста
    def generate(self, length):
        with open('model.pkl', 'rb') as data:
            bigrams = pickle.load(data)
        first_word = random.choice(list(bigrams.keys()))
        next_word = first_word
        generated = ''
        for i in range(length):
            generated += ''.join(next_word + " ")
            next_word = random.choice(bigrams[next_word])
            while next_word not in list(bigrams.keys()): # избежание ошибок
                next_word = random.choice(list(bigrams.keys()))
        print(generated)


# Запуск программы
def start():
    Arguments = argparse.ArgumentParser()
    Arguments.add_argument("-f")
    Arguments.add_argument("-l")
    args = Arguments.parse_args()
    filename = args.f
    length = int(args.l)
    text = Generator_text(filename)
    text.fit()
    text.generate(length)


start()
