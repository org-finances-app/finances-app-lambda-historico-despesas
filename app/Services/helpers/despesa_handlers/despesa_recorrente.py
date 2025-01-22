from .despesa_handler import DespesaHandler


class DespesaRecorrenteHandler(DespesaHandler):
    def handle_pagamento_pagamento(self):
        self.despesa["dataProximoPagamento"] = self._get_proximo_pagamento()

        self.update_depesa()
