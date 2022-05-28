import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pmf = {}

    if corpus[page]:
        for link in corpus:
            pmf[link] = (1 - damping_factor) / len(corpus)
            if link in corpus[page]:
                pmf[link] += damping_factor / len(corpus[page])
    else:
        # Pick page in uniformly random way if no outbound links
        for link in corpus:
            pmf[link] = 1 / len(corpus)

    return pmf


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = {}
    sample = None

    for page in corpus:
        pagerank_dict[page] = 0

    for _ in range(n):
        if not sample:
            sample = random.choices(list(corpus.keys()), k=1)[0]
        else:
            trans_model = transition_model(corpus, sample, damping_factor)
            pages, weights = zip(*trans_model.items())
            sample = random.choices(pages, weights, k=1)[0]
        pagerank_dict[sample] += 1

    # Normalize so valid PMF is returned
    for page in corpus:
        pagerank_dict[page] /= n

    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence within tolerance.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Instantiate containing data structures
    pagerank_dict, new_pagerank_dict = {}, {}

    # Assign initial PR value to all pages in corpus
    for page in corpus:
        pagerank_dict[page] = 1 / len(corpus)

    update = True
    while update:
        for page in pagerank_dict:
            total = 0
            for possible_page in corpus:
                # Do reverse search
                if page in corpus[possible_page]:
                    total += pagerank_dict[possible_page] / len(corpus[possible_page])
                # Pages with no links are treated as if they have links to all pages
                if not corpus[possible_page]:
                    total += pagerank_dict[possible_page] / len(corpus)

            new_pagerank_dict[page] = (1 - damping_factor) / len(
                corpus
            ) + damping_factor * total

        update = False

        # Repeat until all pages are updated by less than threshold
        for page in pagerank_dict:
            if not math.isclose(
                new_pagerank_dict[page], pagerank_dict[page], abs_tol=0.001
            ):
                update = True
            # Assign new values to current values
            pagerank_dict[page] = new_pagerank_dict[page]

    return pagerank_dict


if __name__ == "__main__":
    main()
