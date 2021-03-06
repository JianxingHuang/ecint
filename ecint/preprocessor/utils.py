from ase.io import read
from aiida.orm import StructureData
import json


def path2structure(structure_path, cell, pbc=True):
    """
    :param structure_path:
    :param cell: (list) cell parameters, can be set as [(1,0,0), (0,1,0), (0,0,1)] or like [1, 1, 1, 90, 90, 90],
                 units: angstrom, angle
    :param pbc: periodic boundary conditions, can be set as [False, False, True]
    :return: StructureData
    """
    atoms = read(structure_path)
    atoms.set_cell(cell)
    if (atoms.cell == 0).all():
        raise ValueError('The cell parameters can not be all zero.')
    else:
        atoms.set_pbc(pbc)
        # structure = StructureData(ase=atoms)
    return atoms


def load_json(json_path):
    with open(json_path) as f:
        d = json.load(f)
    return d


def inp2json(cp2k_input):
    # TODO: need edit, parse cp2k input file to json format
    pass
