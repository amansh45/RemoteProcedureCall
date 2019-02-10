import sys
class Interface(object):
    def add(self, a, b):
        try:
            result = a+b
            return 200, result
        except:
            return 205, sys.exc_info()[1]

    def append_strings(self, x, y):
        try:
            x = x.replace('h','2')
            y = y.replace('e','3')
            result = x+y
            return 200, result
        except:
            return 205, sys.exc_info()[1]

    def append_lists(self, m, n, o):
        try:
            for i in range(len(m)):
                m[i] = m[i] * 3

            for i in range(len(n)):
                n[i] = n[i] * 2

            for i in range(len(o)):
                o[i] = o[i] * 4
            result = m+n+o
            return 200, result
        except:
            return 205, sys.exc_info()[1]
