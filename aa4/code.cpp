#include <iostream>
#include <chrono>
#include <vector>
#include <iomanip>
#include <ctime>
#include <cstdlib>
#include <thread>
#include <math.h>

using namespace std;

typedef std::vector<std::vector<int> > Matrix;

void print_matrix(std::string str, Matrix& array, int n)
{
    std::cout << str << '\n';

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
            std::cout << setw(3)<< array[i][j] << ' ';

        std::cout << '\n';
    }
}

void fill_matrix_by_random(Matrix &array, int n)
{
    for (int i = 0; i < n; i++) {
        std::vector<int> tmp{};

        for (int j = 0; j < n; j++) {
            tmp.push_back(rand() % 9);
        }
        array.push_back(tmp);
    }
}

void fill_matrix_by_zero(Matrix &array, int n)
{
    for (int i = 0; i < n; i++) {
        std::vector<int> tmp;

        for (int j = 0; j < n; j++) {
            tmp.push_back(0);
        }
        array.push_back(tmp);
    }
}

void alg_threads(Matrix &array3, Matrix array1, Matrix array2, int number_of_threads,
                 int size_matrix, vector<int> MulV, int n_rows, int part)
{
    int start, finish;
    start = part * n_rows;
    finish = start + n_rows;
    if ((part + 1) == number_of_threads)
        finish = size_matrix;
    else
        finish = start + n_rows;

    std::vector<int> MulU(finish - start, 0);

    for (int i = start; i < finish; i++)
        for (int j = 0; j < size_matrix/2; j++)
            MulU[i-start] += array1[i][2 * j] * array1[i][2 * j + 1];

    for (int i = start; i < finish; i++)
    {
        for (int j = 0; j < size_matrix; j++)
        {
            array3[i][j] = - MulU[i-start] - MulV[j];
            for (int k = 0; k < size_matrix/2; k++)
            {
                array3[i][j] += (array1[i][2 * k] + array2[2 * k + 1][j]) *
                                (array1[i][2 * k + 1] + array2[2 * k][j]);
            }
            if (size_matrix % 2 == 1)
                array3[i][j] +=  array1[i][size_matrix - 1] * array2[size_matrix - 1][j];
        }
    }
}

int main(void)
{
    int size_matrix, number_of_threads;

    Matrix array1{}, array2{}, array3{};
    std::cout << "Введите размер матрицы: ";
    std::cin >> size_matrix;
    std::cout << "Введите количество потоков: ";
    std::cin >> number_of_threads;

    fill_matrix_by_zero(array3, size_matrix);
    fill_matrix_by_random(array1, size_matrix);
    fill_matrix_by_random(array2, size_matrix);

    int time = 0;

    for (int i = 0; i < 100; i++)
    {
        std::vector<std::thread> threads_list;
        int part = 0;

        chrono::high_resolution_clock::time_point t_start, t_end;
        std::srand(std::time(nullptr));

        std::vector<int> MulV(size_matrix, 0);

        for (int j = 0; j < size_matrix; j++)
            for (int i = 0; i < size_matrix/2; i++)
                MulV[j] += array2[2 * i][j] * array2[2 * i + 1][j];

        int n_rows = size_matrix / number_of_threads;

        for (int i = 0; i < number_of_threads; i++)
            threads_list.push_back(std::thread(alg_threads, ref(array3), array1,
            array2, number_of_threads, size_matrix, MulV, n_rows, part++));

         t_start = chrono::high_resolution_clock::now();
         for (auto& thrd : threads_list)
             thrd.join();
         t_end = chrono::high_resolution_clock::now();

         time += chrono::duration_cast<std::chrono::
         microseconds>(t_end-t_start).count();
     }

    time /= 100;

    std::cout << time << '\n';

        // print_matrix("\nПервая матрица: ", array1, size_matrix);
        // print_matrix("\nВторая матрица: ", array2, size_matrix);
        // print_matrix("\nРезультат умножения: ", array3, size_matrix);

        return 0;
}
