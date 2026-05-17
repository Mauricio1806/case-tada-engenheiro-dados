import csv
import random
from datetime import datetime, timedelta, date
from pathlib import Path

random.seed(42)
OUT = Path('./data')
OUT.mkdir(parents=True, exist_ok=True)

PRODUTOS = [
    ('SKU001', 'Heineken Long Neck 330ml',          'Lager',         'Heineken',    6.50, 5.0),
    ('SKU002', 'Brahma Duplo Malte 350ml',           'Lager',         'Brahma',      4.20, 4.7),
    ('SKU003', 'Skol Pilsen Lata 350ml',             'Lager',         'Skol',        3.80, 4.7),
    ('SKU004', 'Stella Artois Long Neck 330ml',      'Lager',         'Stella',      7.90, 5.0),
    ('SKU005', 'Corona Extra Long Neck 330ml',       'Lager',         'Corona',      8.50, 4.5),
    ('SKU006', 'Original 600ml',                     'Lager',         'Antarctica',  9.90, 5.0),
    ('SKU007', 'Eisenbahn Pilsen 600ml',             'Pilsen',        'Eisenbahn',  12.90, 4.8),
    ('SKU008', 'Colorado Appia 600ml',               'Honey Ale',     'Colorado',   18.90, 5.4),
    ('SKU009', 'Colorado Indica 600ml',              'IPA',           'Colorado',   19.90, 7.0),
    ('SKU010', 'Goose Island IPA 355ml',             'IPA',           'Goose Island',14.90, 5.9),
    ('SKU011', 'Patagonia Amber Lager 740ml',        'Amber Lager',   'Patagonia',  16.50, 4.5),
    ('SKU012', 'Leffe Blonde 330ml',                 'Belgian Blond', 'Leffe',      11.90, 6.6),
    ('SKU013', 'Hoegaarden 330ml',                   'Witbier',       'Hoegaarden', 10.90, 4.9),
    ('SKU014', "Beck's Long Neck 330ml",             'Pilsen',        "Beck's",      7.50, 5.0),
    ('SKU015', 'Budweiser Long Neck 330ml',          'Lager',         'Budweiser',   6.90, 5.0),
]

LOJAS = [
    ('LJ01', 'Centro - Sao Paulo',     'Sao Paulo',      'SP', 'Sudeste'),
    ('LJ02', 'Vila Mariana',           'Sao Paulo',      'SP', 'Sudeste'),
    ('LJ03', 'Pinheiros',              'Sao Paulo',      'SP', 'Sudeste'),
    ('LJ04', 'Copacabana',             'Rio de Janeiro', 'RJ', 'Sudeste'),
    ('LJ05', 'Barra da Tijuca',        'Rio de Janeiro', 'RJ', 'Sudeste'),
    ('LJ06', 'Savassi',                'Belo Horizonte', 'MG', 'Sudeste'),
    ('LJ07', 'Moinhos de Vento',       'Porto Alegre',   'RS', 'Sul'),
    ('LJ08', 'Batel',                  'Curitiba',       'PR', 'Sul'),
    ('LJ09', 'Asa Sul',                'Brasilia',       'DF', 'Centro-Oeste'),
    ('LJ10', 'Boa Viagem',             'Recife',         'PE', 'Nordeste'),
    ('LJ11', 'Barra',                  'Salvador',       'BA', 'Nordeste'),
    ('LJ12', 'Meireles',               'Fortaleza',      'CE', 'Nordeste'),
]

CLIENTES = []
for i in range(1, 2001):
    CLIENTES.append({
        'cliente_id': f'CLI{i:05d}',
        'nome': f'Cliente {i:04d}',
        'email': f'cliente{i:04d}@email.exemplo',
        'cidade': random.choice(LOJAS)[2],
        'data_cadastro': (date(2023, 1, 1) + timedelta(days=random.randint(0, 700))).isoformat(),
    })

PEDIDOS, ITENS, PAGAMENTOS = [], [], []
DATA_INICIAL = date(2025, 9, 1)
DATA_FINAL = date(2025, 10, 31)
pedido_seq = 0
item_seq = 0

