from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T', bound='BaseEntity')

class BaseRepository(ABC, Generic[T]):
    """Interface abstrata para repositórios."""
    
    @abstractmethod
    def adicionar(self, entidade: T) -> T:
        pass
    
    @abstractmethod
    def obter_por_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def obter_todos(self) -> List[T]:
        pass
    
    @abstractmethod
    def atualizar(self, entidade: T) -> bool:
        pass
    
    @abstractmethod
    def remover(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def existe(self, id: int) -> bool:
        pass