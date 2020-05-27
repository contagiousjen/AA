import codecs
from sklearn.tree import DecisionTreeClassifier
from itertools import count
import copy
import time

def freq_search(word, _dict):
    print('> Алгоритм частотного анализа')
    alph = [0]*32
    for i in range(len(_dict)):
            alph[ord(_dict[i][0][0]) - 1040] += 1
    keys = []

    for i in range(32):
        tmp = max(zip(alph, count()))[1]
        if max(alph) != 0:
            alph[tmp] = 0
            keys.append(tmp)
    index = 0

    for i in range(len(keys)):
        for j in range(len(_dict)):
            if ord(_dict[j][0][0]) - 1040 == keys[i]:
                tmp = _dict.pop(j)
                _dict.insert(index, tmp)
                index += 1

    res = None
    for i in range(len(_dict)):
        if word == _dict[i][0]:
            res = _dict[i][1]
            break

    if not res:
        print("Слово не найдено")
    else:
        print("Слово было найдено в позиции = ", res)

class Tree:
    def __init__(self, value, index, left = None, right = None):
        self.value = value
        self.index = index
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.value)


def balance_search(tree, word, res):
    if tree == None:
        return res
    else:
        if word < tree.value:
            res = balance_search(tree.left, word, res)
        elif word > tree.value:
            res = balance_search(tree.right, word, res)
        else:
            res = tree.index
        return res
        # balance_search(tree.left, word, res)
        # balance_search(tree.right, word, res)


def build_tree(array):
    if len(array) == 1:
        return Tree(array[0][0], array[0][1])
    mid = len(array) // 2

    if len(array) != 2:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]), \
        build_tree(array[mid+1:]))
    else:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]))

def tree_search(word, _dict):
    print('> Поиск по дереву')

    _dict = sorted(_dict)
    tree = build_tree(_dict)

    res = None
    res = balance_search(tree, word, res)
    if not res:
        print("Слово не найдено")
    else:
        print("Слово было найдено в позиции = ", res)

def main():
    _dict = []

    index = 0
    f = codecs.open('file.txt', 'r', 'utf-8')
    for line in f:
        x = line
        _dict.append(x.rstrip())
        index += 1
    f.close()

    for i in range(len(_dict)):
        _dict[i] = [_dict[i], i]

    word = input('Введите слово для поиска: ')
    word = word.capitalize()

    input_flag = True
    for x in word:
        if (ord(x) < 1040 or ord(x) > 1103) and x != ' ':
            input_flag = False
    if input_flag == False:
        print('Некорректный ввод')
        return

    freq_search(word, _dict)
    tree_search(word, _dict)


if __name__ == "__main__":
    main()
