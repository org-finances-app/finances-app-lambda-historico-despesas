from .despesa_handler import DespesaHandler


class DespesaParceladaHandler(DespesaHandler):
    def handle_processamento_despesa(self):
        qtde_parcelas = self.despesa.get("quantidadeParcelas")
        parcela_atual = int(self.despesa.get("parcelaAtual"))
        parcela_atual += 1

        if parcela_atual == qtde_parcelas:
            self.delete_depesa()
            return

        self.despesa["parcelaAtual"] = parcela_atual
        self.despesa["dataProximoPagamento"] = self._get_proximo_pagamento()

        self.update_depesa()
