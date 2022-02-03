import pandas as pd

wl = pd.read_csv('barnivore_new.csv')

wl_new = wl.rename(columns={'name': 'Name', 'producer': 'Producer', 'origin': 'Origin', 'label': 'Vegan'}, inplace=True)

wl['Vegan'] = wl['Vegan'].replace({'Not Vegan Friendly': 'No'})
wl['Vegan'] = wl['Vegan'].replace({'Vegan Friendly': 'Yes'})


wl.to_csv('barnivore_new.csv', index=False)

print(wl.head(20))

