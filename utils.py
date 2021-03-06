from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()
def abbreviation(text):

    word_list = mecab_list(text)
    skip_words = set(['助詞', '記号', '助動詞', '接続詞', '連体詞', '副詞'])
    # 消したい品詞を消す

    word_list = [i for i in word_list if i[1].split(',')[0] not in skip_words]
    
    if len(word_list) == 0:
        return ("助詞、記号、助動詞、接続詞が多すぎます。", 400)
    # 品詞分解したリストから略語を作成
    return make_word(word_list)

def mecab_list(text):
    word_class = []
    for node in tokenizer.tokenize(text['submit_text']):
        word = node.surface
        if node.reading == '*':
            word_class.append((node.surface, node.part_of_speech, node.surface))
        else:
            word_class.append((node.surface, node.part_of_speech, node.reading))
    return word_class

def make_word(w_l):
    print(w_l)
    if len(w_l) == 1:
        #一単語しかない場合
        res = split_latter(w_l[0][-1])
        #一単語が2文字以下の場合
        if len(res) <= 2:
            return ("".join(res), 400)
        if 'ー' in set(res):
            res = [c for c in res if c != 'ー']
            if len(res) >= 5:
                return ("".join(res[:3]) + 'ー', 200)
            else:
                return ("".join(res[:3]), 200)
        if len(res) >= 6:
            return ("".join(res[:3]),200)
        return ("".join(res[:2]), 200)

    lower_words = set([c for c in "ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ"])

    first = split_latter(w_l[0][-1])
    second = split_latter(w_l[1][-1])

    # firstの小書き文字を省略
    if len(w_l) == 2:
        # secondの伸ばし棒を省略
        second = [c for c in second if c != 'ー']
        if 'ー' in set(first) or len(second) >= 4:
            # 伸ばし棒が入っている場合や、二単語目が4文字以上の場合確定でこの形にする。
            first = [c for c in first if c != 'ー']
            return ("".join(first[:2]) + "".join(second[:1]) + 'ー',200)
        else:
            # 先頭から二文字、二単語目は一文字取る。
            return ("".join(first[:2]) + "".join(second[:2]),200)
    else:
        first = [c for c in first if c != 'ー']
        second = [c for c in second if c != 'ー']
        third = w_l[2][-1]
        return ("".join( first[:2] if len(first) >= 3 else first[0]) + second[0] + third[0], 200)
         
def split_latter(text):
    res = []
    lower_words = set([c for c in "ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮ"])
    for i in range(len(text)):
            # ッとか、ュはさっきの文字とひとつながりとしてみなす。
        if text[i] in lower_words and text[i] not in set(['っ','ュ']):
            res[-1] = res[-1] + text[i]
        else:
            # それ以外の小文字は、別の文字としてみなしている。
            res.append(text[i])
    return res