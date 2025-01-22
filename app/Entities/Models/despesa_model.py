from decimal import Decimal
from .base_table_model import TableModel
from enum import Enum


class TipoPagamentoEnum(str, Enum):
    recorrente = "Recorrente"
    parcelado = "Parcelado"
    a_vista = "À Vista"


class FrequenciaEnum(str, Enum):
    mensal = "Mensal"
    semanal = "Semanal"
    outro = "Outro"


class DespesaModel(TableModel):
    userId: str
    despesaId: str
    tipoPagamento: TipoPagamentoEnum
    categoriaPagamento: str
    ultimoPagamento: str
    descricao: str
    valor: Decimal
    dataProximoPagamento: str = ""
