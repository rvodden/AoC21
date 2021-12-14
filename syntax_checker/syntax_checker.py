from statistics import median


class SyntaxChecker:
    opposing_bracket = {
        '{': '}',
        '(': ')',
        '[': ']',
        '<': '>'
    }

    error_scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    completion_scores = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }

    @staticmethod
    def syntax_score(data: list[str]):

        score = 0

        for datum in data:
            brackets = []
            for c in datum:
                match c:
                    case '(' | '[' | '{' | '<':
                        brackets.append(c)
                    case ')' | ']' | '}' | '>':
                        if SyntaxChecker.opposing_bracket[brackets.pop()] == c:
                            continue
                        score += SyntaxChecker.error_scores[c]
                        break

        return score

    @staticmethod
    def completion_score(data: list[str]):
        scores = []

        for datum in data:
            try:
                brackets = []
                for c in datum:
                    match c:
                        case '(' | '[' | '{' | '<':
                            brackets.append(c)
                        case ')' | ']' | '}' | '>':
                            if SyntaxChecker.opposing_bracket[brackets.pop()] == c:
                                continue
                            raise InvalidSyntaxError

                i_s = 0
                for s in [SyntaxChecker.completion_scores[b] for b in reversed(brackets)]:
                    i_s *= 5
                    i_s += s
                scores.append(i_s)
            except InvalidSyntaxError:
                continue
        return median(scores)


class InvalidSyntaxError(Exception):
    pass
