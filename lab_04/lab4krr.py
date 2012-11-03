from orderedset import OrderedSet

def is_conclusion(premise, conclusion):
    """Tests if a premise is a valid conclusion
    :param frozenset premise
    :param frozenset conclusion
    :return boolean
    """
    assert isinstance(premise, frozenset)
    assert isinstance(conclusion, frozenset)
    return len(premise & conclusion) == len(premise)

def proposition_negation(proposition):
    """Given a proposition, returns its negation
    e.g.: 'p'  -> '!p'
          '!p' -> 'p'
    :param string proposition
    :return string
    """
    if proposition.startswith('!'):
        return proposition[1:]
    else:
        return '!' + proposition

def is_negation_in_premise(proposition, premise):
    """Checks if the negation of the proposition is in the given premise
    :param string proposition
    :param set premise
    :return boolean
    """
    assert isinstance(premise, frozenset)
    return premise.issuperset([proposition_negation(proposition)])

def combine_premises(premise1, premise2):
    """Combines two premises into new different premises"""
    new_premises = OrderedSet()
    for prop in premise1:
        if is_negation_in_premise(prop, premise2):
            new_premises = new_premises | OrderedSet([frozenset(premise1.difference([prop]) | \
                               premise2.difference([proposition_negation(prop)]))])

    return new_premises


def missing_proposition(premise1, premise2, combined_premise):
    """Given 2 premises and one which is combined from the first two, finds
    the proposition which was removed from both premises in order to be obtained
    the combined_premise"""
    return (list(premise1 - combined_premise)[0], list(premise2 - combined_premise)[0])


def main(premises, conclusion):
    """Given a set of premises and a conclusion, tries to find a direct proof"""

    conclusion_not_found = True

    # Combine all the premises from the given set until a conclusion is found
    # or when at an iteration point no new premises or found
    # Since we must track the initial premises which formed the conclusion,
    # keep in another data structure the indexes of initial premises which
    # form a new premise
    track_premise = {}  # Use a hash of all premises for fast lookup when
                        # wanting to track new premises
    premise_idx = []    # remember the indexes of the new premises, will be
                        # used on the final printing

    for idx, premise in enumerate(list(premises)):
        track_premise[premise] = idx
        premise_idx.append((premise, (idx)))

    while conclusion_not_found:
        new_premises = OrderedSet()
        premises_list = list(premises)
        length = len(premises_list)
        for idx1 in range(0, length - 1):
            premise1 = frozenset(premises_list[idx1])
            for idx2 in range(idx1+1, length):
                premise2 = frozenset(premises_list[idx2])

                combined_premises = combine_premises(premise1, premise2)
                new_premises = new_premises | combined_premises
                # Track the new formed premises
                for premise in list(new_premises):
                    if not track_premise.get(premise):
                        track_premise[premise] = (idx1, idx2)
                        premise_idx.append((premise, (idx1, idx2)))

                if is_conclusion(premise1, conclusion) or is_conclusion(premise2,
                    conclusion):
                    conclusion_not_found = False

        if len(new_premises) == 0: # no new premises were added
            # since the conclusion was not found we can assume that the
            # given conclusion cannot by obtained from the initial set of premises
            print 'There is not direct proof'
            return
        else:
            premises = premises | new_premises

    premises_list = list(premises)
    for idx, premise in enumerate(premise_idx):
        if not isinstance(premise[1], tuple):
            print '%s.%s <- premise' % (idx+1, list(premise[0]))
        else:
            print '%s.%s <- %s %s' % (idx+1, list(premise[0]), map(lambda x: x+1, premise[1]),
                                   missing_proposition(
                                        premises_list[premise[1][0]],
                                        premises_list[premise[1][1]],
                                        premise[0]))

def test():

    # Test is_conclusion
    f = is_conclusion
    assert f(frozenset(['p', 'q', 'r']), frozenset(['p', 'q', 'r']))
    assert f(frozenset(['p', 'q']), frozenset(['q', 'r'])) == False
    assert f(frozenset(['!p', 'q']), frozenset(['p', 'q'])) == False
    assert f(frozenset(['!p', 'q']), frozenset(['q', '!p']))

    # Test proposition_negation
    f = proposition_negation
    assert f('p') == '!p'
    assert f('!p') == 'p'

     # Test is_negation_in_premise
    f = is_negation_in_premise
    assert f('p',  frozenset(['p', 'q', 'r'])) == False
    assert f('!p', frozenset(['p', 'q', 'r'])) == True
    assert f('!r', frozenset(['p', 'q', 'r'])) == True
    assert f('p',  frozenset(['!p'])) == True

    # Test combine_premises
    f = combine_premises
    assert len(f(frozenset(['p', '!q', 'r']), frozenset(['p', 'q', 'r'])) & \
            OrderedSet([frozenset(['p', 'r'])])) == 1
    assert len(f(frozenset(['p', 'q']), frozenset(['!p', '!q'])) & \
            OrderedSet([frozenset(['p', '!p']), frozenset(['q', '!q'])])) == 2

    print 'All tests pass'

if __name__ == '__main__':
    test()
    # Hard code some input data from the pdf file
    premises = OrderedSet([frozenset(['!p', '!q', 'r']), frozenset(['!p', 'q', 's']),
         frozenset(['!r', 't']), frozenset(['!s', 't'])])
    conclusion = frozenset(['!p', 't'])

    main(premises, conclusion)
