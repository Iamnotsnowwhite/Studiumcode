import random

# 定义单词列表
nouns = ["cat", "dog", "man", "woman", "car", "bicycle", "tree", "house"]
verbs = ["jumps", "runs", "drives", "flies", "eats", "sleeps", "walks"]
adjectives = ["big", "small", "red", "blue", "fast", "slow", "bright", "dark"]
adverbs = ["quickly", "slowly", "gracefully", "awkwardly", "happily", "sadly"]
prepositions = ["on", "in", "under", "over", "beside", "with", "without"]

# 生成随机句子函数
def generate_sentence(input): #按道理应该接受一个input
    noun1 = random.choice(nouns)
    noun2 = random.choice(nouns)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives)
    adverb = random.choice(adverbs)
    preposition = random.choice(prepositions)
    
    sentence = f"The {adjective} {noun1} {verb} {adverb} {preposition} the {noun2}."
    return sentence


