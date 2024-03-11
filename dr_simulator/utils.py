""" This module contains utility functions for DR Simulator """

import json
import pickle


def pickle_load(path):
    """Loads a pickled object (fitted model, dictionary with data, etc)

    Parameters
    ----------
    path : str
        path to object to load

    Returns
    -------
    object
        unpickled object found at the `path`
    """
    with open(path, "rb") as f:
        object_ = pickle.load(f)
    return object_


def pickle_dump(object_, path):
    """Pickles an object (fitted model, dictionary with data, etc)

    Parameters
    ----------
    object_
        object to compress

    path : str
        path where the pickled object is saved
    """
    with open(path, "wb") as f:
        pickle.dump(object_, f)


def json_load(path):
    """Loads a json string to python

    Parameters
    ----------
    path : str
        path to object to load

    Returns
    -------
    object_ : object
        python object converted from str
    """
    with open(path, "r", encoding="utf-8") as f:
        object_ = json.load(f)
    return object_


def json_dump(object_, path):
    """Dumps a python object to a json string

    Parameters
    ----------
    object_ : object
        python object to convert to str

    path : str
        path where the json string is saved
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(object_, f, ensure_ascii=False, indent=4)
