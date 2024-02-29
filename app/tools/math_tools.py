'''
Математические функции
'''

def sign(n):
    return abs(n)/n if n != 0 else 0

def blockFilter(n, direction_code):
    if direction_code == 0:
        return n
    elif direction_code == 1:
        if n > 0:
            return n
        else:
            return 0
    elif direction_code == 2:
        if n < 0:
            return n
        else:
            return 0
    else:
        return 0


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
    
