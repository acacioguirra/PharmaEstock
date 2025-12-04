from models.base_entity import BaseEntity
from datetime import datetime
from typing import Optional

class Medicamento(BaseEntity):
    """Classe que representa um medicamento com validações específicas."""
    
    def __init__(self, id: int, nome: str, lote: str, validade: str, 
                 fabricante: str, quantidade: int = 0):
        super().__init__(id)
        self.nome = nome
        self.lote = lote
        self.validade = validade
        self.fabricante = fabricante
        self._quantidade = quantidade
        self._validar_dados()
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, value: str):
        if not value or not value.strip():
            raise ValueError("Nome do medicamento não pode ser vazio")
        if len(value) > 100:
            raise ValueError("Nome do medicamento muito longo")
        self._nome = value.strip()
    
    @property
    def lote(self) -> str:
        return self._lote
    
    @lote.setter
    def lote(self, value: str):
        if not value or not value.strip():
            raise ValueError("Lote não pode ser vazio")
        self._lote = value.strip()
    
    @property
    def validade(self) -> str:
        return self._validade
    
    @validade.setter
    def validade(self, value: str):
        self._validar_data_validade(value)
        self._validade = value
    
    @property
    def quantidade(self) -> int:
        return self._quantidade
    
    @quantidade.setter
    def quantidade(self, value: int):
        if value < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self._quantidade = value
    
    def _validar_dados(self):
        """Valida todos os dados do medicamento."""
        if not self.fabricante or not self.fabricante.strip():
            raise ValueError("Fabricante não pode ser vazio")
    
    def _validar_data_validade(self, data_str: str):
        """Valida o formato da data de validade."""
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            if data <= datetime.now():
                raise ValueError("Data de validade deve ser futura")
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Formato de data inválido. Use DD/MM/AAAA")
            raise e
    
    def esta_vencido(self) -> bool:
        """Verifica se o medicamento está vencido."""
        try:
            data_validade = datetime.strptime(self._validade, "%d/%m/%Y")
            return data_validade <= datetime.now()
        except ValueError:
            return False
    
    def to_dict(self) -> dict:
        """Implementação do método abstrato."""
        return {
            'id': self.id,
            'nome': self.nome,
            'lote': self.lote,
            'validade': self.validade,
            'fabricante': self.fabricante,
            'quantidade': self.quantidade,
            'vencido': self.esta_vencido()
        }
    
    def __str__(self) -> str:
        """Implementação do método abstrato."""
        status = " (VENCIDO)" if self.esta_vencido() else ""
        return (f"ID: {self.id:03d} | Nome: {self.nome:20.20s} | "
                f"Lote: {self.lote:10.10s} | Validade: {self.validade} | "
                f"Qtd: {self.quantidade:3d}{status}")