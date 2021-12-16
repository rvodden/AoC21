from itertools import islice
import pandas as pd
import numpy as np

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> [s0,s1,...s[n-1]], [s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = list(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + [elem]
        yield result

def inc(d, k, step=1):
    try:
        d[k] += step
    except KeyError:
        d[k] = step

class Polymerization:
    @staticmethod
    def most_minus_least(start_string: str, polymer_template, steps=10):

        molecule_totals = {}
        atom_totals = {}

        munge_template = { k: (k[0] + v, v + k[1]) for k,v in polymer_template.items() }

        for atoms in window(start_string):
            molecule = ''.join(atoms)
            inc(molecule_totals, molecule)

            for atom in atoms:
                inc(atom_totals, atom)

        for i in range(steps):
            print(".", end="")
            mol_tots_copy = molecule_totals.copy()
            for molecule, number_of_molecules in mol_tots_copy.items():
                molecule_totals[molecule] -= number_of_molecules
                new_molecules = munge_template[molecule]
                
                for new_molecule in new_molecules:
                    inc(molecule_totals, new_molecule, number_of_molecules)
                inc(atom_totals,polymer_template[molecule], number_of_molecules)
        print()

        atom_counts = atom_totals.values()
        return max(atom_counts) - min(atom_counts)