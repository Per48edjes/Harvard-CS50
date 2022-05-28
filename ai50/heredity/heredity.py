import csv
import itertools
import sys
from collections import OrderedDict
import numpy as np

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },
        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },
        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        },
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and people[person]["trait"] !=
             (person in have_trait)) for person in names)
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name":
                name,
                "mother":
                row["mother"] or None,
                "father":
                row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1))
    ]


def child_joint_probability(people, child, child_num_genes, child_has_trait,
                            people_bucket_assignment_dict):
    """
    Returns the conditional joint probability of a child possessing
    `child_num_genes` and `child_has_trait` given parent features
    """
    mother = people[child]["mother"]
    father = people[child]["father"]
    mother_num_genes = people_bucket_assignment_dict[mother]["genes"]
    father_num_genes = people_bucket_assignment_dict[father]["genes"]

    # Calculating probability child has `child_num_genes` based
    # on number of genes possessed by parents
    p_child_num_genes = child_num_gene_probability(mother_num_genes,
                                                   father_num_genes,
                                                   child_num_genes)

    # Probability `child` has `num_genes` copies of gene and `has_trait`
    p_child_in_specific_bucket = (
        p_child_num_genes * PROBS["trait"][child_num_genes][child_has_trait])

    return p_child_in_specific_bucket


def child_num_gene_probability(mother_num_genes, father_num_genes,
                               child_num_genes):
    """
    Returns probability that child has `child_num_genes` given parents'
    number of genes passed in as arguments. Accounts for mutations by
    applying Law of Total Probability via cases of 0, 1, 2 mutations on
    pair of genes coming from mother and father
    """
    # Return numpy array of mother and father genes
    mother_genes, father_genes = np.zeros(2), np.zeros(2)
    mother_genes[:mother_num_genes] = 1
    father_genes[:father_num_genes] = 1

    # `case_eval_array` does casework to see whether each case matches
    # desired `child_num_genes`
    mutation_case_order = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    cases_array = np.tile(
        np.array(np.meshgrid(mother_genes, father_genes)).T.reshape(-1, 2),
        (4, 1, 1))
    mutation_effects_array = np.tile(mutation_case_order.reshape(4, 1, 2),
                                     (1, 4, 1))
    case_eval_array = (np.abs(mutation_effects_array -
                              cases_array).sum(axis=2) == child_num_genes)

    # Build joint probability array based on cases
    mutation_case_probabilities = mutation_case_order * PROBS["mutation"]
    mutation_case_probabilities[mutation_case_probabilities == 0] = (
        1 - PROBS["mutation"])
    mutation_case_probabilities = mutation_case_probabilities.prod(
        axis=1) * (0.5**2)

    # Sum product is probability child has `child_num_genes` based on parent
    # genes and possibility of mutations
    p_num_child_genes = np.matmul(case_eval_array.T,
                                  mutation_case_probabilities).sum()
    return p_num_child_genes


def probability_parameterizer(people, one_gene, two_genes, have_trait):
    """
    Returns dictionary with each person as keys and values being dictionary
    of what features that person has (i.e, "genes" and "has_trait" are keys to
    inner dictionary)
    """
    # Isolate the `zero_genes` and `not_have_trait` groups
    zero_genes = set(people) - (one_gene.union(two_genes))
    not_have_trait = set(people) - have_trait

    # Put people into buckets based on intersection of the two features
    feature_intersections = itertools.product(
        [zero_genes, one_gene, two_genes], [have_trait, not_have_trait],
        repeat=1)

    # List of sets of people in each bucket (read: intersection of features)
    people_bucket_assignment_list = [
        a.intersection(b) for a, b in feature_intersections
    ]

    # List of bucket characteristics
    bucket_characteristics_list = list(
        itertools.product(range(3), (True, False)))

    # Construct output dictionary: keys = people, values = dictionary of bucket
    people_bucket_assignment_dict = {k: {} for k, _ in people.items()}

    for bucket_idx, group in enumerate(people_bucket_assignment_list):
        for person in group:
            people_bucket_assignment_dict[person][
                "genes"] = bucket_characteristics_list[bucket_idx][0]
            people_bucket_assignment_dict[person][
                "trait"] = bucket_characteristics_list[bucket_idx][1]

    return people_bucket_assignment_dict


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probabilities = []

    # Make lookup dict for given assignments of people to buckets
    people_bucket_assignment_dict = probability_parameterizer(
        people, one_gene, two_genes, have_trait)

    for person, bucket_features in people_bucket_assignment_dict.items():
        num_genes = bucket_features["genes"]
        has_trait = bucket_features["trait"]

        # If no parents, use genes unconditional probability distribution
        if people[person]["mother"] is None and people[person][
                "father"] is None:
            joint_probabilities.append(PROBS["gene"][num_genes] *
                                       PROBS["trait"][num_genes][has_trait])

        # Otherwise, condition on cases of parents passing down genes
        else:
            joint_probabilities.append(
                child_joint_probability(people, person, num_genes, has_trait,
                                        people_bucket_assignment_dict))

    # Multiply all joint probabilities together
    p = np.prod(joint_probabilities)
    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person, distributions in probabilities.items():

        # Update gene distribution
        if person in one_gene:
            distributions["gene"][1] += p
        elif person in two_genes:
            distributions["gene"][2] += p
        else:
            distributions["gene"][0] += p

        # Update trait distribution
        if person in have_trait:
            distributions["trait"][True] += p
        else:
            distributions["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, distributions in probabilities.items():
        for distribution in distributions.keys():
            norm_factor = sum(probabilities[person][distribution].values())
            probabilities[person][distribution] = {
                k: v / norm_factor
                for k, v in probabilities[person][distribution].items()
            }


if __name__ == "__main__":
    main()
