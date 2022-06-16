import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.models.ranges import Range1d
from bokeh.models import HoverTool
from datetime import datetime
import panel as pn

print('inicio')
engine = create_engine('postgresql://username:secret@db:5432/database')
conn = engine.connect()

#Query
salarios = pd.read_sql("select a.*,  \
                       b.clae6_desc, \
                       b.clae3_desc, \
                       b.clae2_desc, \
                       b.letra_desc, \
                       f.month,      \
                       f.year,       \
                       usd.dolar_estadounidense, \
                       usd.dolar_referencia_com_3500 \
                       from p_salaries.ft_salarios_actividad a \
                       inner join p_salaries.claes b \
                           on a.clae6 = b.clae6 \
                       inner join p_salaries.lk_fecha f \
                           on a.fecha = f.fecha\
                       inner join p_salaries.usd_mes usd \
                           on a.fecha = usd.indice_tiempo \
                       ", conn)

#claes = pd.read_sql("select * from p_salaries.claes", conn);

lk_fecha = pd.read_sql("select * from p_salaries.lk_fecha", conn)

usd = pd.read_sql("select a.indice_tiempo, \
                  a.dolar_estadounidense,  \
                  a.dolar_referencia_com_3500, \
                  f.month,      \
                  f.year        \
                  from p_salaries.usd_mes a \
                  inner join p_salaries.lk_fecha f  \
                       on a.indice_tiempo = f.fecha  \
                  ", conn);

ipc = pd.read_sql("select a.* ,  \
                  f.month,      \
                  f.year        \
                  from p_salaries.ipc_mes a \
                  inner join p_salaries.lk_fecha f  \
                       on a.indice_tiempo = f.fecha  \
                       ", conn);


ipc = ipc.set_index('indice_tiempo')
usd = usd.set_index('indice_tiempo')
salario_t = salarios.merge(ipc[[ 'ipc_ng_nacional', 'ipc_ng_nacional_tasa_variacion_mensual']], left_on = 'fecha', right_index = True, how='inner')

max_fecha = salario_t.fecha.max()
i_act = int(ipc[ipc.index == max_fecha].ipc_ng_nacional)
salario_t['w_median_act'] = salario_t.w_median/salario_t.ipc_ng_nacional * i_act
salario_t['w_median_usd'] = salario_t.w_median/salario_t.dolar_referencia_com_3500

#P 1
grouped = salario_t.groupby('fecha')['w_median_act'].mean().reset_index()
grouped['rma_salario_act'] = grouped.rolling(window=6).mean()
grouped_usd = salario_t.groupby('fecha')['w_median_usd'].mean().reset_index()
grouped['rma_salario_usd'] = grouped_usd.rolling(window=6).mean()
grouped['fecha'] = grouped['fecha'].astype('datetime64[ns]')

grouped["DateString"] = grouped["fecha"].dt.strftime("%Y-%m-%d")
source = ColumnDataSource(grouped)
p = figure(x_axis_type='datetime', tools='hover', plot_width=800, plot_height=300)
# Eje 1
p.line(x='fecha', y='rma_salario_act', line_width=2, source=source, legend_label='PESOS')
p.y_range = Range1d(grouped['rma_salario_act'].min()-1, grouped['rma_salario_act'].max()+1)

# Eje 2
column2_range = 'segundo y' + "_range"
p.extra_y_ranges = {column2_range: Range1d(grouped['rma_salario_usd'].min()-1, grouped['rma_salario_usd'].max()+1)}                  
p.line(x=grouped['fecha'], y=grouped['rma_salario_usd'], line_width=2, legend_label='USD', y_range_name=column2_range, color="green")

hover = p.select(dict(type=HoverTool))
hover.tooltips = [
        ("Series", "@DateString"),
        ("Pesos", "$x"),
        ("USD", "$y"),
        ]
p.title = 'Evolución'


## P2
max_date = salarios.fecha.max()
tb_int = salarios[salarios.fecha==max_date].groupby(['letra_desc','clae2_desc']).agg({'w_median':'mean'})
df_plot = tb_int[(tb_int.w_median.rank(pct=True) >= 0.9) | (tb_int.w_median.rank(pct=True) <= 0.1)].reset_index() 
#df_plot =tb_int.sort_values(by= 'w_median', ascending=False).head(15).reset_index()
a3 = px.treemap(df_plot, path=['letra_desc'], values='w_median',
                  color='w_median', 
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.mean(df_plot['w_median']), 
                width=800, height=600, title="Industrias de mayores y menores salarios reales")


##P3

max_date =salario_t.fecha.max() 
salario_last = salario_t[salario_t.fecha>=(datetime.strptime(max_date, '%Y-%m-%d') - pd.DateOffset(months=12)).strftime('%Y-%m-%d')]
salario_last = salario_last.groupby(['fecha','letra_desc'])['w_median_act'].median().reset_index()
salario_last['12m'] = salario_last.groupby('letra_desc')['w_median_act'].shift(12)
salario_last = salario_last[salario_last.fecha==max_date]
salario_last['var_interanual'] = 100*(salario_last.w_median_act / salario_last['12m'])-100

a4 = px.scatter(salario_last.sort_values(by='var_interanual', ascending=False), x="w_median_act", y="var_interanual",
	           size = 'w_median_act', color="letra_desc",hover_name="letra_desc", size_max=10,
               width=900, height=500, title="Relación entre aumento interanual real y salario rea por industria")
a4.add_vline(x=salario_last.w_median_act.mean(),line_width=1, line_dash="dash")
a4.add_hline(y=salario_last.var_interanual.mean(),line_width=1, line_dash="dash")
a4.update_layout(showlegend=False)
a4.show()


#app
print('app')
#bokeh_server.stop()
pn.extension('plotly')
ui = pn.Column(p, a3, a4)
from bokeh.resources import INLINE
ui.save('test.html', resources=INLINE)
#show(ui)
#bokeh_server = pn.panel(ui)#.show(port=5006)
#pn.serve(ui, address="0.0.0.0", port=5006)