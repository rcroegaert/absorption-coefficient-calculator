import pandas as pd

material_data = pd.read_csv('data.csv', sep=';')

# material_data.drop(0)
# material_data.to_csv('data.csv', sep=';')

# return speed of sound for Blei
c_lead = material_data['Material', 'c']
c_lead.get('Blei')

# check if a material exists in table

print(material_data.to_markdown())