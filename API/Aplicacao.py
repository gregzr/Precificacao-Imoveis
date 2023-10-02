# Construir a API em FLASK

from flask import Flask, request
from datetime import datetime
import joblib
import sqlite3

# Instanciar aplicativo
Aplicativo = Flask(__name__)

# Carregar o modelo
modelo = joblib.load('Modelo_floresta_Aleatorio_v100.pkl')

# url será onde está rodando + /API_preditivo
# na url será passado um parametro. Ele é extraído pelo GET, vai pra função e retorna no final

@Aplicativo.route('/API_preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01(area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):

    # Capturar informações de entrada
    data_inicio = datetime.now()

    # Recebendo os inputs da API

    Lista = [float(area), float(rooms), float(bathroom), float(parking_spaces), 
             float(floor), float(animal), float(furniture), float(hoa), float(property_tax)]

    # Com os inputs ele vai tentar fazer a previsão no modelo
    # Se conseguir trará a previsão
    # Se não conseguir trará que deu erro

    try:

        previsao = modelo.predict( [Lista] ) # a lista precisa ser um vetor []
        
        # Inserir valor da previsão
        Lista.append(str(previsao))

        # Transformando a lista de str
        input = ''
        for Valor in Lista:
            input = input + ';' + str(Valor)

        # Capturar informações de saída
        data_fim = datetime.now()

        # Calcular o tempo
        Processamento = data_fim - data_inicio

        #Criar conexão com o banco de dados
        conexao_banco = sqlite3.connect('C:/Users/grego/Desktop/CURSOS/Udemy/DataViking/ML/banco_dados_API.db')
        Cursor = conexao_banco.cursor()


        #Query
        query_inserindo_dados = f'''
            INSERT INTO Log_API ( Inputs, Inicio, Fim, Processamento)
            VALUES( '{input}', '{data_inicio}', '{data_fim}', '{Processamento}' )

        '''
        #Executar Query
        Cursor.execute(query_inserindo_dados)
        conexao_banco.commit()

        #Fechando conexão com o banco
        Cursor.close()

        return{'Valor_Aluguel' : str(previsao)} # o retorno precisa ser uma srt
    
    except:
        
        return {'Aviso' : 'Deu algum erro!'}

if __name__ == '__main__':
    Aplicativo.run (debug = True)


