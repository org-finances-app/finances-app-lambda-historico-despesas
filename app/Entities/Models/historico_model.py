from decimal import Decimal
from .base_table_model import TableModel


class HistoricoDespesaModel(TableModel):
    userId: str
    despesaId: str
    dataPagamento: str
    valor: Decimal
    descricao: str
    categoriaPagamento: str
    tipoPagamento: str
