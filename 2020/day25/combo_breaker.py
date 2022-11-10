import aoc


INITIAL_SUBJECT = 7
MOD_NO = 20201227

def transform(subject: int, target: int) -> int:
    loops = 1
    val = subject
    while val != target:
        val = (val * subject) % MOD_NO
        loops += 1
    return loops


def main():
    aoc.setup(__file__)
    card_pubkey, door_pubkey = map(int, aoc.read_lines())
    door_loop = transform(subject=INITIAL_SUBJECT, target=door_pubkey)
    encryption_key = card_pubkey
    for _ in range(door_loop-1):
        encryption_key = (encryption_key * card_pubkey) % MOD_NO
    aoc.answer(1, encryption_key)

if __name__ == '__main__':
    main()
