import codecs
from sklearn.tree import DecisionTreeClassifier
from itertools import count
import copy

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

    res = []
    for i in range(len(_dict)):
        if word == _dict[i][0]:
            res.append(_dict[i][1])

    if len(res) == 0:
        print("Слово не найдено")
    else:
        print("Слово было найдено в позициях = ", res)

# def binary_search(word, _dict):
#     print('> Алгоритм бинарного поиска')
#
#     _dict = sorted(_dict)
#
#     alph = [0]*33
#     for i in range(len(_dict)):
#         alph[ord(_dict[i][0][0]) - 1040] += 1
#
#     first = 0
#     while (word[0] != _dict[first][0][0]):
#         first += 1
#
#     last = first + alph[ord(word[0]) - 1040] - 1
#
#     mid = (first + last) // 2
#
#     while _dict[mid][0] != word and first < last:
#         if word > _dict[mid][0]:
#             first = mid + 1
#         else:
#             last = mid - 1
#         mid = (first + last) // 2
#
#     if first > last:
#         print("Слово не найдено")
#     else:
#         res = []
#         tmp = mid-1
#         while _dict[mid][0][1] == word[1]:
#             if _dict[mid][0] == word:
#                 res.append(_dict[mid][1])
#             mid += 1
#         mid = tmp
#         while _dict[mid][0][1] == word[1]:
#             if _dict[mid][0] == word:
#                 res.append(_dict[mid][1])
#             mid -= 1
#         if len(res) == 0:
#             print("Слово не найдено")
#         else:
#             print("Слово было найдено в позициях = ", res)

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


def balance_search(tree, word):
    if tree == None: return False
    if tree.value == word:
        res = []
        res.append(tree.index)
        tmp = tree.left
        while tmp != None and tmp.value == word:
            res.append(tmp.index)
            tmp = tmp.left
        return res

    if word < tree.value:
        return balance_search(tree.left, word)
    else:
        return balance_search(tree.right, word)

def build_tree(array):
    if len(array) == 1:
        return Tree(array[0][0], array[0][1])
    mid = len(array) // 2

    if len(array) != 2:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]), build_tree(array[mid+1:]))
    else:
        return Tree(array[mid][0], array[mid][1], build_tree(array[:mid]))

def tree_search(word, _dict):
    print('> Поиск по дереву')
    _dict = sorted(_dict)
    tree = build_tree(_dict)
    result = balance_search(tree, word)
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
    # binary_search(word, _dict)
    tree_search(word, _dict)

if __name__ == "__main__":
    main()
