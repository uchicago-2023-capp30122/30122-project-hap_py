import pandas as pd
import plotly.graph_objects as go

#Create dataset for visualization
data = pd.DataFrame(columns=['labels', 'parent', 'visits'])

#Load and transform data
raw = pd.read_csv('data/2020_language.csv')
raw = raw[['language', 'visits']]
parent_child = raw['language'].str.split('-', n=1, expand=True)
raw['lang1'] = parent_child[0]
raw['lang2'] = parent_child[1]
raw['id'] = range(1, len(raw)+1)
raw = raw[['id', 'lang1', 'lang2', 'visits']]

#Create parent totals
lang1_total = raw[['lang1', 'visits']].groupby('lang1').sum().reset_index()
lang1_total = lang1_total.rename(columns={'lang1': 'labels'})
lang1_total['parent'] = 'total'

#Stack 'raw' and 'parent_total'
data = pd.concat([data, parent_total[['labels', 'parent', 'visits']]])

raw = raw.rename(columns={'lang1': 'parent', 'lang2': 'labels'})
data = pd.concat(data, raw[['labels', 'parent', 'visits']])
data = data.append({'labels': 'total', 'parent': '', 'visits': lang1_total['visits'].sum()}, ignore_index=True)

#Icicle
fig = go.Figure(
    go.Icicle(
        ids = data.language,
        labels = data['child'],
        parents = data['parent'],
        values = data['visits'],
        branchvalues='total',
        root_color="lightgrey",
        tiling=dict(
            orientation='h'
        )
    )
)

fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()