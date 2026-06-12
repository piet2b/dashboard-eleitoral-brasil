"""
app.py
------
Aplicação principal do Dashboard Eleitoral Brasil.

Executar localmente:
    python app.py

Deploy no Plotly Cloud:
    O objeto `server` é exposto para o gunicorn.
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Módulos internos
from data.dataset import (
    get_resultado_2t,
    get_eleitorado,
    get_candidatos_camara,
    get_historico_participacao,
    get_financiamento,
    get_vagas_camara,
)
from components.charts import (
    fig_mapa_resultado,
    fig_barras_estado,
    fig_piramide_etaria,
    fig_historico_participacao,
    fig_financiamento,
    fig_vagas_camara,
    fig_scatter_candidatos,
    fig_comparativo_eleitorado,
)
from components.layout_components import (
    make_kpi_card,
    make_section_header,
    make_chart_card,
    make_navbar,
    make_footer,
)
from utils.theme import VERDE_BRASIL, AMARELO_BRASIL, AZUL_BRASIL, CINZA_ESCURO

# ── Pré-carregamento dos dados ────────────────────────────────────────────────
df_resultado  = get_resultado_2t()
df_eleitorado = get_eleitorado()
df_candidatos = get_candidatos_camara()
df_historico  = get_historico_participacao()
df_financ     = get_financiamento()
df_vagas      = get_vagas_camara()

# ── Inicialização do app ──────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard interativo sobre eleições no Brasil"},
    ],
    title="Dashboard Eleitoral Brasil",
    suppress_callback_exceptions=True,
)

# Expõe o servidor Flask para o gunicorn (deploy no Plotly Cloud)
server = app.server

# ── KPIs ──────────────────────────────────────────────────────────────────────

total_eleitorado_22 = df_eleitorado[df_eleitorado["ano"] == 2022]["eleitores"].sum()
total_eleitorado_24 = df_eleitorado[df_eleitorado["ano"] == 2024]["eleitores"].sum()
estados_lula = (df_resultado["vencedor"] == "Lula").sum()
total_deputados = df_vagas["vagas"].sum()

kpis = dbc.Row([
    make_kpi_card(
        f"{total_eleitorado_22 / 1e6:.1f}M",
        "Eleitores em 2022",
        AZUL_BRASIL,
        "bi bi-people-fill",
    ),
    make_kpi_card(
        f"{total_eleitorado_24 / 1e6:.1f}M",
        "Eleitores em 2024",
        VERDE_BRASIL,
        "bi bi-person-check-fill",
    ),
    make_kpi_card(
        f"{estados_lula}/27",
        "Estados vencidos por Lula (2T 2022)",
        "#E74C3C",
        "bi bi-map-fill",
    ),
    make_kpi_card(
        str(total_deputados),
        "Deputados Federais (2022)",
        AMARELO_BRASIL if AMARELO_BRASIL != "#FFDF00" else "#D4A800",
        "bi bi-building-fill",
        col_width=3,
    ),
], className="mb-4 g-3")

# ── Layout principal ──────────────────────────────────────────────────────────

app.layout = html.Div([

    make_navbar(),

    dbc.Container([

        # ── Hero ──────────────────────────────────────────────────────────────
        html.Div([
            html.H1("Eleições no Brasil", style={
                "fontSize": "clamp(1.6rem, 4vw, 2.4rem)",
                "fontWeight": "800",
                "color": CINZA_ESCURO,
                "marginBottom": "6px",
            }),
            html.P(
                "Análise interativa dos dados eleitorais brasileiros — "
                "Presidenciais 2022 e Municipais 2024",
                className="text-muted",
                style={"fontSize": "1rem", "marginBottom": "0"},
            ),
        ], style={"padding": "28px 0 20px"}),

        # ── KPIs ──────────────────────────────────────────────────────────────
        kpis,

        html.Hr(style={"margin": "8px 0 28px", "borderColor": "#dee2e6"}),

        # ═════════════════════════════════════════════════════════════════════
        # SEÇÃO 1 – RESULTADO PRESIDENCIAL 2022
        # ═════════════════════════════════════════════════════════════════════
        html.Div(id="secao-resultado"),
        make_section_header(
            "Resultado Presidencial 2022",
            "Distribuição dos votos no 2º turno entre Lula (PT) e Bolsonaro (PL) por estado.",
            "🗺️",
        ),

        dbc.Row([
            # Mapa
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(
                            id="grafico-mapa",
                            figure=fig_mapa_resultado(df_resultado),
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ]),
                    className="shadow-sm",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
                md=7, className="mb-3",
            ),

            # Barras com filtro
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Label("Ordenar por:", className="fw-semibold small me-2"),
                            dbc.RadioItems(
                                id="radio-ordem",
                                options=[
                                    {"label": " Mais votos Lula",      "value": "lula"},
                                    {"label": " Mais votos Bolsonaro",  "value": "bolsonaro"},
                                ],
                                value="lula",
                                inline=True,
                                className="small",
                            ),
                        ], className="d-flex align-items-center flex-wrap gap-2 mb-2"),
                        html.Label("Número de estados:", className="fw-semibold small"),
                        dcc.Slider(
                            id="slider-top-n",
                            min=5, max=27, step=1, value=10,
                            marks={5: "5", 10: "10", 15: "15", 20: "20", 27: "27"},
                        ),
                        dcc.Graph(
                            id="grafico-barras-estado",
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ]),
                    className="shadow-sm h-100",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=5, className="mb-3"),
        ], className="mb-4"),

        html.Hr(style={"margin": "8px 0 28px", "borderColor": "#dee2e6"}),

        # ═════════════════════════════════════════════════════════════════════
        # SEÇÃO 2 – ELEITORADO
        # ═════════════════════════════════════════════════════════════════════
        html.Div(id="secao-eleitorado"),
        make_section_header(
            "Perfil do Eleitorado",
            "Distribuição por faixa etária e gênero nas eleições de 2022 e 2024.",
            "👥",
        ),

        dbc.Row([
            # Pirâmide etária
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Ano:", className="fw-semibold small"),
                        dbc.RadioItems(
                            id="radio-ano-piramide",
                            options=[
                                {"label": " 2022", "value": 2022},
                                {"label": " 2024", "value": 2024},
                            ],
                            value=2022, inline=True, className="small mb-2",
                        ),
                        dcc.Graph(
                            id="grafico-piramide",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "460px"},
                        ),
                    ]),
                    className="shadow-sm h-100",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=6, className="mb-3"),

            # Comparativo 2022 vs 2024
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Filtrar por gênero:", className="fw-semibold small"),
                        dbc.RadioItems(
                            id="radio-genero-comp",
                            options=[
                                {"label": " Todos",     "value": "Todos"},
                                {"label": " Feminino",  "value": "Feminino"},
                                {"label": " Masculino", "value": "Masculino"},
                            ],
                            value="Todos", inline=True, className="small mb-2",
                        ),
                        dcc.Graph(
                            id="grafico-comparativo-eleitorado",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "460px"},
                        ),
                    ]),
                    className="shadow-sm h-100",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=6, className="mb-3"),
        ], className="mb-4"),

        html.Hr(style={"margin": "8px 0 28px", "borderColor": "#dee2e6"}),

        # ═════════════════════════════════════════════════════════════════════
        # SEÇÃO 3 – CÂMARA FEDERAL
        # ═════════════════════════════════════════════════════════════════════
        html.Div(id="secao-camara"),
        make_section_header(
            "Câmara Federal 2022",
            "Composição, diversidade de candidatos e financiamento de campanha.",
            "🏛️",
        ),

        dbc.Row([
            # Rosca – vagas
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Mostrar top N partidos:", className="fw-semibold small"),
                        dcc.Slider(
                            id="slider-vagas-top",
                            min=5, max=16, step=1, value=10,
                            marks={5: "5", 8: "8", 12: "12", 16: "16"},
                        ),
                        dcc.Graph(
                            id="grafico-vagas",
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "420px"},
                        ),
                    ]),
                    className="shadow-sm h-100",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=5, className="mb-3"),

            # Scatter – diversidade
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.P(
                            "Cada bolha é um partido. O tamanho representa o total de candidatos.",
                            className="text-muted small mb-2",
                        ),
                        dcc.Graph(
                            id="grafico-scatter-candidatos",
                            figure=fig_scatter_candidatos(df_candidatos),
                            config={"displayModeBar": False, "responsive": True},
                            style={"height": "430px"},
                        ),
                    ]),
                    className="shadow-sm h-100",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=7, className="mb-3"),
        ], className="mb-4"),

        # Financiamento (linha completa)
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Número de partidos:", className="fw-semibold small"),
                        dcc.Slider(
                            id="slider-financ-top",
                            min=3, max=10, step=1, value=8,
                            marks={3: "3", 5: "5", 7: "7", 10: "10"},
                        ),
                        dcc.Graph(
                            id="grafico-financiamento",
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ]),
                    className="shadow-sm",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=12, className="mb-3"),
        ], className="mb-4"),

        html.Hr(style={"margin": "8px 0 28px", "borderColor": "#dee2e6"}),

        # ═════════════════════════════════════════════════════════════════════
        # SEÇÃO 4 – HISTÓRICO
        # ═════════════════════════════════════════════════════════════════════
        html.Div(id="secao-historico"),
        make_section_header(
            "Série Histórica — 1989 a 2022",
            "Evolução do eleitorado, comparecimento e abstenções nas eleições presidenciais.",
            "📈",
        ),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Label("Exibir séries:", className="fw-semibold small"),
                        dbc.Checklist(
                            id="check-historico",
                            options=[
                                {"label": " Eleitorado total",  "value": "eleitorado"},
                                {"label": " Comparecimento",    "value": "comparecimento"},
                                {"label": " Abstenções",        "value": "abstencoes"},
                            ],
                            value=["comparecimento", "abstencoes"],
                            inline=True, className="small mb-2",
                        ),
                        dcc.Graph(
                            id="grafico-historico",
                            config={"displayModeBar": False, "responsive": True},
                        ),
                    ]),
                    className="shadow-sm",
                    style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
                ),
            ], md=12, className="mb-3"),
        ], className="mb-4"),

    ], fluid=True, style={"maxWidth": "1400px"}),

    make_footer(),

], style={"backgroundColor": "#F7F8FC", "fontFamily": "Inter, sans-serif"})


# ═════════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ═════════════════════════════════════════════════════════════════════════════

# ── Callback 1: Barras por estado (filtro: ordenação + top-n) ────────────────
@app.callback(
    Output("grafico-barras-estado", "figure"),
    Input("slider-top-n", "value"),
    Input("radio-ordem",  "value"),
)
def atualizar_barras_estado(top_n: int, ordem: str):
    """
    Atualiza o gráfico de barras horizontais com resultado por estado.
    Inputs: número de estados a exibir e critério de ordenação.
    """
    return fig_barras_estado(df_resultado, top_n=top_n, ordem=ordem)


# ── Callback 2: Pirâmide etária (filtro: ano) ────────────────────────────────
@app.callback(
    Output("grafico-piramide", "figure"),
    Input("radio-ano-piramide", "value"),
)
def atualizar_piramide(ano: int):
    """
    Atualiza a pirâmide etária ao trocar o ano (2022 ou 2024).
    """
    return fig_piramide_etaria(df_eleitorado, ano=ano)


# ── Callback 3: Comparativo eleitorado (filtro: gênero) ─────────────────────
@app.callback(
    Output("grafico-comparativo-eleitorado", "figure"),
    Input("radio-genero-comp", "value"),
)
def atualizar_comparativo_eleitorado(genero: str):
    """
    Atualiza as barras comparativas 2022 vs 2024 com filtro por gênero.
    """
    return fig_comparativo_eleitorado(df_eleitorado, genero=genero)


# ── Callback 4: Rosca – composição da Câmara (filtro: top N) ─────────────────
@app.callback(
    Output("grafico-vagas", "figure"),
    Input("slider-vagas-top", "value"),
)
def atualizar_vagas(top_n: int):
    """
    Atualiza o gráfico de rosca com a composição da Câmara.
    """
    return fig_vagas_camara(df_vagas, top_n=top_n)


# ── Callback 5: Financiamento (filtro: top N partidos) ───────────────────────
@app.callback(
    Output("grafico-financiamento", "figure"),
    Input("slider-financ-top", "value"),
)
def atualizar_financiamento(top_n: int):
    """
    Atualiza as barras de financiamento com o número de partidos selecionado.
    """
    return fig_financiamento(df_financ, top_n=top_n)


# ── Callback 6: Linha histórica (filtro: séries visíveis) ────────────────────
@app.callback(
    Output("grafico-historico", "figure"),
    Input("check-historico", "value"),
)
def atualizar_historico(series: list):
    """
    Mostra/oculta séries no gráfico histórico conforme checklist.
    Evita figura vazia se nenhuma série estiver selecionada.
    """
    if not series:
        series = ["comparecimento"]
    return fig_historico_participacao(df_historico, mostrar=series)


# ── Callback 7: Navbar collapse (responsividade mobile) ─────────────────────
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_navbar(n):
    return True  # Toggle simples — o Bootstrap cuida do estado


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
