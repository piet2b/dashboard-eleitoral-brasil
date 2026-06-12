import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.theme import (
    VERDE_BRASIL, AMARELO_BRASIL, AZUL_BRASIL,
    CINZA_ESCURO, LULA_COLOR, BOLSONARO_COLOR,
)

_FONT   = "Inter, sans-serif"
_BG     = "rgba(0,0,0,0)"
_PAPER  = "rgba(0,0,0,0)"
_GRID   = "#ebebeb"


def _base_layout(**kwargs):
    return dict(
        paper_bgcolor=_PAPER,
        plot_bgcolor=_BG,
        font=dict(family=_FONT, color=CINZA_ESCURO, size=12),
        **kwargs,
    )

# ── 1. Mapa resultado 2T 2022 ─────────────────────────────────────────────────
def fig_mapa_resultado(df: pd.DataFrame) -> go.Figure:
    df = df.copy()
    df["cor_num"] = df["vencedor"].map({"Lula": 1, "Bolsonaro": 0})
    df["texto"] = df.apply(
        lambda r: (
            f"<b>{r['estado']}</b><br>"
            f"Lula: {r['pct_lula']:.2f}%<br>"
            f"Bolsonaro: {r['pct_bolsonaro']:.2f}%<br>"
            f"Vencedor: {r['vencedor']}"
        ),
        axis=1,
    )
    fig = go.Figure(go.Choropleth(
        locations=df["uf"],
        z=df["cor_num"],
        locationmode="geojson-id",
        geojson=(
            "https://raw.githubusercontent.com/codeforamerica/"
            "click_that_hood/master/public/data/brazil-states.geojson"
        ),
        featureidkey="properties.sigla",
        colorscale=[[0, BOLSONARO_COLOR], [1, LULA_COLOR]],
        showscale=False,
        hovertext=df["texto"],
        hoverinfo="text",
        marker_line_color="white",
        marker_line_width=1.0,
    ))
    fig.update_geos(fitbounds="locations", visible=False, bgcolor=_BG)
    fig.update_layout(
        **_base_layout(
            title=dict(
                text="Resultado por Estado — 2º Turno 2022",
                font=dict(size=13, color=CINZA_ESCURO),
            ),
            height=400,
            geo=dict(bgcolor=_BG),
        )
    )
    return fig


# ── 2. Barras horizontais — resultado por estado ──────────────────────────────
def fig_barras_estado(df: pd.DataFrame, top_n: int = 10, ordem: str = "lula") -> go.Figure:
    col_sort = "pct_lula" if ordem == "lula" else "pct_bolsonaro"
    # Ordena decrescente, pega top_n, depois inverte para o gráfico horizontal
    dff = df.nlargest(top_n, col_sort).sort_values(col_sort, ascending=True)

    altura = max(320, top_n * 28)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=dff["estado"], x=dff["pct_lula"],
        name="Lula", orientation="h",
        marker_color=LULA_COLOR,
        hovertemplate="%{y}: %{x:.2f}%<extra>Lula</extra>",
    ))
    fig.add_trace(go.Bar(
        y=dff["estado"], x=dff["pct_bolsonaro"],
        name="Bolsonaro", orientation="h",
        marker_color=BOLSONARO_COLOR,
        hovertemplate="%{y}: %{x:.2f}%<extra>Bolsonaro</extra>",
    ))
    fig.update_layout(
        **_base_layout(
            title=dict(
                text=f"Top {top_n} estados — % de votos válidos",
                font=dict(size=13),
            ),
            barmode="group",
            xaxis=dict(
                title="% de votos válidos",
                ticksuffix="%",
                showgrid=True, gridcolor=_GRID,
                range=[0, 85],
            ),
            yaxis=dict(showgrid=False, automargin=True),
            height=altura,
            margin=dict(l=10, r=20, t=44, b=40),
        )
    )
    return fig


