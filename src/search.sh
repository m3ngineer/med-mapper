# Quick drug search commands

pip install ack

# IMBRUVICA
ack -c -l IMBRUVICA zipfiles/CMS_PartD_Prescriber_NPI_Drug_14.txt >>
# 869

ack -c -l IMBRUVICA zipfiles/CMS_PartD_Prescriber_NPI_Drug_15.txt
# 2198

ack -c -l IMBRUVICA zipfiles/CMS_PartD_Prescriber_NPI_Drug_16.txt >>
# 3315
# ZYKADIA
ack -c -l ZYKADIA zipfiles/CMS_PartD_Prescriber_NPI_Drug_14.txt
# 3

ack -c -l ZYKADIA zipfiles/CMS_PartD_Prescriber_NPI_Drug_15.txt >>
# 40

ack -c -l ZYKADIA zipfiles/CMS_PartD_Prescriber_NPI_Drug_16.txt
# 39

# GILOTRIF
ack -c -l GILOTRIF zipfiles/CMS_PartD_Prescriber_NPI_Drug_14.txt >>
# 122

ack -c -l GILOTRIF zipfiles/CMS_PartD_Prescriber_NPI_Drug_15.txt
# 258

ack -c -l GILOTRIF CMS_PartD_Prescriber_NPI_Drug_16.txt
# 333

# MEKINIST
ack -c -l MEKINIST zipfiles/CMS_PartD_Prescriber_NPI_Drug_14.txt >>
# 61

ack -c -l MEKINIST zipfiles/CMS_PartD_Prescriber_NPI_Drug_15.txt
# 99

ack -c -l MEKINIST CMS_PartD_Prescriber_NPI_Drug_16.txt
# 144


# XALKORI
ack -c -l XALKORI zipfiles/CMS_PartD_Prescriber_NPI_Drug_14.txt >>
# 139

ack -c -l XALKORI zipfiles/CMS_PartD_Prescriber_NPI_Drug_15.txt
# 213

ack -c -l XALKORI CMS_PartD_Prescriber_NPI_Drug_16.txt
# 237

# OPDIVO - nivolumab
ack -c -l nivolumab zipfiles/CMS_PartB_Provider_Util_Payment_14.txt
# 0

ack -c -l nivolumab zipfiles/CMS_PartB_Provider_Util_Payment_15.txt
# 0

ack -c nivolumab CMS_PartB_Provider_Util_Payment_CY2016.txt >>
# 558

# KEYTRUDA - pembrolizumab
ack -c -l pembrolizumab zipfiles/CMS_PartB_Provider_Util_Payment_14.txt
# 0

ack -c -l nivolumab zipfiles/CMS_PartB_Provider_Util_Payment_15.txt
# 0

ack -c nivolumab CMS_PartB_Provider_Util_Payment_CY2016.txt
# 28
