import codecs
from sklearn.tree import DecisionTreeClassifier
from itertools import count
import copy

class Tree:
    def __init__(self, value, index, left = None, right = None):
        self.value = value
        self.index = index
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.value)

def print_tree(tree):
    if tree == None: return
    print(tree.value, tree.index)
    print_tree(tree.left)
    print_tree(tree.right)

def balance_search(tree, value):
    if tree == None: return False
    if tree.value[0] == value:
        res = []
        res.append(tree.value[1])
        tmp = tree.left
        while tmp != None and tmp.value == value:
            res.append(tmp.value[1])
            tmp = tmp.left
        return res

    if value < tree.value[0]:
        return balance_search(tree.left, value)
    else:
        return balance_search(tree.right, value)

def build_tree(array):
    if len(array) == 1:
        return Tree(array[0][0], array[0][1])
    mid = len(array) // 2

    if len(array) != 2:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]), build_tree(array[mid+1:]))
    else:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]))

def binary_search(word, _dict):
    print('Алгоритм бинарного поиска')

    alph = [0]*33
    for i in range(len(_dict)):
        alph[ord(_dict[i][0][0]) - 1040] += 1

    first = 0
    while (word[0] != _dict[first][0][0]):
        first += 1

    last = first + alph[ord(word[0]) - 1040] - 1

    mid = (first + last) // 2

    while _dict[mid][0] != word and first < last:
        if word > _dict[mid][0]:
            first = mid + 1
        else:
            last = mid - 1
        mid = (first + last) // 2

    if first > last:
        print("Слово не найдено")
    else:
        res = []
        tmp = mid-1
        while _dict[mid][0][1] == word[1]:
            if _dict[mid][0] == word:
                res.append(_dict[mid][1])
            mid += 1
        mid = tmp
        while _dict[mid][0][1] == word[1]:
            if _dict[mid][0] == word:
                res.append(_dict[mid][1])
            mid -= 1
        if len(res) == 0:
            print("Слово не найдено")
        else:
            print("Слово было найдено в позициях = ", res)

def freq_search(word, _dict):
    print('Алгоритм частотного анализа')

    alph = [0]*33
    for i in range(len(_dict)):
            alph[ord(_dict[i][0][0]) - 1040] += 1

    keys = []

    for i in range(len(alph)):
        tmp = max(zip(alph, count()))[1]
        if max(alph) != 0:
            alph[tmp] = 0
            keys.append(tmp)

    index = 0

    for i in range(len(_dict)):
        _dict[i] = [_dict[i], i]

    for i in range(len(keys)):
        for j in range(len(_dict)):
            if ord(_dict[j][0][0][0]) - 1040 == keys[i]:
                tmp = _dict.pop(j)
                _dict.insert(index, tmp)
                index += 1

    res = []
    for i in range(len(_dict)):
        if word == _dict[i][0][0]:
            res.append(_dict[i][0][1])

    if len(res) == 0:
        print("Слово не найдено")
    else:
        print("Слово было найдено в позициях = ", res)

def tree_search(word, _dict):
    print('Поиск по дереву')
    _dict = sorted(_dict)
    test = build_tree(_dict)
    result = balance_search(test, word)
    if result == False:
        print("Слово не найдено")
    else:
        print("Слово было найдено в позициях = ", result)

def main():

    _dict = []

    index = 0
    f = codecs.open('file.txt', 'r', 'utf-8')
    for line in f:
        x = line
        _dict.append(x.rstrip())
        index += 1
    f.close()

    alph = [0]*40
    for i in range(len(_dict)):
        alph[ord(_dict[i][0]) - 1040] += 1

    alph_copy = copy.deepcopy(alph)

    keys = []

    for i in range(len(alph)):
        tmp = max(zip(alph, count()))[1]
        if max(alph) != 0:
            alph[tmp] = 0
            keys.append(tmp)

    index = 0

    for i in range(len(_dict)):
        _dict[i] = [_dict[i], i]

    for i in range(len(keys)):
        for j in range(len(_dict)):
            if ord(_dict[j][0][0]) - 1040 == keys[i]:
                tmp = _dict.pop(j)
                _dict.insert(index, tmp)
                index += 1

    f = codecs.open('file1.txt', 'w', 'utf-8')
    for i in range(len(_dict)):
        f.write(_dict[i][0] + str(_dict[i][1]) + '\n')
    f.close()

    alph = copy.deepcopy(alph_copy)
    alph_copy = sorted(alph_copy)
    alph_copy.reverse()

    ind = 0
    for k in range(len(alph_copy)):
        for i in range(ind, ind+alph_copy[k]):
            for j in range(ind, ind+alph_copy[k]-1):
                if _dict[j][0][1] > _dict[j+1][0][1]:
                    _dict[j], _dict[j+1] = _dict[j+1], _dict[j]
        ind += alph_copy[k]

    f = codecs.open('file2.txt', 'w', 'utf-8')
    for i in range(len(_dict)):
        f.write(_dict[i][0] + str(_dict[i][1]) + '\n')
    f.close()

    word = input('Введите слово для поиска: ')
    word = word.capitalize()
    fl = True
    for x in word:
        if (ord(x) < 1040 or ord(x) > 1103) and x != ' ':
            fl = False
    if fl == False:
        print('Некорректный ввод')
        return

    binary_search(word, _dict)
    freq_search(word, _dict)
    tree_search(word, _dict)

if __name__ == "__main__":
    main()
