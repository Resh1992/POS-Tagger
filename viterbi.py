from tabulate import tabulate

POS_TAG_VERB = 'VERB'
POS_TAG_NOUN = 'NOUN'
POS_TAG_ADV = 'ADV'
TOKEN_START = 'START'
TOKEN_END = 'END'
POS_TAGS = [TOKEN_START, POS_TAG_VERB, POS_TAG_NOUN, POS_TAG_ADV, TOKEN_END]

TRANS_PROBS = {
    TOKEN_START: {
        POS_TAG_VERB: 0.3,
        POS_TAG_NOUN: 0.2
    },
    POS_TAG_VERB: {
        POS_TAG_VERB: 0.1,
        POS_TAG_NOUN: 0.4,
        POS_TAG_ADV: 0.4
    },
    POS_TAG_NOUN: {
        POS_TAG_VERB: 0.3,
        POS_TAG_NOUN: 0.1,
        POS_TAG_ADV: 0.1
    },
    POS_TAG_ADV: {
        TOKEN_END: 0.1
    }
}

WORD_PROB = {
    'learning': {
        POS_TAG_VERB: 0.003,
        POS_TAG_NOUN: 0.001
    },
    'changes': {
        POS_TAG_VERB: 0.004,
        POS_TAG_NOUN: 0.003
    },
    'thoroughly': {
        POS_TAG_ADV: 0.001
    },
    TOKEN_END: {
        TOKEN_END: 1
    }
}

def get_trans_probability(prev_pos_tag, current_pos_tag):
    if current_pos_tag in TRANS_PROBS[prev_pos_tag]:
        return TRANS_PROBS[prev_pos_tag][current_pos_tag]
    else:
        return 0

def calculate_viterbi_column(prev_column, token):
    curr_column = {}

    for pos_word_tag in WORD_PROB[token]:
        max_value = 0
        for pos_prev_tag in prev_column:
            pos_prev_prob = prev_column[pos_prev_tag]['value']
            prob_value = pos_prev_prob * get_trans_probability(pos_prev_tag, pos_word_tag) * WORD_PROB[token][pos_word_tag]
            if prob_value > max_value:
                max_value = prob_value
                max_prev_tag = pos_prev_tag

        if max_value > 0:
            curr_column[pos_word_tag] = {
                'value': max_value,
                'prev_tag': max_prev_tag
            }

    return curr_column

def calculate_viterbi_columns(sentence):
    curr_column = {
        TOKEN_START: {
            'value': 1
        }
    }
    columns = [curr_column]

    for token in sentence.split() + [TOKEN_END]:
        curr_column = calculate_viterbi_column(curr_column, token)
        columns.append(curr_column)

    return columns

def print_matrix(sentence, columns, print_backtrack = False):
    table = {
        '': POS_TAGS
    }
    c = 0
    tokens = [TOKEN_START] + sentence.split() + [TOKEN_END]
    for column in columns:
        token = tokens[c]
        table[token] = []
        for tag in POS_TAGS:
            if print_backtrack and tag in column and 'prev_tag' in column[tag]:
                table[token].append(str(column[tag]['value']) + ' (' + column[tag]['prev_tag'] + ')')
            elif tag in column:
                table[token].append(column[tag]['value'])
            else:
                table[token].append(0)
        c += 1

    print(tabulate(table, headers = tokens))

sentence = 'learning changes thoroughly'

columns = calculate_viterbi_columns(sentence)
print_matrix(sentence, columns, True)
