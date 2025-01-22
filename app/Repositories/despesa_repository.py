from Repositories.base_table_repository import TableRepository
from Entities.Tables.despesa_table import DespesaTable
from dataclasses import dataclass
from boto3.dynamodb.conditions import Key


@dataclass(init=True)
class DespesaRepository(TableRepository):

    def __init__(self):
        self.table = DespesaTable()
        super()

    def get_by_data_pagamento_index(self, data: str):
        filters = Key("dataProximoPagamento").eq(data)

        query = self.dynamo_table.query(
            IndexName="dataProximoPagamentoIndex", KeyConditionExpression=filters
        )

        return query["Items"]
