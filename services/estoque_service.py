from repositories.medicamento_repository import MedicamentoRepository
from models.medicamento import Medicamento
from typing import List, Optional, Dict

class EstoqueService:
    """Serviço que gerencia as operações de estoque."""
    
    def __init__(self):
        self._repository = MedicamentoRepository()
    
    def cadastrar_medicamento(self, dados: Dict) -> Medicamento:
        """Cadastra um novo medicamento."""
        try:
            medicamento = Medicamento(
                id=0,  # Será definido pelo repositório
                nome=dados['nome'],
                lote=dados['lote'],
                validade=dados['validade'],
                fabricante=dados['fabricante'],
                quantidade=dados.get('quantidade', 0)
            )
            return self._repository.adicionar(medicamento)
        except KeyError as e:
            raise ValueError(f"Campo obrigatório faltando: {e}")
    
    def listar_medicamentos(self, apenas_ativos: bool = True) -> List[Medicamento]:
        """Lista medicamentos, opcionalmente filtrando vencidos."""
        if apenas_ativos:
            return [med for med in self._repository.obter_todos() 
                    if not med.esta_vencido()]
        return self._repository.obter_todos()
    
    def buscar_medicamento(self, id: int) -> Optional[Medicamento]:
        """Busca um medicamento pelo ID."""
        return self._repository.obter_por_id(id)
    
    def buscar_por_nome(self, nome: str) -> List[Medicamento]:
        """Busca medicamentos pelo nome."""
        return self._repository.obter_por_nome(nome)
    
    def atualizar_medicamento(self, id: int, dados: Dict) -> bool:
        """Atualiza um medicamento existente."""
        medicamento = self._repository.obter_por_id(id)
        if not medicamento:
            return False
        
        # Atualiza apenas os campos fornecidos
        for campo, valor in dados.items():
            if valor:  # Não atualiza se o valor for vazio
                if hasattr(medicamento, campo):
                    setattr(medicamento, campo, valor)
        
        return self._repository.atualizar(medicamento)
    
    def remover_medicamento(self, id: int) -> bool:
        """Remove um medicamento."""
        return self._repository.remover(id)
    
    def adicionar_quantidade(self, id: int, quantidade: int) -> bool:
        """Adiciona quantidade ao estoque de um medicamento."""
        medicamento = self._repository.obter_por_id(id)
        if medicamento:
            medicamento.quantidade += quantidade
            return self._repository.atualizar(medicamento)
        return False
    
    def remover_quantidade(self, id: int, quantidade: int) -> bool:
        """Remove quantidade do estoque de um medicamento."""
        medicamento = self._repository.obter_por_id(id)
        if medicamento and medicamento.quantidade >= quantidade:
            medicamento.quantidade -= quantidade
            return self._repository.atualizar(medicamento)
        return False
    
    def gerar_relatorio(self) -> Dict:
        """Gera um relatório do estoque."""
        medicamentos = self._repository.obter_todos()
        total = len(medicamentos)
        vencidos = len(self._repository.obter_vencidos())
        quantidade_total = sum(med.quantidade for med in medicamentos)
        
        return {
            'total_medicamentos': total,
            'medicamentos_vencidos': vencidos,
            'quantidade_total': quantidade_total,
            'por_fabricante': self._agrupar_por_fabricante(medicamentos)
        }
    
    def _agrupar_por_fabricante(self, medicamentos: List[Medicamento]) -> Dict:
        """Agrupa medicamentos por fabricante."""
        grupos = {}
        for med in medicamentos:
            if med.fabricante not in grupos:
                grupos[med.fabricante] = []
            grupos[med.fabricante].append(med.to_dict())
        return grupos