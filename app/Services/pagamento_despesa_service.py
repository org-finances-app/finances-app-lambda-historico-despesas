from Repositories.despesa_repository import DespesaRepository
from Repositories.base_table_repository import TableRepository
from datetime import date
from Utils.logger import LOGGER
from datetime import timedelta

from Entities.Tables.historico_despesa import HistoricoDespesaTable

from .helpers.despesa_handlers.despesa_handler import DespesaHandler
from .helpers.despesa_handlers.despesa_parcelada import DespesaParceladaHandler
from .helpers.despesa_handlers.despesa_a_vista import DespesaAVistaHandler
from .helpers.despesa_handlers.despesa_recorrente import DespesaRecorrenteHandler

import traceback


class DespesaHandlerFactory:
    handlers = {
        "À Vista": DespesaAVistaHandler,
        "Parcelado": DespesaParceladaHandler,
        "Recorrente": DespesaRecorrenteHandler,
    }

    @staticmethod
    def get_handler(despesa: dict, batch_writter: dict) -> DespesaHandler:
        handler = DespesaHandlerFactory.handlers[despesa.get("tipoPagamento")]
        return handler(despesa, batch_writter)


class PagamentoDespesaService:

    def __init__(self) -> None:
        self.despesa_repository = DespesaRepository()
        self.historico_repository = TableRepository(table=HistoricoDespesaTable())

    @property
    def date_to_process(self):
        return "2025-01-21"
        # Run the service for yesterday
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def _fetch_despesas_do_dia(self):
        return self.despesa_repository.get_by_data_pagamento_index(self.date_to_process)

    def run(self):
        LOGGER.append_keys(date_to_process=self.date_to_process)

        LOGGER.info(
            f"Iniciando serviço de atualização de despesas para a data {self.date_to_process}"
        )

        despesas = self._fetch_despesas_do_dia()

        LOGGER.info(f"Quantidade de despesas a serem atualizadas: {len(despesas)}")

        with self.historico_repository.dynamo_table.batch_writer() as historico_despesa_batch_writter:
            with self.despesa_repository.dynamo_table.batch_writer() as despesa_batch_writter:
                for despesa in despesas:
                    LOGGER.append_keys(
                        userId=despesa.get("userId"),
                        despesaId=despesa.get("despesaId"),
                    )

                    try:
                        LOGGER.info(f"Processando despesa {despesa.get('despesaId')}")

                        despesa_handler = DespesaHandlerFactory.get_handler(
                            despesa, despesa_batch_writter
                        )

                        LOGGER.info("Inserindo Histórico")

                        historico_despesa_batch_writter.put_item(
                            Item=despesa_handler.get_historico()
                        )

                        despesa_handler.handle_pagamento_pagamento()

                    except Exception as e:
                        LOGGER.error(
                            f"Erro ao processar despesa {despesa.get('despesaId')}"
                        )
                        LOGGER.error(e)
                        LOGGER.error(traceback.format_exc())

        LOGGER.info("Fim do serviço de atualização de despesas")
