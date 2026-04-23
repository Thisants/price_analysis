import pandas as pd
print("Pandas pronto para o combate! 🐼")
# 1. Carregar a planilha (O "banco de dados")
# Troque 'cotacoes.xlsx' pelo nome exato do seu arquivo
df = pd.read_excel("cotacoes.xlsx")

# 2. Mostrar o conteúdo para conferir
print("Aqui está o seu banco de dados:")
print(df.info())

preco = df["Preco"]

print("--- Apenas os Preços ---")
print(preco)

nome_primeira_Empresas = df["Empresas"].iloc[0]
print(f"A primeira empresa na lista é: {nome_primeira_Empresas}")