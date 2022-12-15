import cmp

gates = []

alice_input = {
    'k30': cmp.gen(),
    'k31': cmp.gen(),
    'k40': cmp.gen(),
    'k41': cmp.gen(),
    'k60': cmp.gen(),
    'k61': cmp.gen(),
}

bob_input = {
    'k10': cmp.gen(),
    'k11': cmp.gen(),
    'k20': cmp.gen(),
    'k21': cmp.gen(),
    'k50': cmp.gen(),
    'k51': cmp.gen(),
}

alice_key = {}


def build_circuit():
    k10 = bob_input['k10']
    k11 = bob_input['k11']
    k70 = cmp.gen()
    k71 = cmp.gen()
    gates.append(cmp.NOT(k10, k11, k70, k71))  # 0
    k40 = alice_input['k40']
    k41 = alice_input['k41']
    k80 = cmp.gen()
    k81 = cmp.gen()
    gates.append(cmp.NOT(k40, k41, k80, k81))  # 1
    k60 = alice_input['k60']
    k61 = alice_input['k61']
    k90 = cmp.gen()
    k91 = cmp.gen()
    gates.append(cmp.NOT(k60, k61, k90, k91))  # 2
    k20 = bob_input['k20']
    k21 = bob_input['k21']
    k100 = cmp.gen()
    k101 = cmp.gen()
    gates.append(cmp.AND(k20, k21, k80, k81, k100, k101))  # 3
    k50 = bob_input['k50']
    k51 = bob_input['k51']
    k110 = cmp.gen()
    k111 = cmp.gen()
    gates.append(cmp.AND(k50, k51, k90, k91, k110, k111))  # 4
    k30 = alice_input['k30']
    k31 = alice_input['k31']
    k140 = cmp.gen()
    k141 = cmp.gen()
    gates.append(cmp.AND(k70, k71, k30, k31, k140, k141))  # 5
    k120 = cmp.gen()
    k121 = cmp.gen()
    gates.append(cmp.NOT(k100, k101, k120, k121))  # 6
    k130 = cmp.gen()
    k131 = cmp.gen()
    gates.append(cmp.NOT(k110, k111, k130, k131))  # 7
    k150 = cmp.gen()
    k151 = cmp.gen()
    gates.append(cmp.AND(k120, k121, k130, k131, k150, k151))  # 8
    k160 = cmp.gen()
    k161 = cmp.gen()
    gates.append(cmp.OR(k140, k141, k150, k151, k160, k161))  # 9
    return [k160, k161]


def dec_not_gate(gate, k):
    for t in gate:
        r, c = t[0], t[1]
        x = cmp.DEC(k, r, c)
        if x:
            return x


def dec_and_or_gate(gate, k1, k2):
    k = k1
    r = k2
    for t in gate:
        x = cmp.DEC(k, r, t)
        if x:
            return x


def alice_set_key(a1, a0):
    if a0 == 0:
        k6 = alice_input['k60']
    else:
        k6 = alice_input['k61']
    alice_key['k6'] = k6
    if a1 == 0:
        k3 = alice_input['k30']
        k4 = alice_input['k40']
    else:
        k3 = alice_input['k31']
        k4 = alice_input['k41']
    alice_key['k3'] = k3
    alice_key['k4'] = k4


def evaluate(b1, b0):
    if b0 == 0:
        k5 = bob_input['k50']
    else:
        k5 = bob_input['k51']
    if b1 == 0:
        k1 = bob_input['k10']
        k2 = bob_input['k20']
    else:
        k1 = bob_input['k11']
        k2 = bob_input['k21']
    gate = gates[0]
    k7 = dec_not_gate(gate, k1)
    gate = gates[1]
    k4 = alice_key['k4']
    k8 = dec_not_gate(gate, k4)
    gate = gates[2]
    k6 = alice_key['k6']
    k9 = dec_not_gate(gate, k6)
    gate = gates[3]
    k10 = dec_and_or_gate(gate, k2, k8)
    gate = gates[4]
    k11 = dec_and_or_gate(gate, k5, k9)
    gate = gates[5]
    k3 = alice_key['k3']
    k14 = dec_and_or_gate(gate, k7, k3)
    gate = gates[6]
    k12 = dec_not_gate(gate, k10)
    gate = gates[7]
    k13 = dec_not_gate(gate, k11)
    gate = gates[8]
    k15 = dec_and_or_gate(gate, k12, k13)
    gate = gates[9]
    k16 = dec_and_or_gate(gate, k14, k15)
    return ''.join(k16)


def ge(a, b):
    output = build_circuit()
    k160, k161 = output
    a1, a0 = int(a[0]), int(a[1])
    b1, b0 = int(b[0]), int(b[1])
    alice_set_key(a1, a0)
    result = evaluate(b1, b0)
    if result == k160:
        return 0
    elif result == k161:
        return 1
    else:
        return -1


def main():
    a = '01'
    b = '10'
    ans = ge(a, b)
    if ans == 0:
        print(a, b, 'a < b')
    elif ans == 1:
        print(a, b, 'a >= b')
    else:
        print('error!')


if __name__ == '__main__':
    main()
