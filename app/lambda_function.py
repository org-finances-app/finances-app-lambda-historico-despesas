from Services.pagamento_despesa_service import PagamentoDespesaService


def lambda_handler(event, context=None):
    PagamentoDespesaService().run()


if __name__ == "__main__":
    lambda_handler({})
