import PySimpleGUI as sg
import requests

def tela_inicial():
    sg.theme('DarkBlue4')

    cep = [
        [sg.Text('Informe um CEP:', font = 'arial 12', pad = (0,0))],
        [sg.Input(size = (20,0), font = 'arial 12', pad = (0,0), key = 'cep')]
    ]

    coluna1 = [
        [sg.Text('Endereço:', font = 'arial 12')],
        [sg.Text('Bairro:', font = 'arial 12')],
        [sg.Text('Cidade:', font = 'arial 12')],
        [sg.Text('Estado:', font = 'arial 12')],
    ]

    coluna2 = [
        [sg.Text('', font = 'arial 12', size = (40, 1), key = 'endereco')],
        [sg.Text('', font = 'arial 12', size = (40, 1), key = 'bairro')],
        [sg.Text('', font = 'arial 12', size = (40, 1), key = 'cidade')],
        [sg.Text('', font = 'arial 12', size = (40, 1), key = 'estado')],
    ]

    layout = [
        [sg.Column(cep, element_justification='c'), sg.Column(coluna1), sg.Column(coluna2)],
        [sg.Button('Buscar', font = 'arial 12', pad = (0,20)), sg.Button('Sair', font = 'arial 12', pad = (20,20))]
    ]

    return sg.Window('Consulta de CEP', layout=layout, finalize=True)

janela = tela_inicial()

while True:
    evento, valores = janela.read()
    if evento == sg.WINDOW_CLOSED or evento == 'Sair':
        break

    if evento == 'Buscar':
        cep = valores['cep']
        if len(cep) != 8:
            sg.popup('CEP inválido. Por favor, informe um CEP com 8 dígitos.', title = 'CEP inválido.')
        else:
            url = f'https://viacep.com.br/ws/{cep}/json/'
            try:
                response = requests.get(url)
                if response.status_code == 100:
                    endereco = response.json()
                    janela['endereco'].update(endereco['logradouro'])
                    janela['bairro'].update(endereco['bairro'])
                    janela['cidade'].update(endereco['localidade'])
                    janela['estado'].update(endereco['uf'])
                else:
                    sg.popup('Erro ao buscar informações do CEP. Por favor, tente novamente mais tarde.', title = 'Erro')
            except:
                sg.popup('Erro ao buscar informações do CEP. Por favor, verifique sua conexão com a internet.',title = 'Erro')
