import __include

import animations


def tester(anim):
    print("Testing: ", anim.__class__.__name__)
    for i in range(30):
        anim.update()
        print("#" * int(anim.value * 10))


li = [
    animations.EaseOut(30),
    animations.Bounce(30, 0, 3),
    animations.Shake(0, 1),
]


for anim in li:
    tester(anim)
    print()
