import pandas as pd
import yfinance as yf
import itertools

def generate_observation_states(n):
    movements = ['rise', 'fall']
    return list(itertools.product(movements, repeat=n))

def download_stockData(ticker1, ticker2, period):
    data = yf.download([ticker1, ticker2], period=period, progress=False, auto_adjust=True)

    for ticker in [ticker1, ticker2]:
        data[('Movement', ticker)] = data['Close'][ticker] >= data['Open'][ticker]
    data = data.dropna()

    return data

def stock_movement(ticker1, ticker2, data, shift):

    movements_ticker1 = data[('Movement', ticker1)].apply(lambda x: 'rise' if x == True else 'fall').tolist()

    data[('Movement_next', ticker1)] = data[('Movement', ticker1)].shift(shift*-1)
    data = data.dropna()

    movements_shift_ticker1 = data[('Movement_next', ticker1)].apply(
        lambda x: 'rise' if x == True else 'fall').tolist()
    movements_ticker2 = data[('Movement', ticker2)].apply(lambda x: 'rise' if x == True else 'fall').tolist()

    return movements_ticker1, movements_ticker2, movements_shift_ticker1

def calc_prob_trans(movements):
    bull_to_bull, bull_to_bear, bear_to_bull, bear_to_bear = 0, 0, 0, 0
    for i in range(len(movements[0]) - 1):
        if movements[0][i] == 'rise' and movements[0][i + 1] == 'rise':
            bull_to_bull += 1
        elif movements[0][i] == 'rise' and movements[0][i + 1] == 'fall':
            bull_to_bear += 1
        elif movements[0][i] == 'fall' and movements[0][i + 1] == 'rise':
            bear_to_bull += 1
        elif movements[0][i] == 'fall' and movements[0][i + 1] == 'fall':
            bear_to_bear += 1

    total_from_bull = bull_to_bull + bull_to_bear
    total_from_bear = bear_to_bull + bear_to_bear

    prob_trans = {
        'P(Rise | Rise)': bull_to_bull / total_from_bull if total_from_bull > 0 else 0,
        'P(Fall | Rise)': bull_to_bear / total_from_bull if total_from_bull > 0 else 0,
        'P(Rise | Fall)': bear_to_bull / total_from_bear if total_from_bear > 0 else 0,
        'P(Fall | Fall)': bear_to_bear / total_from_bear if total_from_bear > 0 else 0,
    }

    return prob_trans

def calc_init_dist(movements):
    bull_to_bull, bull_to_bear, bear_to_bull, bear_to_bear = 0, 0, 0, 0
    for i in range(len(movements[0]) - 1):
        if movements[0][i] == 'rise' and movements[0][i + 1] == 'rise':
            bull_to_bull += 1
        elif movements[0][i] == 'rise' and movements[0][i + 1] == 'fall':
            bull_to_bear += 1
        elif movements[0][i] == 'fall' and movements[0][i + 1] == 'rise':
            bear_to_bull += 1
        elif movements[0][i] == 'fall' and movements[0][i + 1] == 'fall':
            bear_to_bear += 1

    total_from_bull = bull_to_bull + bull_to_bear
    total_from_bear = bear_to_bull + bear_to_bear

    initial_dist = {'rise': total_from_bull / (total_from_bull + total_from_bear),
                    'fall': total_from_bear / (total_from_bull + total_from_bear)}

    return initial_dist

def calc_prob_ems(movements):

    s1bull_s2bull, s1bull_s2bear, s1bear_s2bull, s1bear_s2bear = 0, 0, 0, 0
    for i in range(len(movements[2]) - 1):
        if movements[2][i] == 'rise' and movements[1][i] == 'rise':
            s1bull_s2bull += 1
        elif movements[2][i] == 'rise' and movements[1][i] == 'fall':
            s1bull_s2bear += 1
        elif movements[2][i] == 'fall' and movements[1][i] == 'rise':
            s1bear_s2bull += 1
        elif movements[2][i] == 'fall' and movements[1][i] == 'fall':
            s1bear_s2bear += 1

    total_s1_bull = s1bull_s2bull + s1bull_s2bear
    total_s1_bear = s1bear_s2bull + s1bear_s2bear

    prob_ems = {
        'P(S2 Rise | S1 Rise)': s1bull_s2bull / total_s1_bull if total_s1_bull > 0 else 0,
        'P(S2 Fall | S1 Rise)': s1bull_s2bear / total_s1_bull if total_s1_bull > 0 else 0,
        'P(S2 Rise | S1 Fall)': s1bear_s2bull / total_s1_bear if total_s1_bear > 0 else 0,
        'P(S2 Fall | S1 Fall)': s1bear_s2bear / total_s1_bear if total_s1_bear > 0 else 0,
    }

    return prob_ems

