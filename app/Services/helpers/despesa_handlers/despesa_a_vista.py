from .despesa_handler import DespesaHandler


class DespesaAVistaHandler(DespesaHandler):
    def handle_processamento_despesa(self):
        self.delete_depesa()