# ── 3. Pirâmide etária ────────────────────────────────────────────────────────
def fig_piramide_etaria(df: pd.DataFrame, ano: int = 2022) -> go.Figure:
    dff  = df[df["ano"] == ano].copy()
    faixas = [
        "16-17","18-20","21-24","25-29","30-34","35-39","40-44",
        "45-49","50-54","55-59","60-64","65-69","70-74","75-79","80+",
    ]
    fem  = dff[dff["genero"] == "Feminino" ].set_index("faixa")["eleitores"].reindex(faixas).fillna(0)
    mas  = dff[dff["genero"] == "Masculino"].set_index("faixa")["eleitores"].reindex(faixas).fillna(0)
    max_val = max(fem.max(), mas.max()) * 1.12

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=faixas,
        x=[-v for v in fem],
        name="Feminino",
        orientation="h",
        marker_color="#E91E8C",
        customdata=fem.values,
        hovertemplate="%{customdata:,.0f}<extra>Feminino</extra>",
    ))
    fig.add_trace(go.Bar(
        y=faixas,
        x=mas.values,
        name="Masculino",
        orientation="h",
        marker_color=AZUL_BRASIL,
        hovertemplate="%{x:,.0f}<extra>Masculino</extra>",
    ))

    # Gera ticks simétricos legíveis
    step   = 2_000_000
    n_steps = int(max_val // step) + 1
    tick_vals = (
        [-i * step for i in range(n_steps, 0, -1)]
        + [0]
        + [ i * step for i in range(1, n_steps + 1)]
    )
    tick_text = [f"{abs(v)//1_000_000:.0f}M" for v in tick_vals]

    fig.update_layout(
        **_base_layout(
            title=dict(
                text=f"Pirâmide Etária do Eleitorado — {ano}",
                font=dict(size=13),
            ),
            barmode="overlay",
            bargap=0.12,
            xaxis=dict(
                range=[-max_val, max_val],
                tickvals=tick_vals,
                ticktext=tick_text,
                showgrid=True, gridcolor=_GRID,
                zeroline=True, zerolinecolor="#bbb", zerolinewidth=1,
            ),
            yaxis=dict(showgrid=False, automargin=True, tickfont=dict(size=11)),
            height=460,
            margin=dict(l=10, r=10, t=44, b=30),
        )
    )
    return fig


# ── 4. Histórico participação ─────────────────────────────────────────────────
def fig_historico_participacao(df: pd.DataFrame, mostrar: list = None) -> go.Figure:
    if not mostrar:
        mostrar = ["comparecimento"]

    cores = {
        "eleitorado":     AZUL_BRASIL,
        "comparecimento": VERDE_BRASIL,
        "abstencoes":     "#E74C3C",
    }
    nomes = {
        "eleitorado":     "Eleitorado total",
        "comparecimento": "Comparecimento",
        "abstencoes":     "Abstenções",
    }

    fig = go.Figure()
    for serie in mostrar:
        fig.add_trace(go.Scatter(
            x=df["ano"], y=df[serie],
            mode="lines+markers",
            name=nomes[serie],
            line=dict(color=cores[serie], width=2.5),
            marker=dict(size=7),
            hovertemplate="%{y:,.0f}<extra>" + nomes[serie] + "</extra>",
        ))
    fig.update_layout(
        **_base_layout(
            title=dict(
                text="Participação nas Eleições Presidenciais (1989–2022)",
                font=dict(size=13),
            ),
            xaxis=dict(
                title="Ano", showgrid=True, gridcolor=_GRID,
                dtick=4, tickangle=0,
            ),
            yaxis=dict(
                title="Eleitores",
                showgrid=True, gridcolor=_GRID,
                tickformat=",.0f",
                automargin=True,
            ),
            height=400,
            margin=dict(l=10, r=10, t=44, b=40),
        )
    )
    return fig


# ── 5. Financiamento de campanha — FEFC 2022 ──────────────────────────────────
def fig_financiamento(df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    dff = df.nlargest(top_n, "valor").sort_values("valor", ascending=True)

    fig = go.Figure(go.Bar(
        y=dff["partido"],
        x=dff["valor"],
        orientation="h",
        marker=dict(
            color=dff["valor"],
            colorscale=[[0, "#AED6F1"], [1, AZUL_BRASIL]],
            showscale=False,
        ),
        hovertemplate="R$ %{x:,.0f}<extra>%{y}</extra>",
        text=[f"R$ {v/1e6:.0f}M" for v in dff["valor"]],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig.update_layout(
        **_base_layout(
            title=dict(
                text="Fundo Eleitoral (FEFC) por Partido — 2022",
                font=dict(size=13),
            ),
            xaxis=dict(
                title="Valor (R$)",
                showgrid=True, gridcolor=_GRID,
                tickformat=",.0s",
                range=[0, dff["valor"].max() * 1.22],
            ),
            yaxis=dict(showgrid=False, automargin=True),
            height=max(300, top_n * 46),
            margin=dict(l=10, r=80, t=44, b=40),
        )
    )
    return fig


# ── 6. Rosca — vagas Câmara Federal ──────────────────────────────────────────
def fig_vagas_camara(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    dff    = df.nlargest(top_n, "vagas")
    outros = df[~df["partido"].isin(dff["partido"])]["vagas"].sum()
    if outros > 0:
        dff = pd.concat(
            [dff, pd.DataFrame([{"partido": "Outros", "vagas": outros}])],
            ignore_index=True,
        )

    cores = [
        "#1f77b4","#d62728","#ff7f0e","#2ca02c","#9467bd",
        "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf",
        "#aec7e8","#ffbb78",
    ]

    fig = go.Figure(go.Pie(
        labels=dff["partido"],
        values=dff["vagas"],
        hole=0.50,
        marker=dict(colors=cores[:len(dff)], line=dict(color="white", width=1.5)),
        hovertemplate="%{label}: %{value} vagas (%{percent})<extra></extra>",
        # Mostra só % dentro do gráfico; nome vai para a legenda
        textinfo="percent",
        textfont=dict(size=11),
        insidetextorientation="radial",
    ))
    fig.update_layout(
        **_base_layout(
            title=dict(
                text="Composição da Câmara Federal — 2022",
                font=dict(size=13),
            ),
            height=420,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle", y=0.5,
                xanchor="left",   x=1.02,
                font=dict(size=11),
            ),
            margin=dict(l=10, r=130, t=44, b=10),
        )
    )
    return fig


# ── 7. Scatter — diversidade de candidatos ───────────────────────────────────
def fig_scatter_candidatos(df: pd.DataFrame) -> go.Figure:
    tamanhos = (df["total_candidatos"] / df["total_candidatos"].max()) * 55 + 10

    fig = go.Figure(go.Scatter(
        x=df["pct_mulheres"],
        y=df["pct_negros"],
        mode="markers+text",
        text=df["partido"],
        textposition="top center",
        textfont=dict(size=10),
        marker=dict(
            size=tamanhos,
            color=df["total_candidatos"],
            colorscale=[[0, "#AED6F1"], [1, AZUL_BRASIL]],
            showscale=True,
            colorbar=dict(title=dict(text="Candidatos", side="right"), thickness=12, len=0.6),
            opacity=0.85,
            line=dict(width=1.5, color="white"),
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "% Mulheres: %{x:.1f}%<br>"
            "% Negros/Pardos: %{y:.1f}%<extra></extra>"
        ),
    ))
    fig.update_layout(
        **_base_layout(
            title=dict(
                text="Diversidade de Candidatos à Câmara — 2022",
                font=dict(size=13),
            ),
            xaxis=dict(
                title="% Candidatas Mulheres",
                showgrid=True, gridcolor=_GRID,
                ticksuffix="%",
                range=[28, 48],
            ),
            yaxis=dict(
                title="% Candidatos Negros/Pardos",
                showgrid=True, gridcolor=_GRID,
                ticksuffix="%",
                range=[34, 60],
            ),
            height=430,
            showlegend=False,
            margin=dict(l=10, r=80, t=44, b=50),
        )
    )
    return fig


# ── 8. Comparativo eleitorado 2022 vs 2024 ────────────────────────────────────
def fig_comparativo_eleitorado(df: pd.DataFrame, genero: str = "Todos") -> go.Figure:
    faixas = [
        "16-17","18-20","21-24","25-29","30-34","35-39","40-44",
        "45-49","50-54","55-59","60-64","65-69","70-74","75-79","80+",
    ]
    dff = df if genero == "Todos" else df[df["genero"] == genero]
    agg = dff.groupby(["ano","faixa"])["eleitores"].sum().reset_index()

    df22 = agg[agg["ano"] == 2022].set_index("faixa")["eleitores"].reindex(faixas).fillna(0)
    df24 = agg[agg["ano"] == 2024].set_index("faixa")["eleitores"].reindex(faixas).fillna(0)

    titulo = "Eleitorado por Faixa Etária — 2022 vs 2024"
    if genero != "Todos":
        titulo += f" ({genero})"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=faixas, y=df22,
        name="2022",
        marker_color=AZUL_BRASIL,
        opacity=0.85,
        hovertemplate="%{x}: %{y:,.0f}<extra>2022</extra>",
    ))
    fig.add_trace(go.Bar(
        x=faixas, y=df24,
        name="2024",
        marker_color=VERDE_BRASIL,
        opacity=0.85,
        hovertemplate="%{x}: %{y:,.0f}<extra>2024</extra>",
    ))
    fig.update_layout(
        **_base_layout(
            title=dict(text=titulo, font=dict(size=13)),
            barmode="group",
            bargap=0.18,
            bargroupgap=0.05,
            xaxis=dict(
                title="Faixa Etária",
                showgrid=False,
                tickangle=-35,
                automargin=True,
            ),
            yaxis=dict(
                title="Eleitores",
                showgrid=True, gridcolor=_GRID,
                tickformat=",.0f",
                automargin=True,
            ),
            height=420,
            margin=dict(l=10, r=10, t=44, b=60),
        )
    )
    return fig