def calc_best_path(observation_states, prob_ems, prob_trans, T, initial_dist):
    states = ['rise', 'fall']
    viterbi_matrix = pd.DataFrame(0.0, index=states, columns=range(T))
    backpointers = pd.DataFrame("", index=states, columns=range(T))

    iter = []
    best_state = []

    for o in range(len(observation_states)):
        step = 0
        for s in observation_states[o]:
            for t in states:
                emiss_key = f'P(S2 {s.capitalize()} | S1 {t.capitalize()})'
                if step == 0:
                    viterbi_matrix.loc[t, step] = initial_dist[t] * prob_ems.get(emiss_key)
                elif step > 0:
                    if t == 'rise':
                        if viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Rise | Rise)'] > viterbi_matrix.loc[
                            states[1], step - 1] * prob_trans['P(Fall | Rise)']:
                            prob_max = viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Rise | Rise)']
                            backpointers.loc[t, step] = states[0]
                        else:
                            prob_max = viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Fall | Rise)']
                            backpointers.loc[t, step] = states[1]
                    elif t == 'fall':
                        if viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Rise | Fall)'] > viterbi_matrix.loc[
                            states[1], step - 1] * prob_trans['P(Fall | Fall)']:
                            prob_max = viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Rise | Fall)']
                            backpointers.loc[t, step] = states[0]
                        else:
                            prob_max = viterbi_matrix.loc[states[0], step - 1] * prob_trans['P(Fall | Fall)']
                            backpointers.loc[t, step] = states[1]
                    viterbi_matrix.loc[t, step] = prob_ems.get(emiss_key) * prob_max
            step += 1
        iter.append(viterbi_matrix.copy())
        best_state.append(backpointers.copy())

    trace_path = pd.DataFrame("", index=['path'], columns=range(T))
    best_path = []

    for i in range(len(best_state)):
        if iter[i].loc[states[0], T - 1] > iter[i].loc[states[1], T - 1]:
            trace_path.loc[0, T - 1] = states[0]
        else:
            trace_path.loc[0, T - 1] = states[1]
        for p in range(T - 1):
            trace_path.loc[0, T - p - 2] = best_state[i].loc[trace_path.loc[0, T - 1], T - p - 1]
        best_path.append(trace_path.copy())

    results_map = dict(zip(observation_states, best_path))

    return results_map

def calc_accuracies(observation_states, results_map, movements, T):
    obsv_correct, obsv_wrong = dict.fromkeys(observation_states, 0), dict.fromkeys(observation_states, 0)

    count_correct = 0
    total = 0
    for i in range(len(movements[1]) - T):
        for j in range(T):
            if results_map[tuple(movements[1][i:i + T])].loc[0, j] == movements[2][i + j]:
                count_correct += 1
                total += 1
                obsv_correct[tuple(movements[1][i:i + T])] += 1
            else:
                total += 1
                obsv_wrong[tuple(movements[1][i:i + T])] += 1

    obsv_accuracies = {
        key: obsv_correct[key] / (obsv_correct[key] + obsv_wrong[key])
        for key in obsv_correct.keys() & obsv_wrong.keys() if obsv_correct[key] + obsv_wrong[key] > 0
    }

    sorted_obsv_accuracies = dict(sorted(obsv_accuracies.items(), key=lambda item: item[1], reverse=True))

    accuracies = (count_correct / total) * 100

    print("OVERALL ACCURACIES: ", (count_correct / total) * 100, "%\n")

    for key in sorted_obsv_accuracies:
        print("OBSERVATION: ", {key}, " : ", obsv_correct[key], "of ", obsv_correct[key] + obsv_wrong[key],
              "\nPATH: ",
              results_map[key], "\nACCURACY: ", sorted_obsv_accuracies[key])
        print("\n")

    return accuracies