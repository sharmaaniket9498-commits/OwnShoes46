import plotly.express as px
import plotly.graph_objects as go

BG="#101318"; GRID="#282e36"; TEXT="#dfe3e8"; MUTED="#9ca4ae"; ORANGE="#ff3b1d"; GOLD="#ff8a45"; GREEN="#27d7a0"

def style(fig, height=300):
    fig.update_layout(
        template="plotly_dark", height=height, margin=dict(l=12,r=12,t=18,b=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Onest, Arial",color=TEXT,size=11),
        legend=dict(orientation="h",y=1.12,x=0),
        xaxis=dict(showgrid=False,zeroline=False,color=MUTED),
        yaxis=dict(gridcolor=GRID,zeroline=False,color=MUTED),
    )
    return fig

def revenue_line(df):
    fig=px.line(df,x="Month",y="Revenue",markers=True)
    fig.update_traces(line=dict(color=ORANGE,width=3),marker=dict(size=6),fill="tozeroy",fillcolor="rgba(255,59,29,.12)")
    fig.update_yaxes(tickprefix="₹",tickformat="~s")
    return style(fig,300)

def revenue_profit(df):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Month"],y=df["Revenue"],name="Revenue",mode="lines+markers",line=dict(color=ORANGE,width=3),fill="tozeroy",fillcolor="rgba(255,59,29,.10)"))
    fig.add_trace(go.Scatter(x=df["Month"],y=df["Profit"],name="Profit",mode="lines+markers",line=dict(color=GOLD,width=2)))
    fig.update_yaxes(tickprefix="₹",tickformat="~s")
    return style(fig,300)

def category_bar(df, value="revenue"):
    fig=px.bar(df,x="category",y=value,color="category",color_discrete_sequence=[ORANGE,GOLD,"#e85b43","#8d969f","#d9a15f","#ff765e"])
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_width=0)
    if value in ["revenue","profit"]: fig.update_yaxes(tickprefix="₹",tickformat="~s")
    return style(fig,300)

def stock_bar(df):
    fig=px.bar(df.sort_values("stock"),x="stock",y="name",orientation="h",color="stock",color_continuous_scale=["#ff3b1d","#ff9b55"])
    fig.update_layout(showlegend=False,coloraxis_showscale=False)
    return style(fig,320)
