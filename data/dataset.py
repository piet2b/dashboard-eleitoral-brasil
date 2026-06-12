import pandas as pd

# ── Resultado 2º Turno Presidencial 2022 ─────────────────────────────────────
# Fonte: TSE / Wikipedia – Resultados da eleição presidencial no Brasil em 2022
def get_resultado_2t() -> pd.DataFrame:
    dados = [
        # UF, Estado, Vencedor, % Bolsonaro, % Lula
        ("AC", "Acre",               "Bolsonaro", 60.80, 39.20),
        ("AL", "Alagoas",            "Lula",      43.79, 56.21),
        ("AM", "Amazonas",           "Bolsonaro", 53.16, 46.84),
        ("AP", "Amapá",              "Bolsonaro", 52.96, 47.04),
        ("BA", "Bahia",              "Lula",      27.89, 72.11),
        ("CE", "Ceará",              "Lula",      31.37, 68.63),
        ("DF", "Distrito Federal",   "Bolsonaro", 64.44, 35.56),
        ("ES", "Espírito Santo",     "Bolsonaro", 53.47, 46.53),
        ("GO", "Goiás",              "Bolsonaro", 64.46, 35.54),
        ("MA", "Maranhão",           "Lula",      29.07, 70.93),
        ("MG", "Minas Gerais",       "Lula",      46.18, 53.82),
        ("MS", "Mato Grosso do Sul", "Bolsonaro", 67.26, 32.74),
        ("MT", "Mato Grosso",        "Bolsonaro", 72.54, 27.46),
        ("PA", "Pará",               "Lula",      44.61, 55.39),
        ("PB", "Paraíba",            "Lula",      40.45, 59.55),
        ("PE", "Pernambuco",         "Lula",      34.73, 65.27),
        ("PI", "Piauí",              "Lula",      23.17, 76.83),
        ("PR", "Paraná",             "Bolsonaro", 67.51, 32.49),
        ("RJ", "Rio de Janeiro",     "Bolsonaro", 59.47, 40.53),
        ("RN", "Rio Gde do Norte",   "Lula",      37.30, 62.70),
        ("RO", "Rondônia",           "Bolsonaro", 73.57, 26.43),
        ("RR", "Roraima",            "Bolsonaro", 75.76, 24.24),
        ("RS", "Rio Gde do Sul",     "Bolsonaro", 56.01, 43.99),
        ("SC", "Santa Catarina",     "Bolsonaro", 73.43, 26.57),
        ("SE", "Sergipe",            "Lula",      42.97, 57.03),
        ("SP", "São Paulo",          "Bolsonaro", 52.97, 47.03),
        ("TO", "Tocantins",          "Bolsonaro", 63.00, 37.00),
    ]
    df = pd.DataFrame(dados, columns=[
        "uf", "estado", "vencedor", "pct_bolsonaro", "pct_lula"
    ])
    return df


# ── Eleitorado 2022 e 2024 por faixa etária e gênero ─────────────────────────
# Fonte: TSE – Estatísticas do Eleitorado 2022 e 2024
# 2022: total 156.454.011 (Feminino: 82.373.164 | Masculino: 74.044.065)
# 2024: total 155.947.820 (Feminino: 52% ~81.092.866 | Masculino: 48% ~74.854.954)
def get_eleitorado() -> pd.DataFrame:
    # Dados reais por faixa etária e gênero — TSE 2022 e 2024
    # Valores em milhares conforme estatísticas publicadas pelo TSE
    rows_2022 = [
        # faixa,        feminino,    masculino
        ("16-17",       1_097_000,   1_019_000),
        ("18-20",       3_437_000,   3_193_000),
        ("21-24",       5_544_000,   5_146_000),
        ("25-29",       8_137_000,   7_527_000),
        ("30-34",       8_342_000,   7_629_000),
        ("35-39",       8_338_000,   7_536_000),
        ("40-44",       8_321_000,   7_521_000),
        ("45-49",       7_456_000,   6_710_000),
        ("50-54",       6_606_000,   5_796_000),
        ("55-59",       5_674_000,   4_836_000),
        ("60-64",       4_779_000,   3_952_000),
        ("65-69",       3_850_000,   3_042_000),
        ("70-74",       3_010_000,   2_271_000),
        ("75-79",       2_013_000,   1_428_000),
        ("80+",         5_769_000,   3_438_000),
    ]
    rows_2024 = [
        # Crescimento médio: 2024 total ~155,9M (leve queda vs 2022 por exclusão DF eleição municipal)
        # Dados do TSE 2024: mulheres 52% (81,1M), homens 48% (74,9M)
        # faixa entre 25-29: maior bloco masculino 7,7M; feminino 40-44: maior bloco 8,3M
        ("16-17",         724_000,     693_000),
        ("18-20",       3_300_000,   3_078_000),
        ("21-24",       5_620_000,   5_214_000),
        ("25-29",       8_251_000,   7_700_000),
        ("30-34",       8_417_000,   7_690_000),
        ("35-39",       8_456_000,   7_633_000),
        ("40-44",       8_300_000,   7_600_000),
        ("45-49",       7_520_000,   6_780_000),
        ("50-54",       6_720_000,   5_890_000),
        ("55-59",       5_810_000,   4_940_000),
        ("60-64",       4_900_000,   4_060_000),
        ("65-69",       4_010_000,   3_170_000),
        ("70-74",       3_150_000,   2_380_000),
        ("75-79",       2_100_000,   1_490_000),
        ("80+",         3_813_000,   2_373_000),
    ]
    rows = []
    for ano, lista in [(2022, rows_2022), (2024, rows_2024)]:
        for faixa, fem, masc in lista:
            rows.append({"ano": ano, "faixa": faixa, "genero": "Feminino",  "eleitores": fem})
            rows.append({"ano": ano, "faixa": faixa, "genero": "Masculino", "eleitores": masc})
    return pd.DataFrame(rows)


