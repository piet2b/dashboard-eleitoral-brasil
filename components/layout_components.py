from dash import html
import dash_bootstrap_components as dbc
from utils.theme import VERDE_BRASIL, AZUL_BRASIL, AMARELO_BRASIL, CINZA_ESCURO


def make_kpi_card(
    valor: str,
    titulo: str,
    cor: str,
    icone: str,
    col_width: int = 3,
) -> dbc.Col:
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"{icone} fs-2", style={"color": cor, "opacity": 0.85}),
                    html.Div([
                        html.P(titulo, className="text-muted mb-0", style={"fontSize": "0.78rem", "fontWeight": "500"}),
                        html.H4(valor, className="mb-0 fw-bold", style={"color": CINZA_ESCURO, "fontSize": "clamp(1.1rem,2vw,1.6rem)"}),
                    ], className="ms-3"),
                ], className="d-flex align-items-center"),
                html.Div(style={
                    "height": "3px",
                    "background": f"linear-gradient(90deg, {cor}, transparent)",
                    "borderRadius": "2px",
                    "marginTop": "12px",
                }),
            ])
        ],
        className="shadow-sm h-100",
        style={"borderRadius": "12px", "border": f"1px solid #e9ecef", "borderTop": f"3px solid {cor}"}),
        md=col_width, className="mb-2",
    )


def make_section_header(titulo: str, subtitulo: str, emoji: str = "") -> html.Div:
    return html.Div([
        html.H5(
            [html.Span(emoji + " ", style={"marginRight": "6px"}), titulo],
            style={"fontWeight": "700", "color": CINZA_ESCURO, "marginBottom": "2px"},
        ),
        html.P(subtitulo, className="text-muted", style={"fontSize": "0.88rem", "marginBottom": "16px"}),
    ])


def make_chart_card(children, class_name: str = "") -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(children),
        className=f"shadow-sm {class_name}",
        style={"borderRadius": "12px", "border": "1px solid #e9ecef"},
    )


def make_navbar() -> dbc.Navbar:
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand([
                html.Span("🗳️", style={"marginRight": "8px"}),
                "Dashboard Eleitoral Brasil",
            ], style={"fontWeight": "700", "fontSize": "1.1rem", "color": "white"}),

            dbc.NavbarToggler(id="navbar-toggler"),

            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Resultado 2022",  href="#secao-resultado",  className="text-white-50 small")),
                    dbc.NavItem(dbc.NavLink("Eleitorado",      href="#secao-eleitorado", className="text-white-50 small")),
                    dbc.NavItem(dbc.NavLink("Câmara",          href="#secao-camara",     className="text-white-50 small")),
                    dbc.NavItem(dbc.NavLink("Histórico",       href="#secao-historico",  className="text-white-50 small")),
                ], navbar=True),
                id="navbar-collapse",
                navbar=True,
                is_open=False,
            ),
        ], fluid=True),
        color=AZUL_BRASIL,
        dark=True,
        sticky="top",
        style={"boxShadow": "0 2px 8px rgba(0,0,0,.18)"},
    )


def make_footer() -> html.Footer:
    return html.Footer(
        dbc.Container(
            html.P(
                "Dashboard Eleitoral Brasil · Dados: TSE · Desenvolvido com Python Dash",
                className="text-center text-muted small py-3 mb-0",
            ),
            fluid=True,
        ),
        style={"borderTop": "1px solid #dee2e6", "marginTop": "40px", "backgroundColor": "#f8f9fa"},
    )