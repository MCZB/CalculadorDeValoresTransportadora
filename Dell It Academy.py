import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Função para ler os dados das distâncias entre cidades a partir de um arquivo CSV
def ler_dados_csv():
    with open('DnitDistancias.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        cidades = next(reader)
        distancias = [list(map(float, row)) for row in reader]
        return cidades, distancias

# Função para calcular o custo do transporte com base na distância, tipo de caminhão e quantidade de caminhões
def calcular_custo(distancia, tipo_caminhao, quantidade_caminhoes):
    precos_por_km = {
        'Caminhão de pequeno porte': 4.87,
        'Caminhão de médio porte': 11.92,
        'Caminhão de grande porte': 27.44
    }
    return distancia * precos_por_km[tipo_caminhao] * quantidade_caminhoes

# Função para determinar a quantidade de caminhões necessários para transportar o peso total dos itens
def escolher_caminhao(peso_total):
    limites_carga = {
        'Caminhão de grande porte': 10000,
        'Caminhão de médio porte': 4000,
        'Caminhão de pequeno porte': 1000
    }

    caminhoes_necessarios = {
        'Caminhão de pequeno porte': 0,
        'Caminhão de médio porte': 0,
        'Caminhão de grande porte': 0
    }

    for tipo_caminhao, limite_carga in limites_carga.items():
        while peso_total >= limite_carga:
            caminhoes_necessarios[tipo_caminhao] += 1
            peso_total -= limite_carga

    if peso_total > 0:
        caminhoes_necessarios['Caminhão de pequeno porte'] += 1

    return caminhoes_necessarios

def limpar_resultado():
    resultado_var.set("")

# Função para adicionar uma cidade à lista de cidades na interface gráfica
def adicionar_cidade():
    cidade = entry_cidade.get()
    if cidade not in cidades:
        messagebox.showerror("Erro", "Cidade não encontrada.")
        return
    if cidade in lista_cidades.get(0, tk.END):
        messagebox.showerror("Erro", "A cidade já está na lista.")
        return
    lista_cidades.insert(tk.END, cidade)

# Função para remover uma cidade selecionada da lista de cidades na interface gráfica
def remover_cidade():
    indice_selecionado = lista_cidades.curselection()
    if indice_selecionado:
        lista_cidades.delete(indice_selecionado)

# Função para adicionar uma cidade de parada na interface gráfica
def adicionar_cidade_parada():
    entry_cidade_parada = ttk.Combobox(frame, values=cidades, state="readonly")
    entry_cidade_parada.grid(row=9, column=len(entry_cidades_parada) + 1)
    entry_cidades_parada.append(entry_cidade_parada)

    quantidades_descarregar = []
    entry_quantidades_descarregar_cidade = []
    for i, item in enumerate(itens):
        quantidade_descarregar_var = tk.StringVar()
        quantidade_descarregar_var.set("0")
        quantidades_descarregar.append(quantidade_descarregar_var)

        entry_quantidade_descarregar = tk.Entry(frame, textvariable=quantidade_descarregar_var, width=5)
        entry_quantidade_descarregar.grid(row=10 + i, column=len(entry_cidades_parada))
        entry_quantidades_descarregar_cidade.append(entry_quantidade_descarregar)

    quantidades_descarregar_var.append(quantidades_descarregar)
    entry_quantidades_descarregar.append(entry_quantidades_descarregar_cidade)

def get_entry_quantidades_descarregar(column):
    entry_quantidades_descarregar = []
    for i in range(len(itens)):
        entry_quantidade_descarregar = frame.grid_slaves(row=10 + i, column=column)
        if entry_quantidade_descarregar:
            entry_quantidades_descarregar.append(entry_quantidade_descarregar[0])
    return entry_quantidades_descarregar 

# Função para remover uma cidade de parada na interface gráfica
# Função para remover uma cidade de parada na interface gráfica
def remover_cidade_parada():
    if entry_cidades_parada:
        column = entry_cidades_parada[-1].grid_info()['column']
        entry_cidades_parada[-1].grid_forget()
        entry_cidades_parada.pop()

        entry_quantidades_descarregar = get_entry_quantidades_descarregar(column)
        for entry_quantidade_descarregar in entry_quantidades_descarregar:
            entry_quantidade_descarregar.grid_forget()

        quantidades_descarregar_var.pop()
        

# Função para calcular a distância total, o custo total, o peso total dos itens e os caminhões necessários para o transporte
def calcular_distancia_e_custo():
    rota = lista_cidades.get(0, tk.END)
    if len(rota) < 2:
        messagebox.showerror("Erro", "Selecione pelo menos duas cidades.")
        return

    distancia_total = 0
    for i in range(len(rota) - 1):
        indice_cidade1 = cidades.index(rota[i])
        indice_cidade2 = cidades.index(rota[i + 1])
        distancia = distancias[indice_cidade1][indice_cidade2]
        distancia_total += distancia

    itens = {
        'Celular': 0.5,
        'Geladeira': 60.0,
        'Freezer': 100.0,
        'Cadeira': 5.0,
        'Luminária': 0.8,
        'Lavadora de roupa': 120.0
    }
    limites_carga = {
        'Caminhão de pequeno porte': 1000,
        'Caminhão de médio porte': 4000,
        'Caminhão de grande porte': 10000
    }
    peso_total = 0
    for item, quantidade in zip(itens_var, quantidades_var):
        peso_total += itens[item.get()] * float(quantidade.get())

    caminhoes_necessarios = escolher_caminhao(peso_total)

    custo = 0
    for tipo_caminhao, quantidade_caminhoes in caminhoes_necessarios.items():
        custo += calcular_custo(distancia_total, tipo_caminhao, quantidade_caminhoes)

    itens_descarregar = []
    for cidade_parada, quantidades in zip(entry_cidades_parada, quantidades_descarregar_var):
        cidade = cidade_parada.get()
        if cidade and cidade not in rota:
            messagebox.showerror("Erro", "A cidade de parada não está na rota.")
            return

        itens_descarregar_cidade = []
        for item, quantidade in zip(itens_var, quantidades):
            itens_descarregar_cidade.append((item.get(), float(quantidade.get())))

        itens_descarregar.append((cidade, itens_descarregar_cidade))

    transporte = {
        'distancia_total': distancia_total,
        'custo_total': custo,
        'caminhoes_necessarios': caminhoes_necessarios,
        'itens_transportados': [(item.get(), float(quantidade.get())) for item, quantidade in zip(itens_var, quantidades_var)],
        'itens_descarregar': itens_descarregar
    }

    # Verificar se a quantidade de itens para descarregar é maior do que o transporte está levando
    for cidade, itens_descarregar_cidade in itens_descarregar:
        for item_descarregar, quantidade_descarregar in itens_descarregar_cidade:
            for item_transportado, quantidade_transportado in transporte['itens_transportados']:
                if item_descarregar == item_transportado and quantidade_descarregar > quantidade_transportado:
                    messagebox.showerror("Erro", f"A quantidade de {item_descarregar} para descarregar em {cidade} é maior do que o transporte está levando.")
                    return

    transportes.append(transporte)

    cidades_parada = [cidade.get() for cidade in entry_cidades_parada]
    cidades_parada_str = ', '.join(cidades_parada)

    itens_descarregar_str = ', '.join(f"{cidade}: {', '.join(f'{item}: {qtd}' for item, qtd in itens_descarregar_cidade)}" for cidade, itens_descarregar_cidade in itens_descarregar)
    caminhoes_necessarios_str = ', '.join(f"{tipo}: {qtd}" for tipo, qtd in caminhoes_necessarios.items())

    resultado_var.set(f"Distância: {distancia_total:.2f} km\nCusto: R$ {custo:.2f}\nPeso total: {peso_total:.2f} kg\nCidades de parada: {cidades_parada_str}\nItens a descarregar: {itens_descarregar_str}\nCaminhões necessários: {caminhoes_necessarios_str}")

# Função para gerar um relatório com informações detalhadas sobre o transporte
def gerar_relatorio():
    relatorio = ""

    for i, transporte in enumerate(transportes):
        relatorio += f"Transporte {i + 1}:\n"
        relatorio += f"Custo total: R$ {transporte['custo_total']:.2f}\n"
        relatorio += f"Custo médio por km: R$ {transporte['custo_total'] / transporte['distancia_total']:.2f}\n"
        relatorio += f"Caminhões necessários:\n"
        for tipo_caminhao, quantidade_caminhoes in transporte['caminhoes_necessarios'].items():
            relatorio += f"  {tipo_caminhao}: {quantidade_caminhoes}\n"
        relatorio += f"Total de itens transportados: {sum(qtd for _, qtd in transporte['itens_transportados'])}\n"

        relatorio += f"Itens carregados:\n"
        for item, quantidade in transporte['itens_transportados']:
            if quantidade > 0:
                relatorio += f"  {item}: {quantidade}\n"

        relatorio += f"Total de itens descarregados nas cidades de parada:\n"
        for cidade, itens_descarregar_cidade in transporte['itens_descarregar']:
            relatorio += f"  {cidade}: {sum(qtd for _, qtd in itens_descarregar_cidade)}\n"
            relatorio += f"  Itens descarregados em {cidade}:\n"
            for item, quantidade in itens_descarregar_cidade:
                if quantidade > 0:
                    relatorio += f"    {item}: {quantidade}\n"

        # Calcular o custo médio por produto
        custo_medio_por_produto = sum(transporte['custo_total'] for transporte in transportes) / sum(sum(qtd for _, qtd in transporte['itens_transportados']) for transporte in transportes)
        relatorio += f"Custo médio por produto: R$ {custo_medio_por_produto:.2f}\n"

        # Calcular o custo total por trecho
        custo_total_por_trecho = transporte['custo_total'] / (len(transporte['itens_transportados']) - 1)
        relatorio += f"Custo total por trecho: R$ {custo_total_por_trecho:.2f}\n"

        # Calcular o custo total para cada modalidade de transporte
        relatorio += f"Custo total para cada modalidade de transporte:\n"
        for tipo_caminhao, custo in {tipo_caminhao: calcular_custo(transporte['distancia_total'], tipo_caminhao, quantidade_caminhoes) for tipo_caminhao, quantidade_caminhoes in transporte['caminhoes_necessarios'].items()}.items():
            relatorio += f"  {tipo_caminhao}: R$ {custo:.2f}\n"

        # Calcular o número total de veículos deslocados
        total_veiculos_deslocados = sum(transporte['caminhoes_necessarios'].values())
        relatorio += f"Número total de veículos deslocados: {total_veiculos_deslocados}\n"

        relatorio += "\n"

    janela_relatorio = tk.Toplevel(app)
    janela_relatorio.title("Relatório")
    label_relatorio = tk.Label(janela_relatorio, text=relatorio, justify=tk.LEFT)
    label_relatorio.pack(padx=10, pady=10)

# Função para calcular a distância entre duas cidades selecionadas e o custo com base no tipo de caminhão

def calcular_distancia_entre_cidades():
    cidade1 = cidade1_combobox.get()
    cidade2 = cidade2_combobox.get()
    tipo_caminhao = tipo_caminhao_combobox.get()

    if cidade1 not in cidades or cidade2 not in cidades:
        messagebox.showerror("Erro", "Selecione duas cidades válidas.")
        return

    if not tipo_caminhao:
        messagebox.showerror("Erro", "Selecione um tipo de caminhão.")
        return

    indice_cidade1 = cidades.index(cidade1)
    indice_cidade2 = cidades.index(cidade2)
    distancia = distancias[indice_cidade1][indice_cidade2]

    custo = calcular_custo(distancia, tipo_caminhao, 1)

    resultado_cidades_var.set(f"Distância entre {cidade1} e {cidade2}: {distancia:.2f} km\nCusto com {tipo_caminhao}: R$ {custo:.2f}")

# Lendo os dados das distâncias entre cidades a partir do arquivo CSV
cidades, distancias = ler_dados_csv()
transportes = []

# Criando a interface gráfica
app = tk.Tk()
app.title("Calculadora de Distância e Custo")
app.geometry("900x700")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

# Adicione os widgets necessários para selecionar duas cidades e o tipo de caminhão
label_cidade1 = tk.Label(frame, text="Cidade 1:")
label_cidade1.grid(row=19, column=0, sticky="e")
cidade1_combobox = ttk.Combobox(frame, values=cidades, state="readonly")
cidade1_combobox.grid(row=19, column=1)


label_cidade2 = tk.Label(frame, text="Cidade 2:")
label_cidade2.grid(row=20, column=0, sticky="e")
cidade2_combobox = ttk.Combobox(frame, values=cidades, state="readonly")
cidade2_combobox.grid(row=20, column=1)

label_tipo_caminhao = tk.Label(frame, text="Tipo de caminhão:")
label_tipo_caminhao.grid(row=21, column=0, sticky="e")
tipo_caminhao_combobox = ttk.Combobox(frame, values=['Caminhão de pequeno porte', 'Caminhão de médio porte', 'Caminhão de grande porte'], state="readonly")
tipo_caminhao_combobox.grid(row=21, column=1)

# Adicione o botão para calcular a distância entre as cidades selecionadas e o custo com base no tipo de caminhão
botao_calcular_cidades = tk.Button(frame, text="Calcular distância entre cidades", command=calcular_distancia_entre_cidades)
botao_calcular_cidades.grid(row=22, columnspan=4)

# Adicione um label para exibir o resultado do cálculo
resultado_cidades_var = tk.StringVar()
label_resultado_cidades = tk.Label(frame, textvariable=resultado_cidades_var)
label_resultado_cidades.grid(row=23, columnspan=4)

label_cidade = tk.Label(frame, text="Cidade:")
label_cidade.grid(row=0, column=0, sticky="e")
entry_cidade = ttk.Combobox(frame, values=cidades, state="readonly")
entry_cidade.grid(row=0, column=1)

botao_adicionar = tk.Button(frame, text="Adicionar cidade", command=adicionar_cidade)
botao_adicionar.grid(row=0, column=2)

botao_remover = tk.Button(frame, text="Remover cidade", command=remover_cidade)
botao_remover.grid(row=0, column=3)

lista_cidades = tk.Listbox(frame, height=5, selectmode=tk.SINGLE)
lista_cidades.grid(row=1, column=0, columnspan=3, pady=10, rowspan=2)

itens = ['Celular', 'Geladeira', 'Freezer', 'Cadeira', 'Luminária', 'Lavadora de roupa']
itens_var = []
quantidades_var = []
for i, item in enumerate(itens):
    item_var = tk.StringVar()
    item_var.set(item)
    itens_var.append(item_var)

    quantidade_var = tk.StringVar()
    quantidade_var.set("0")
    quantidades_var.append(quantidade_var)

    label_item = tk.Label(frame, text=item + ":")
    label_item.grid(row=3 + i, column=0, sticky="e")
    entry_quantidade = tk.Entry(frame, textvariable=quantidade_var, width=5)
    entry_quantidade.grid(row=3 + i, column=1)

label_cidade_parada = tk.Label(frame, text="Cidade de parada:")
label_cidade_parada.grid(row=9, column=0, sticky="e")

entry_cidades_parada = []
quantidades_descarregar_var = []
entry_quantidades_descarregar = []

botao_adicionar_parada = tk.Button(frame, text="Adicionar parada", command=adicionar_cidade_parada)
botao_adicionar_parada.grid(row=8, column=6)

botao_remover_parada = tk.Button(frame, text="Remover parada", command=remover_cidade_parada)
botao_remover_parada.grid(row=8, column=7)

for i, item in enumerate(itens):
    label_item_descarregar = tk.Label(frame, text=item + ":")
    label_item_descarregar.grid(row=10 + i, column=0, sticky="e")

botao_calcular = tk.Button(frame, text="Calcular", command=calcular_distancia_e_custo)
botao_calcular.grid(row=16, columnspan=1, column=1)

resultado_var = tk.StringVar()
label_resultado = tk.Label(frame, textvariable=resultado_var)
label_resultado.grid(row=17, columnspan=4)

botao_relatorio = tk.Button(frame, text="Gerar relatório", command=gerar_relatorio)
botao_relatorio.grid(row=16, column=3, columnspan=3)

frame_calculo_cidades = tk.Frame(frame)
frame_calculo_cidades.grid(row=18, column=0, columnspan=4, pady=10)

botao_limpar = tk.Button(frame, text="Limpar resultado", command=limpar_resultado)
botao_limpar.grid(row=16, columnspan=4, column=1)

# Adicione um título acima da seção de cálculo de distância e preço entre duas cidades
titulo_calculo_cidades = tk.Label(frame, text="Calcular distância e preço entre duas cidades", font=("Arial", 12, "bold"))
titulo_calculo_cidades.grid(row=18, column=0, columnspan=4, pady=10)

# Atualize as posições dos widgets existentes
label_cidade1.grid(row=19, column=0, sticky="e")
cidade1_combobox.grid(row=19, column=1, sticky="w")
label_cidade2.grid(row=20, column=0, sticky="e")
cidade2_combobox.grid(row=20, column=1, sticky="w")
label_tipo_caminhao.grid(row=21, column=0, sticky="e")
tipo_caminhao_combobox.grid(row=21, column=1, sticky="w")
botao_calcular_cidades.grid(row=22, column=1, sticky="w")
label_resultado_cidades.grid(row=23, column=0, columnspan=4)

app.mainloop()