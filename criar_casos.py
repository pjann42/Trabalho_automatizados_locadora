import random

def criar_casos_aleatorios(num_caixas,):

    num_pilhas = 3
    
    caixas = [chr(i) for i in range(97, 97 + num_caixas)] 
    
    caixas_iniciais = caixas[:]
    random.shuffle(caixas_iniciais)

    caixas_finais = caixas[:]
    random.shuffle(caixas_finais)
    
    pilhas_inicial = [[] for _ in range(num_pilhas)]
    pilhas_final = [[] for _ in range(num_pilhas)]
    
    for caixa in caixas_iniciais:
        pilhas_inicial[random.randint(0, num_pilhas - 1)].append(caixa)
    
    for caixa in caixas_finais:
        pilhas_final[random.randint(0, num_pilhas - 1)].append(caixa)
    
    return pilhas_inicial, pilhas_final

#pilhas_inicial, pilhas_final = criar_casos_aleatorios(7)
#print("Pilhas Iniciais:", pilhas_inicial)
#print("Pilhas Finais:", pilhas_final)
