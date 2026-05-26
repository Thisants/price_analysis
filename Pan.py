"""
Biblioteca Pandas
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
    
    # Evita quebrar se houverem colunas extras no fim do Excel
    colunas_base = ["Num", "Descricao", "Qtd", "Empresa1", "Empresa2", "Empresa3", "MenorPreco"]
    df.columns = colunas_base + list(df.columns[len(colunas_base):])

    df = df[df["Descricao"].notna() & (df["Descricao"].astype(str).str.strip() != "")]
    for col in ["Empresa1", "Empresa2", "Empresa3", "Qtd"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Qtd"])
    df = df[df["Qtd"] > 0].reset_index(drop=True)

    print("\n" + "="*65)
    print("  COTAÇÃO DE COMPRAS — pan.py")
    print("="*65)
    print(f"  Arquivo : {ARQUIVO}")
    print(f"  Itens   : {len(df)}")
    print("="*65)
    print(f"\n  {'#':<5} {'Descrição':<35} {'Qtd':>5}  {'Emp.1':>10}  {'Emp.2':>10}  {'Emp.3':>10}")
    print("  " + "-"*60)

    # FUNÇÃO DE FORMATAÇÃO: Definida fora do loop para poupar memória
    def fmt(v): 
        return f"R${v:>8.2f}" if pd.notna(v) else "       —  "

    for _, row in df.iterrows():
        num  = int(row["Num"]) if pd.notna(row["Num"]) else "-"
        desc = str(row["Descricao"])[:33]
        qtd  = int(row["Qtd"])
        print(f"  {num:<5} {desc:<35} {qtd:>5}  {fmt(row['Empresa1'])}  {fmt(row['Empresa2'])}  {fmt(row['Empresa3'])}")

    print(f"\n  Execute price_analysis.py para ver quem é mais barata.\n")

if __name__ == "__main__":
    main()
