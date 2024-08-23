import pandas as pd

df_fr = pd.read_csv('resultats_fr.csv', delimiter=';', encoding='utf-8-sig')
df_en = pd.read_csv('resultats_en.csv', delimiter=';', encoding='utf-8-sig')

df_merged = pd.merge(df_fr, df_en, on='Word', suffixes=('_FR', '_EN'))

df_merged = df_merged[['Word', 'FR title', 'EN title', 'FR Indication', 'EN Indication', 'FR Definition', 'EN Definition']]

df_merged.to_csv('resultats_merged.csv', sep=';', index=False, encoding='utf-8-sig')