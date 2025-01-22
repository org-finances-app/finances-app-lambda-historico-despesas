from Utils.despesa_futura_utils import gera_data_proxima_despesa
from dataclasses import dataclass
from abc import ABC, abstractmethod
from Utils.logger import LOGGER
from Entities.Models.historico_model import HistoricoDespesaModel


@dataclass
class DespesaHandler(ABC):
    despesa: dict
    batch_writter: dict

    def _get_proximo_pagamento(self) -> str:
        return gera_data_proxima_despesa(
            self.despesa.get("dataProximoPagamento"),
            self.despesa.get("frequencia"),
            self.despesa.get("detalhesFrequencia"),
        ).strftime("%Y-%m-%d")

    def delete_depesa(self):
        LOGGER.info("Deletando despesa")

        self.batch_writter.delete_item(
            Key={
                "userId": self.despesa.get("userId"),
                "despesaId": self.despesa.get("despesaId"),
            }
        )

    def update_depesa(self):
        LOGGER.info("Atualizando despesa")
        self.batch_writter.put_item(Item=self.despesa)

    def get_historico(self) -> dict:
        return HistoricoDespesaModel(
            userId=self.despesa.get("userId"),
            despesaId=self.despesa.get("despesaId"),
            dataPagamento=self.despesa.get("dataProximoPagamento"),
            valor=self.despesa.get("valor"),
            descricao=self.despesa.get("descricao"),
            categoriaPagamento=self.despesa.get("categoriaPagamento"),
            tipoPagamento=self.despesa.get("tipoPagamento"),
        ).model_dump()

    @abstractmethod
    def handle_pagamento_pagamento(self):
        pass
