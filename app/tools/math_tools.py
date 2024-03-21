'''
Математические функции
'''

def sign(n: float) -> float:
    '''
    Определяет знак числа.

    Параметры:
    - `n` - число для которого определяется знак

    Возвращает:
    - -1, `n` < 0
    - 0, `n` = 0
    - 1, `n` > 0
    '''
    return abs(n)/n if n != 0 else 0


def nextIterible(iterible, index: float, time: int, speed: int) -> any:
    '''
    Перебирает элементы итерируемого объекта с заданной скоростью.

    Параметры:
    - `iterible` - итерируемый объект, для которого проверяется должен ли смениться элемент
    - `index` - текущий `float` индекс
    - `time` - время с предыдущего вызова
    - `speed` - скорость (элементы/секунду) с которой сменяются элементы итерируемого объекта

    Возвращает:
    - текущий элемент и текущий `float` индекс
    '''

    if not iter(iterible):
        return iterible, -1
    index += speed * 0.001 * time
    if index < len(iterible):
        return iterible[int(index)], index
    return iterible[0], -1


def absMax(nums):
    '''
    Находит максимальное по модулю число из набора.

    Параметры:
    - `nums` - набор чисел

    Возвращает:
    - модуль максимального по модулю числа из набора
    '''
    return max(abs(num) for num in nums)


def signFilter(n: float, mode: int):
    '''
    Пропускает число, если оно соответсвтует условию.

    Параметры:
    - `n` - число к которому применяется фильтр
    - `mode` - режим работы фильтра:
        - 0 - пропускает число без фильтрации
        - 1 - пропускает только положительное число
        - 2 - пропускает только отрицательное число
        - другое - не пропускает никакое число

    Возвращает:
    - `n` - принятое число, если оно соответсвтует условию
    - `0` - если оно не соответсвтует условию
    '''
    if mode == 0:
        return n
    elif mode == 1:
        if n > 0:
            return n
        else:
            return 0
    elif mode == 2:
        if n < 0:
            return n
        else:
            return 0
    else:
        return 0


def rectInArea(rect, area):
    '''
    Находит часть `rect`, которая накладывается на `area`, и отступ `offset` необходимый для обрезания текстуры объекта,
    которому принадлежит `rect`.
    
    Принимает:
    - `rect` - прямоугольник (pygame.Rect) для которого находится область наложения на `area`
    - `area` - прямоугольник (pygame.Rect) используемый для нахождения части `rect`

    Возвращает:
    - `rect` -  область наложения параметра `rect` на `area`
    '''
    offset = [0,0]
    if rect.left < area.left:
        rect.width -= area.left - rect.left
        offset[0] += area.left - rect.left
        rect.left = area.left
    if rect.right > area.right:
        rect.width -= rect.right - area.right
    if rect.top < area.top:
        rect.height -= area.top - rect.top
        offset[1] += area.top - rect.top
        rect.top = area.top
    if rect.bottom > area.bottom:
        rect.height -= rect.bottom - area.bottom 
    return rect, offset


def segmentIntersection(segment1, segment2):

    '''
    Находит точку пересечения 2 отрезков
    (Написано ИИ. ПЕРЕПИСАТЬ!!!!)
    '''

    def cross_product(pointA, pointB):
        return pointA[0] * pointB[1] - pointB[0] * pointA[1]

    def direction(pointA, pointB, pointC):
        return cross_product((pointC[0] - pointA[0], pointC[1] - pointA[1]), (pointB[0] - pointA[0], pointB[1] - pointA[1]))

    def on_segment(pointA, pointB, pointC):
        return min(pointA[0], pointB[0]) <= pointC[0] <= max(pointA[0], pointB[0]) and min(pointA[1], pointB[1]) <= pointC[1] <= max(pointA[1], pointB[1])

    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    def check_intersection(segment1, segment2):
        pointA, pointB = segment1
        pointC, pointD = segment2

        d1 = direction(pointC, pointD, pointA)
        d2 = direction(pointC, pointD, pointB)
        d3 = direction(pointA, pointB, pointC)
        d4 = direction(pointA, pointB, pointD)

        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        elif d1 == 0 and on_segment(pointC, pointD, pointA):
            return True
        elif d2 == 0 and on_segment(pointC, pointD, pointB):
            return True
        elif d3 == 0 and on_segment(pointA, pointB, pointC):
            return True
        elif d4 == 0 and on_segment(pointA, pointB, pointD):
            return True
        else:
            return False
    
    if check_intersection(segment1, segment2):
        return line_intersection(segment1, segment2)
    else:
        return None
    
