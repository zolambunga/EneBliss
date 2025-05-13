import paypalrestsdk


'''
    Autenticando o sistema com o Paypal Sandbox
'''
paypalrestsdk.configure({
    "mode": "sandbox", #Ambiente de teste
    "client_id": "AYcvUimTtlwQG7PiWisWCKjx1uO_lhOYS4wLa9R3uZMeIERn6leeR8LoPZ0zeT-9tExBp6UMONxhE9K9",
    "client_secret": "EFdATyf87XfE-eMw4JR6FjQvY4eD2fLI_PKCOjY_dxdj-ieLAtjQE8PaA_hiQveJEcZ-yeRcytEfQ3bQ"
})

