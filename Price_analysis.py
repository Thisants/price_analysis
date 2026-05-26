"""
price_analysis.py — Analisa a cotação e diz quem é mais barata.
Uso: python puro
"""
import sys
import pandas as pd
from pathlib import Path

ARQUIVO = sys.argv[1] if len(sys.argv) > 1 else "cotacoes.xlsx"

def main():
    if not Path(ARQUIVO).exists():
        print(f"Arquivo '{ARQUIVO}' não encontrado.")
        sys.exit(1)

    df = pd.read_excel(ARQUIVO, header=1, skiprows=[2])
    
    colunas_base = ["Num", "Descricao", "Qtd", "Empresa1", "Empresa2", "Empresa3", "MenorPreco"]
    df.columns = colunas_base + list(df.columns[len(colunas_base):])
    
    df = df[df["Descricao"].notna() & (df["Descricao"].astype(str).str.strip() != "")]
    
    empresas = {"Empresa 1": "Empresa1", "Empresa 2": "Empresa2", "Empresa 3": "Empresa3"}
    col_empresas = list(empresas.values())

    for col in col_empresas + ["Qtd"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    df = df.dropna(subset=["Qtd"])
    df = df[df["Qtd"] > 0].reset_index(drop=True)

    if df.empty:
        print("Nenhum dado válido para analisar.")
        return

    # VETORIZAÇÃO: O Pandas acha os menores valores instantaneamente aqui
    df["M_Preco"] = df[col_empresas].min(axis=1)
    df["M_Coluna"] = df[col_empresas].idxmin(axis=1)
    
    rev_empresas = {v: k for k, v in empresas.items()}
    df["M_Vencedor"] = df["M_Coluna"].map(rev_empresas)

    print("\n" + "="*65)
    print("  ANÁLISE DE PREÇOS — Quem é mais barata?")
    print("="*65)
    print(f"\n  {'#':<5} {'Item':<35} {'Mais barata':<14} {'Preço':>10}")
    print("  " + "-"*60)

    for _, row in df.dropna(subset=["M_Preco"]).iterrows():
        num = int(row['Num']) if pd.notna(row['Num']) else "-"
        print(f"  {num:<5} {str(row['Descricao'])[:33]:<35} "
              f"{row['M_Vencedor']:<14} R$ {row['M_Preco']:>8.2f}")

    # Total geral
    totais = {}
    for nome, col in empresas.items():
        total = (df[col] * df["Qtd"]).sum()
        if total > 0:
            totais[nome] = round(total, 2)

    if len(totais) < 2:
        print(f"\n  ! É necessário ter pelo menos 2 empresas com preços para comparar.\n")
        return

    mais_barata = min(totais, key=totais.get)
    mais_cara   = max(totais, key=totais.get)
    economia    = totais[mais_cara] - totais[mais_barata]
    variacao    = (economia / totais[mais_barata]) * 100 if totais[mais_barata] > 0 else 0

    print("\n" + "="*65)
    print("  TOTAL GERAL POR EMPRESA")
    print("="*65)
    for nome, total in sorted(totais.items(), key=lambda x: x[1]):
        tag = " MAIS BARATA" if nome == mais_barata else ""
        print(f"  {nome:<14}  R$ {total:>10,.2f}{tag}")

    print(f"\n Mais barata : {mais_barata}  →  R$ {totais[mais_barata]:,.2f}")
    print(f"   Mais cara   : {mais_cara}  →  R$ {totais[mais_cara]:,.2f}")
    print(f"   Economia    : R$ {economia:,.2f}  ({variacao:.1f}% de diferença)\n")

if __name__ == "__main__":
    main()
