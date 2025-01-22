from .base_table import Table
from ..Models.despesa_model import DespesaModel, TableModel


class HistoricoDespesaTable(Table):
    name: str = "HistoricoDespesa"
    partition_key: str = "userId"
    sort_key: str = "despesaId"
    model: TableModel = DespesaModel
