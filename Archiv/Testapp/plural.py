import re

def build_match_and_apply_function(pattern, search, replace):
        def matches_rule(word):
            return re.search(pattern, word)
        def apply_rule(word):
            return re.sub(search, replace, word)
        return (matches_rule, apply_rule)

rules = []
with open('plural4-rules.txt', encoding='utf-8') as pattern_file:
    for line in pattern_file:
        pattern, search, replace = line.split(None, 3)
        rules.append(build_match_and_apply_function(
            pattern, search,replace))