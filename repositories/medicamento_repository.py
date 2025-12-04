from repositories.base_repository import BaseRepository
from models.medicamento import Medicamento
from typing import List, Optional

class MedicamentoRepository(BaseRepository[Medicamento]):
    """Implementação do repositório para Medicamento."""
    
    def __init__(self):
        self._medicamentos: List[Medicamento] = []
        self._proximo_id = 1
    
    def adicionar(self, medicamento: Medicamento) -> Medicamento:
        """Adiciona um medicamento ao repositório."""
        medicamento.id = self._proximo_id
        self._medicamentos.append(medicamento)
        self._proximo_id += 1
        medicamento.atualizar_timestamp()
        return medicamento
    
    def obter_por_id(self, id: int) -> Optional[Medicamento]:
        """Obtém um medicamento pelo ID."""
        for med in self._medicamentos:
            if med.id == id:
                return med
        return None
    
    def obter_por_nome(self, nome: str) -> List[Medicamento]:
        """Obtém medicamentos pelo nome (busca parcial)."""
        return [med for med in self._medicamentos if nome.lower() in med.nome.lower()]
    
    def obter_todos(self) -> List[Medicamento]:
        """Obtém todos os medicamentos."""
        return self._medicamentos.copy()
    
    def obter_vencidos(self) -> List[Medicamento]:
        """Obtém apenas medicamentos vencidos."""
        return [med for med in self._medicamentos if med.esta_vencido()]
    
    def atualizar(self, medicamento: Medicamento) -> bool:
        """Atualiza um medicamento existente."""
        for i, med in enumerate(self._medicamentos):
            if med.id == medicamento.id:
                self._medicamentos[i] = medicamento
                medicamento.atualizar_timestamp()
                return True
        return False
    
    def remover(self, id: int) -> bool:
        """Remove um medicamento pelo ID."""
        medicamento = self.obter_por_id(id)
        if medicamento:
            self._medicamentos.remove(medicamento)
            return True
        return False
    
    def existe(self, id: int) -> bool:
        """Verifica se um medicamento existe."""
        return self.obter_por_id(id) is not None
    
    def obter_por_fabricante(self, fabricante: str) -> List[Medicamento]:
        """Obtém medicamentos por fabricante."""
        return [med for med in self._medicamentos 
                if fabricante.lower() in med.fabricante.lower()]