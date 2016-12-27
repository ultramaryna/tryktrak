import random

def rzut_kostka():
    rzuty = []
    rzuty.append(random.randint(1,6))
    rzuty.append(random.randint(1,6))
    if rzuty[0] == rzuty[1]:
        rzuty.append(rzuty[0])
        rzuty.append(rzuty[0])
    return rzuty
