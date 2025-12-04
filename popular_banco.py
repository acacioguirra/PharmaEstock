import database as db
from datetime import datetime

# Lista de 10 medicamentos fictícios
# Inclui: 1 Vencido, 1 Perto de vencer, Vários fabricantes
lista_medicamentos = [
    {
        "nome": "Dipirona Monoidratada 500mg",
        "lote": "A1020",
        "validade": "10/12/2026",
        "fabricante": "Medley",
        "quantidade": 200
    },
    {
        "nome": "Paracetamol 750mg",
        "lote": "B3040",
        "validade": "01/05/2027",
        "fabricante": "EMS",
        "quantidade": 150
    },
    {
        "nome": "Amoxicilina 500mg",
        "lote": "C5060",
        "validade": "20/11/2025",
        "fabricante": "Neo Química",
        "quantidade": 45
    },
    {
        "nome": "Ibuprofeno 600mg",
        "lote": "D7080",
        "validade": "15/01/2024",  # DATA NO PASSADO (PARA TESTAR VENCIMENTO)
        "fabricante": "Teuto",
        "quantidade": 12
    },
    {
        "nome": "Dorflex Comprimidos",
        "lote": "E9010",
        "validade": "30/08/2026",
        "fabricante": "Sanofi",
        "quantidade": 500
    },
    {
        "nome": "Omeprazol 20mg",
        "lote": "F1112",
        "validade": "12/12/2025",
        "fabricante": "Eurofarma",
        "quantidade": 80
    },
    {
        "nome": "Losartana Potássica 50mg",
        "lote": "G1314",
        "validade": "25/03/2026",
        "fabricante": "Sandoz",
        "quantidade": 100
    },
    {
        "nome": "Vitamina C 1g Efervescente",
        "lote": "H1516",
        "validade": "05/02/2025", # PERTO DE VENCER (dependendo da data atual)
        "fabricante": "Cimed",
        "quantidade": 30
    },
    {
        "nome": "Azitromicina 500mg",
        "lote": "I1718",
        "validade": "18/09/2027",
        "fabricante": "Pfizer",
        "quantidade": 60
    },
    {
        "nome": "Clonazepam 0.5mg",
        "lote": "J1920",
        "validade": "22/07/2026",
        "fabricante": "Medley",
        "quantidade": 90
    }
]

def popular():
    print("🔄 Iniciando população do banco de dados...")
    
    # Garante que o banco existe
    db.init_db()
    
    for med in lista_medicamentos:
        try:
            db.cadastrar_medicamento(med)
            print(f"✅ Cadastrado: {med['nome']}")
        except Exception as e:
            print(f"❌ Erro ao cadastrar {med['nome']}: {e}")
            
    print("\n🎉 Concluído! 10 medicamentos inseridos.")

if __name__ == "__main__":
    popular()