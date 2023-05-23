import pandas as pd

class DataTableReader:
    
    def __init__(self):
        self.material_data = pd.read_csv('data.csv', sep=';', index_col='Material')

    def get_c(self, material):
        try:
            row_data = self.material_data.loc[material]['c']
            return row_data
        except KeyError:
            print(f'Material {material} not found in table!')
            return None

    def print_table(self):
        print(self.material_data.to_markdown())

    
data_table = DataTableReader()

# return speed of sound for Blei
print('Speed of sound in lead: ' + str(data_table.get_c('Blei')))
# see what happens when material does not exist in table
print('Speed of sound in a muffin: ' + str(data_table.get_c('Muffin')))


# Luft exists multiple times in table
# To-Do: case handling for multiple entries (go by temperature)

data_table.print_table()