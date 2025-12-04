from abc import ABC, abstractmethod
from datetime import datetime

class BaseEntity(ABC):
    """Classe abstrata base para todas as entidades do sistema."""
    
    def __init__(self, id: int):
        self._id = id
        self._data_criacao = datetime.now()
        self._data_atualizacao = datetime.now()
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID deve ser um número inteiro positivo")
        self._id = value
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Método abstrato para converter objeto em dicionário."""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """Método abstrato para representação em string."""
        pass
    
    def atualizar_timestamp(self):
        """Atualiza o timestamp de modificação."""
        self._data_atualizacao = datetime.now()