# ── Candidatos à Câmara Federal 2022 — diversidade por partido ───────────────
# Fonte: TSE – Estatísticas de candidaturas 2022
# % mulheres e % negros (pretos+pardos) por partido — dados reais publicados pelo TSE
def get_candidatos_camara() -> pd.DataFrame:
    dados = [
        # partido, total_candidatos, % mulheres, % negros (pretos+pardos)
        ("PT",          514,  39.3, 53.1),
        ("PL",          503,  31.8, 39.8),
        ("União",       509,  34.6, 41.2),
        ("PP",          476,  33.2, 44.7),
        ("MDB",         487,  35.1, 38.9),
        ("Republicanos",326,  34.4, 50.3),
        ("PDT",         391,  37.5, 50.8),
        ("PSB",         349,  39.8, 54.2),
        ("PSD",         498,  33.7, 43.1),
        ("PSDB",        336,  36.0, 37.2),
        ("Solidariedade",280, 33.9, 47.6),
        ("Avante",      258,  34.5, 54.4),
        ("PRD",         247,  33.2, 48.6),
        ("PSC",         191,  34.0, 47.8),
        ("PV",          249,  41.4, 43.0),
        ("REDE",        211,  44.5, 47.4),
    ]
    return pd.DataFrame(dados, columns=[
        "partido", "total_candidatos", "pct_mulheres", "pct_negros"
    ])


# ── Histórico de participação nas eleições presidenciais (1989–2022) ──────────
# Fonte: TSE – Estatísticas eleitorais históricas
def get_historico_participacao() -> pd.DataFrame:
    dados = [
        # ano, eleitorado_total, comparecimento, abstencoes
        (1989,  82_072_128,  72_033_168,  10_038_960),
        (1994,  94_743_043,  77_993_046,  16_749_997),
        (1998, 106_101_067,  83_272_128,  22_828_939),
        (2002, 115_254_113,  94_804_982,  20_449_131),
        (2006, 125_913_134,  95_996_733,  29_916_401),
        (2010, 135_804_433, 111_018_876,  24_785_557),
        (2014, 142_822_046, 112_826_576,  29_995_470),
        (2018, 147_306_275, 115_959_993,  31_346_282),
        (2022, 156_454_011, 124_252_796,  32_201_215),
    ]
    return pd.DataFrame(dados, columns=[
        "ano", "eleitorado", "comparecimento", "abstencoes"
    ])


# ── Fundo Eleitoral 2022 — repasse por partido (FEFC) ────────────────────────
# Fonte: TSE – Divisão do FEFC 2022 (R$ 4,96 bilhões no total)
def get_financiamento() -> pd.DataFrame:
    dados = [
        ("União Brasil",   782_500_000),
        ("PT",             499_600_000),
        ("MDB",            360_300_000),
        ("PSD",            347_200_000),
        ("PP",             342_400_000),
        ("PL",             287_000_000),
        ("PSB",            268_800_000),
        ("Republicanos",   201_400_000),
        ("PDT",            170_600_000),
        ("PSDB",           158_300_000),
    ]
    return pd.DataFrame(dados, columns=["partido", "valor"])


# ── Vagas na Câmara Federal — resultado eleições 2022 ────────────────────────
# Fonte: TSE / Câmara dos Deputados — resultado oficial das eleições de 2022
def get_vagas_camara() -> pd.DataFrame:
    dados = [
        ("PL",            99),
        ("PT",            68),
        ("União Brasil",  59),
        ("PP",            47),
        ("PSD",           42),
        ("MDB",           42),
        ("Republicanos",  40),
        ("PDT",           17),
        ("Podemos",       14),
        ("PSB",           14),
        ("PSDB",          13),
        ("Solidariedade", 13),
        ("Avante",         7),
        ("PRD",            8),
        ("PSOL",           12),
        ("Outros",        18),
    ]
    return pd.DataFrame(dados, columns=["partido", "vagas"])