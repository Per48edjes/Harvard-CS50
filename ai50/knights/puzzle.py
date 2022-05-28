from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

AclaimsAKnight = Symbol("A claims to be a Knight")
AclaimsAKnave = Symbol("A claims to be a Knave")

AclaimsBKnight = Symbol("A claims B is a Knight")
AclaimsBKnave = Symbol("A claims B is a Knave")

BclaimsBKnight = Symbol("B claims B is a Knight")
BclaimsBKnave = Symbol("B claims B is a Knave")

BclaimsAKnight = Symbol("B claims A is a Knight")
BclaimsAKnave = Symbol("B claims A is a Knave")

BsaysAclaimsAKnave = Symbol("B says 'A claims to be a Knave'")
BclaimsCKnave = Symbol("B claims C is a Knave")

CclaimsAKnight = Symbol("C claims A is a Knight")

# Puzzle 0
# A says "I am both a knight and a knave."
Astatements0 = And(AclaimsAKnight, AclaimsAKnave)
knowledge0 = And(
    # Knight/Knave definitions
    Biconditional(AKnight, Not(AKnave)),
    # Puzzle facts
    Implication(AclaimsAKnight, Or(AKnight, AKnave)),
    Implication(AclaimsAKnave, Not(Or(AKnight, AKnave))),
    # Liars are Knaves
    Biconditional(Not(Astatements0), AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Astatements1 = And(AclaimsAKnave, AclaimsBKnave)
knowledge1 = And(
    # Knight/Knave definitions
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # Puzzle facts
    Or(BKnight, BKnave),
    Implication(AclaimsAKnave, Not(Or(AKnight, AKnave))),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(And(AKnight, AclaimsBKnave), BKnave),
    # Liars are Knaves
    Biconditional(Not(Astatements1), AKnave),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Astatements2 = Or(And(AclaimsAKnight, AclaimsBKnight),
                  And(AclaimsAKnave, AclaimsBKnave))
Bstatements2 = Not(Astatements2)
knowledge2 = And(
    # Knight/Knave definitions
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    # Puzzle facts
    Implication(And(AKnight, Astatements2), BKnight),
    # Liars are Knaves
    Biconditional(Not(Astatements2), AKnave),
    Biconditional(Not(Bstatements2), BKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Astatements3 = And(Or(AclaimsAKnight, AclaimsAKnave),
                   Not(And(AclaimsAKnight, AclaimsAKnave)))
Bstatements3 = And(BsaysAclaimsAKnave, BclaimsCKnave)
Cstatements3 = CclaimsAKnight
knowledge3 = And(
    # Knight/Knave definitions
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    # Puzzle facts
    Biconditional(AclaimsAKnight, Not(AclaimsAKnave)),
    Implication(BKnight, And(AclaimsAKnave, CKnave)),
    Implication(AKnight, CKnight),
    # Liars are Knaves
    Biconditional(Not(Astatements3), AKnave),
    Biconditional(Not(Bstatements3), BKnave),
    Biconditional(Not(Cstatements3), CKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
