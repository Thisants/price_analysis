empresa_x = 630.00
empresa_y = 430.59
empresa_z = 500.00

empresas = {
    "Empresa X": empresa_x,
    "Empresa Y": empresa_y,
    "Empresa Z": empresa_z
}

mais_barata = min(empresas, key=empresas.get)
mais_cara = max(empresas, key=empresas.get)

preco_barato = empresas[mais_barata]
preco_caro = empresas[mais_cara]

variacao = ((preco_caro - preco_barato) / preco_barato) * 100

print(f"A empresa mais barata é: {mais_barata} (R$ {preco_barato:.2f})")
print(f"A empresa mais cara é: {mais_cara} (R$ {preco_caro:.2f})")
print(f"A {mais_cara} é {variacao:.2f}% mais cara que a {mais_barata}.")