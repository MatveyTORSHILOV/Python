def main():
    with open('Торшилов_Матвей_УБ_52_vvod.txt', 'r') as file:
        data = file.readlines()

    matrix1 = []
    index = 0
    while index < len(data):
        line = data[index].strip()
        if not line:
            index += 1
            continue
        row = list(map(int, line.split()))
        matrix1.append(row)
        if len(matrix1) == len(row):
            break
        index += 1

    if matrix1:
        sums = [sum(row) for row in matrix1]
        min_sum_index = sums.index(min(sums))
        max_sum_index = sums.index(max(sums))

        result1 = [
            "Задание 1:",
            f"Строка с наименьшей суммой: {matrix1[min_sum_index]} (сумма: {sums[min_sum_index]})",
            f"Строка с наибольшей суммой: {matrix1[max_sum_index]} (сумма: {sums[max_sum_index]})"
        ]
    else:
        result1 = ["Задание 1: Матрица не найдена"]

    matrix2 = []
    for i in range(index + 1, len(data)):
        line = data[i].strip()
        if not line:
            continue
        row = list(map(int, line.split()))
        matrix2.append(row)
        if len(matrix2) == len(row):
            break

    if matrix2 and len(matrix2) == len(matrix2[0]):
        n = len(matrix2)
        # Замена элементов
        for i in range(n):
            for j in range(n):
                if matrix2[i][j] < 0:
                    matrix2[i][j] = 0
                elif matrix2[i][j] > 0:
                    matrix2[i][j] = 1

        lower_triangular = []
        for i in range(n):
            row = []
            for j in range(n):
                if i >= j:
                    row.append(matrix2[i][j])
                else:
                    row.append(0)
            lower_triangular.append(row)

        result2 = ["Задание 2:", "Нижняя треугольная матрица:"]
        for row in lower_triangular:
            result2.append(' '.join(map(str, row)))
    else:
        result2 = ["Задание 2: Квадратная матрица не найдена"]

    # Вывод результатов в файл
    with open('Торшилов_Матвей_УБ_52_vivod.txt', 'w') as file:
        file.write('\n'.join(result1 + [''] + result2))


if __name__ == "main":
    main()