dia = DATA_INICIAL
while dia <= DATA_FINAL:
    fator_dia = {0: 0.6, 1: 0.7, 2: 0.8, 3: 0.9, 4: 1.4, 5: 1.6, 6: 1.1}[dia.weekday()]
    qtd_pedidos_hoje = int(80 * fator_dia)

    for _ in range(qtd_pedidos_hoje):
        pedido_seq += 1
        cliente = random.choice(CLIENTES)
        loja = random.choice(LOJAS)
        hora = random.randint(10, 23)
        minuto = random.randint(0, 59)
        segundo = random.randint(0, 59)
        ts_pedido = datetime.combine(dia, datetime.min.time()).replace(
            hour=hora, minute=minuto, second=segundo)

        r = random.random()
        status = 'PAGO' if r < 0.90 else ('CANCELADO' if r < 0.95 else 'PENDENTE')

        qtd_itens = random.choices([1, 2, 3, 4, 5], weights=[20, 35, 25, 15, 5])[0]
        total_pedido = 0.0
        itens_do_pedido = []
        for _ in range(qtd_itens):
            item_seq += 1
            prod = random.choice(PRODUTOS)
            qtd = random.choices([1, 2, 3, 6, 12], weights=[35, 25, 20, 15, 5])[0]
            preco = prod[4] * random.uniform(0.95, 1.05)
            subtotal = round(preco * qtd, 2)
            total_pedido += subtotal
            itens_do_pedido.append({
                'item_id': f'IT{item_seq:08d}',
                'pedido_id': f'PED{pedido_seq:08d}',
                'sku': prod[0],
                'quantidade': qtd,
                'preco_unitario': round(preco, 2),
                'subtotal': subtotal,
            })

        taxa = round(random.uniform(5.0, 12.0), 2)
        total_pedido_final = round(total_pedido + taxa, 2)

        PEDIDOS.append({
            'pedido_id': f'PED{pedido_seq:08d}',
            'cliente_id': cliente['cliente_id'],
            'loja_id': loja[0],
            'criado_em': ts_pedido.isoformat(),
            'status': status,
            'subtotal': round(total_pedido, 2),
            'taxa_entrega': taxa,
            'total': total_pedido_final,
            'canal': random.choice(['APP_IOS', 'APP_ANDROID', 'WEB']),
        })
        ITENS.extend(itens_do_pedido)

        if status != 'CANCELADO':
            metodo = random.choices(
                ['PIX', 'CARTAO_CREDITO', 'CARTAO_DEBITO', 'DINHEIRO'],
                weights=[45, 35, 15, 5])[0]
            ts_pag = ts_pedido + timedelta(seconds=random.randint(30, 600))
            PAGAMENTOS.append({
                'pagamento_id': f'PAG{pedido_seq:08d}',
                'pedido_id': f'PED{pedido_seq:08d}',
                'metodo': metodo,
                'valor': total_pedido_final,
                'processado_em': ts_pag.isoformat(),
                'status': 'APROVADO' if status == 'PAGO' else 'PENDENTE',
            })
    dia += timedelta(days=1)

# Problemas de qualidade DE PROPOSITO pra Silver pegar
duplicados = random.sample(PEDIDOS, 50)
PEDIDOS.extend(duplicados)
for it in random.sample(ITENS, 20):
    it['subtotal'] = 0.0
for p in random.sample(PEDIDOS, 10):
    p['criado_em'] = p['criado_em'] + 'Z'

def write_csv(path, rows, fieldnames):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(OUT / 'pedidos.csv', PEDIDOS,
          ['pedido_id', 'cliente_id', 'loja_id', 'criado_em', 'status',
           'subtotal', 'taxa_entrega', 'total', 'canal'])
write_csv(OUT / 'pedido_itens.csv', ITENS,
          ['item_id', 'pedido_id', 'sku', 'quantidade', 'preco_unitario', 'subtotal'])
write_csv(OUT / 'pagamentos.csv', PAGAMENTOS,
          ['pagamento_id', 'pedido_id', 'metodo', 'valor', 'processado_em', 'status'])

with open(OUT / 'produtos.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['sku', 'nome', 'categoria', 'marca', 'preco_base', 'abv'])
    for p in PRODUTOS:
        w.writerow(p)

with open(OUT / 'lojas.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['loja_id', 'nome', 'cidade', 'estado', 'regiao'])
    for l in LOJAS:
        w.writerow(l)

with open(OUT / 'clientes.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['cliente_id', 'nome', 'email', 'cidade', 'data_cadastro'])
    w.writeheader()
    w.writerows(CLIENTES)

print(f'OK - gerados {len(PEDIDOS):,} pedidos, {len(ITENS):,} itens, {len(PAGAMENTOS):,} pagamentos')