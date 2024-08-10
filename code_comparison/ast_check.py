import math
import numpy
import ast


def point(x, y):
    return '[' + str(x) + ',' + str(y) + ']'


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.seq = []

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.seq.append(type(node).__name__)

    def visit_FunctionDef(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.seq.append(type(node).__name__)

    def visit_Assign(self, node):
        self.seq.append(type(node).__name__)


class CodeParse(object):
    def __init__(self, codeA, codeB):
        self.visitorB = None
        self.visitorA = None
        self.codeA = codeA
        self.codeB = codeB
        self.nodeA = ast.parse(self.codeA)
        self.nodeB = ast.parse(self.codeB)
        self.seqA = ""
        self.seqB = ""
        self.work()

    def work(self):
        self.visitorA = CodeVisitor()
        self.visitorA.visit(self.nodeA)
        self.seqA = self.visitorA.seq
        self.visitorB = CodeVisitor()
        self.visitorB.visit(self.nodeB)
        self.seqB = self.visitorB.seq


class CalculateSimilarity(object):
    def __init__(self, seq_a, seq_b, gap_penalty, match_score, mismatch_score):
        self.seq_a = seq_a
        self.seq_b = seq_b
        self.gap_penalty = gap_penalty
        self.match_score = match_score
        self.mismatch_score = mismatch_score
        self.similarity = []
        self.smith_waterman(self.seq_a, self.seq_b, self.gap_penalty)

    def score(self, a, b):
        if a == b:
            return self.match_score
        else:
            return self.mismatch_score

    def traceback(self, a, b, H, path, value, result):
        if value:
            temp = value[0]
            result.append(temp)
            value = path[temp]
            x = int((temp.split(',')[0]).strip('['))
            y = int((temp.split(',')[1]).strip(']'))
        else:
            return
        if H[x, y] == 0:  # 终止条件
            xx = 0
            yy = 0
            sim = 0
            for item in range(len(result) - 2, -1, -1):
                position = result[item]
                x = int((position.split(',')[0]).strip('['))
                y = int((position.split(',')[1]).strip(']'))
                if x == xx:
                    pass
                elif y == yy:
                    pass
                else:
                    sim = sim + 1
                xx = x
                yy = y
            self.similarity.append(sim * 2 / (len(a) + len(b)))

        else:
            self.traceback(a, b, H, path, value, result)

    def smith_waterman(self, A, B, W):
        n, m = len(A), len(B)
        matrix = numpy.zeros([n + 1, m + 1], int)
        path = {}
        for i in range(0, n + 1):
            for j in range(0, m + 1):
                if i == 0 or j == 0:
                    path[point(i, j)] = []
                else:
                    s = self.score(A[i - 1], B[j - 1])
                    L = matrix[i - 1, j - 1] + s
                    P = matrix[i - 1, j] - W
                    Q = matrix[i, j - 1] - W
                    matrix[i, j] = max(L, P, Q, 0)

                    # 添加进路径
                    path[point(i, j)] = []
                    if math.floor(L) == matrix[i, j]:
                        path[point(i, j)].append(point(i - 1, j - 1))
                    if math.floor(P) == matrix[i, j]:
                        path[point(i, j)].append(point(i - 1, j))
                    if math.floor(Q) == matrix[i, j]:
                        path[point(i, j)].append(point(i, j - 1))

        end = numpy.argwhere(matrix == numpy.max(matrix))
        for pos in end:
            key = point(pos[0], pos[1])
            value = path[key]
            result = [key]
            self.traceback(A, B, matrix, path, value, result)

    def calc_similarity(self):  # 取均值
        return sum(self.similarity) / len(self.similarity)


def calc(code1, code2) -> float:
    my_ast = CodeParse(code1, code2)
    parser = CalculateSimilarity(my_ast.seqA, my_ast.seqB, 1, 1, -1 / 3)
    return parser.calc_similarity()


def main():
    my_ast = CodeParse("print('hello, world!')", "print('hell0 world!')")
    parser = CalculateSimilarity(my_ast.seqA, my_ast.seqB, 1, 1, -1 / 3)
    print(parser.calc_similarity())


if __name__ == "__main__":
    main()
