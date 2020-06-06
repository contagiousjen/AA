##----- Задание: вывести массив размещений n единиц в строке из m нулей -----##

def recursion(n, start):
    n -= 1
    if n:
        for i in range(start, m):
            array[i] = 1
            recursion(n, i+1)
            array[i] = 0
    else:
        print(array)
        
        
m = input('Введите длину строки m: ')
n = input('Введите количество единиц n: ')

correct = True
try:
    m = int(m)
    n = int(n)
except:
    correct = False

if n >= m:
    correct = False

if correct:
    array = [0]*m
    recursion(n+1, 0)
else:
    print('Некорректный ввод')
