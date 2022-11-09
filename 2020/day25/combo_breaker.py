
with open('2020/day25/data.txt') as f:
    CARD_PUBKEY, DOOR_PUBKEY = map(int, f.read().splitlines())
INITIAL_SUBJECT = 7
MOD_NO = 20201227


def transform(subject: int, target: int) -> int:
    loops = 1
    val = subject
    while val != target:
        val = (val * subject) % MOD_NO
        loops += 1
    return loops

card_loop = transform(subject=INITIAL_SUBJECT, target=CARD_PUBKEY)
door_loop = transform(subject=INITIAL_SUBJECT, target=DOOR_PUBKEY)
print(card_loop, door_loop)

asdf = CARD_PUBKEY
for x in range(door_loop-1):
    asdf = (asdf * CARD_PUBKEY) % MOD_NO
print(asdf)
