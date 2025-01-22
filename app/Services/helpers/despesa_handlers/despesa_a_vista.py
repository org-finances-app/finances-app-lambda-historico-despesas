from .despesa_handler import DespesaHandler


class DespesaAVistaHandler(DespesaHandler):
    def handle_pagamento_pagamento(self):
        self.delete_depesa()
