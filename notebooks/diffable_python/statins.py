# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This notebook contains SnoMed/NHS [dm+d codes](https://ebmdatalab.net/what-is-the-dmd-the-nhs-dictionary-of-medicines-and-devices/) for statins derived from the BNF code section on [lipid regulating drugs](https://openprescribing.net/bnf/0212/). 
#
#

from ebmdatalab import bq
import os
import pandas as pd

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
(bnf_code LIKE '0212000B0%' OR #  Atorvastatin
bnf_code LIKE  '0212000AJ%' OR #  Fenofibrate/Simvastatin 
bnf_code LIKE  '0212000M0%' OR #  Fluvastatin Sodium
bnf_code LIKE  '0212000X0%' OR #  Pravastatin Sodium
bnf_code LIKE  '0212000AA%' OR #  Rosuvastatin Calcium
bnf_code LIKE  '0212000Y0%' OR #  Simvastatin
bnf_code LIKE  '0212000AC%')   #  Simvastatin & Ezetimibe 
)
SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

statins_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','statins_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
statins_codelist
