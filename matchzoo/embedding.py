"""Matchzoo toolkit for token embedding."""

import abc
import csv
import typing

import numpy as np
import pandas as pd


class Embedding(abc.ABC):
    """
    Embedding class.
    """

    def __init__(self):
        """Init."""
        self._vocab = {}
        self._matrix = None
    
    @abc.abstractmethod
    def _entity_to_vec(self, entity: str):
        """Get word embedding by entity."""
    
    def __getitem__(self, entities: typing.Union[str, list]):
        """Get embeddings by entity of list of entities."""
        if isinstance(entities, str):
            return self._entity_to_vec(entities)
        
        return np.vstack([self._entity_to_vec(entity) for entity in entities])
    
    def __contains__(self, entity):
        """"""
        return entity in self._vocab
    
    @property
    def dimension(self):
        """"""
        return self._matrix.shape[1]
    
    @property
    def matrix(self):
        """"""
        return self._matrix
    
    @matrix.setter
    def matrix(self, matrix_instance):
        self._matrix = matrix_instance

class RandomInitializedEmbedding(Embedding):
    """
    Random Initialized WordEmbedding.
    """
    def __init__(
        self,
        vocab: dict,
        dimension: int,
        random_scale: float = 0.2):
        """Initialization."""
        self._vocab = vocab # term index.
        self._dimension = dimension
        self._matrix = np.random.uniform(-random_scale,
                                         random_scale,
                                         (len(self._vocab), self._dimension))
    
    def _entity_to_vec(self, entity):
        """"""
        return self._matrix[self._vocab[entity]]

class PretrainedEmbedding(Embedding):
    """Pretrained."""

    def __init__(self):
        """"""
        self._vocab = self._matrix.index.values

    def _entity_to_vec(self, entity):
        """"""
        return self._matrix.loc[entity].values
    
    @abc.abstractmethod
    def _read_embedding(self, file_path: str):
        """Read embedding file given dir."""


class Word2Vec(PretrainedEmbedding):
    """Word2Vec.

    Examples:
        >>> word2vec = Word2Vec('tests/sample/embed_10.txt')
        >>> word2vec.dimension
        10
        >>> word2vec.matrix SKIP
        >>> word2vec['fawn']
        [...]
        >>> word2vec['fawn', 'abondon']
        [[...], [...]]
        >>> 'oov' in word2vec
        False
    """
    def __init__(
        self,
        file_path: str
    ):
        """Init."""
        self._matrix = self._read_embedding(file_path)
        super().__init__()
    
    def _read_embedding(self, file_path: str):
        return pd.read_table(file_path,
                             sep=" ",
                             index_col=0,
                             header=None,
                             skiprows=1)


class Glove(PretrainedEmbedding):
    """Glove.

    Examples:
        >>> glove = Glove('tests/sample/embed_10.txt')
        >>> glove.dimension
        10
        >>> glove.matrix
        [[...],
         [...]]
        >>> glove['fawn']
        [...]
        >>> glove['fawn', 'abondon']
        [[...], [...]]
        >>> 'oov' in glove
        False
    """
    def __init__(
        self,
        file_path: str,
    ):
        """Init."""
        self._matrix = self._read_embedding(file_path)
        super().__init__()
    
    def _read_embedding(self, file_path: str):
        return pd.read_table(file_path,
                             sep=" ",
                             index_col=0,
                             header=None,
                             quoting=csv.QUOTE_NONE)
