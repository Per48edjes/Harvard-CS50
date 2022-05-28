import sys

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop over all variables in puzzle
        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                # Remove those words that are inconsistent with variable's
                # unary constraint (i.e., length)
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get i, j for overlap between `x`, `y`
        i, j = self.crossword.overlaps[x, y]
        revised = False
        for x_word in self.domains[x].copy():
            constraint_satisfied = False
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    constraint_satisfied = True
            if not constraint_satisfied:
                self.domains[x].remove(x_word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Gather all arcs in puzzle or designated subset
        if not arcs:
            queue = [
                (v1, v2)
                for (v1, v2), overlap in self.crossword.overlaps.items()
                if overlap is not None
            ]
        else:
            queue = arcs

        # Keep pulling from queue if at least 1 arc remains
        while len(queue) > 0:
            x, y = queue.pop()
            # If changes were made to make it consistent, further action needed
            if self.revise(x, y):
                # Return False if unsolvable
                if len(self.domains[x]) == 0:
                    return False
                # Take all of x’s neighbors except y; add the arcs between them
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Return True if all variables are assigned to words
        return len(self.crossword.variables) == len(assignment)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # All words are unique
        words = assignment.values()
        if len(words) != len(set(words)):
            return False
        for var, word in assignment.items():
            # All words assigned to variables are correct length
            if len(word) != var.length:
                return False
            # All words sharing proper overlap with neighbors (if neighbors are
            # already in `assignment`)
            for neighbor in self.crossword.neighbors(var):
                i, j = self.crossword.overlaps[var, neighbor]
                try:
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
                except KeyError:
                    continue
        # Return True if and only if every variable in the assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def least_constraining_heuristic(word):
            """
            Return the number of values eliminated from neighbor variables for a
            given choice of word for a given variable
            """
            eliminated_neighbor_values_count = 0
            for neighbor in self.crossword.neighbors(var):
                # Ignore `neighbors` already in `assignment`
                if neighbor not in assignment.keys():
                    i, j = self.crossword.overlaps[var, neighbor]
                    for neighbor_word in self.domains[neighbor]:
                        if word[i] != neighbor_word[j]:
                            eliminated_neighbor_values_count += 1
            return eliminated_neighbor_values_count

        # Return list of values `var` could take on ordered by the least
        # constraining heuristic
        least_constraining_values = sorted(
            self.domains[var], key=least_constraining_heuristic
        )
        return least_constraining_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = [
            var for var in self.crossword.variables if var not in assignment.keys()
        ]

        # First sort on minimum remaining values
        remaining_value_sort = sorted(
            unassigned_vars, key=lambda var: len(self.domains[var])
        )

        # Then sort on maximum degree
        degree_sort = sorted(
            remaining_value_sort,
            key=lambda var: len(self.crossword.neighbors(var)),
            reverse=True,
        )

        return degree_sort[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: `assignment` complete
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                # Make copy of domain in case we have to revert inferences and
                # keep track of `inferences_made`
                domain_copy = self.domains.copy()
                inferences_made = []
                # Isolate all arcs `var` is involved in
                arcs = [(var, neighbor) for neighbor in self.crossword.neighbors(var)]
                if not self.ac3(arcs=arcs):
                    # If ac3 fails, restore domains
                    self.domains = domain_copy
                else:
                    # Add "inferences" to `assignment`
                    for _, neighbor in arcs:
                        if len(self.domains[neighbor]) == 1:
                            assignment[neighbor] = next(iter(self.domains[neighbor]))
                            if self.consistent(assignment):
                                inferences_made.append(neighbor)
                                continue
                            else:
                                del assignment[neighbor]
                # Recursive case: try `backtrack` on "new" `assignment`
                result = self.backtrack(assignment)
                if result:
                    return result
                # Remove the inferences if they lead to problems later
                for neighbor in inferences_made:
                    del assignment[neighbor]
            # Remove "newly" assigned `var` if it leads to a problem later
            del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
