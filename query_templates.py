import itertools

def parse(input_tuple):
    p1, m, yuhun, idx = input_tuple
    # parse_string = ''
    if yuhun is None:
        parse_string = f"({p1}{idx} = '{m}')"
    elif yuhun is not None:
        parse_string = f"({p1}{idx} = '{m}' and myh{idx} = '{yuhun}')"
    return parse_string


def normal_query(B, M, yuhun_M, D, yuhun_D):
    permutations_list = list(itertools.permutations(range(1, 6), 5))
    query = 'select * from dws_retail_cust_dj'
    query_list = []
    query_sub_list1 = []
    query_sub_list2 = []
    for ban in B:
        if ban is not None:
            query_list.append(f"(M1 != '{ban}' and M2 != '{ban}' and M3 != '{ban}' and M4 != '{ban}' and M5 != '{ban}' and D1 != '{ban}' and D2 != '{ban}' and D3 != '{ban}' and D4 != '{ban}' and D5 != '{ban}')\n")
    for perm in permutations_list:
        m_list = list(map(parse, [('m', m, yuhun, idx) for m, yuhun, idx in zip(M, yuhun_M, perm) if m is not None]))
        query_sub_list1.append(f"({' and '.join(m_list)})")

        d_list = list(map(parse, [('d', d, yuhun, idx) for d, yuhun, idx in zip(D, yuhun_D, perm) if d is not None]))
        query_sub_list2.append(f"({' and '.join(d_list)})")

    query_list.append(f"({' or '.join(list(set(query_sub_list1)))})")
    query_list.append(f"({' or '.join(list(set(query_sub_list2)))})")

    if query_list != []:
        query += ' where ' + ' and '.join(query_list)

    return query