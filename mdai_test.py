import mdai
from pathlib import Path
from pandas.core.frame import DataFrame
import pyinputplus as pyip
import send2trash

DOMAIN = 'philips.md.ai'
AUTH_TOKEN = '47bef9d52243027bee102328b014796b'
PROJ_ID_MAP = { #these are the MD.ai project ID assigned
    1: 'gaq3pBlV', #COVID
    2: 'glBE9BVE', #SI Animal
    3: 'rLRAXB2k', #SI Clinical
    4: 'W7qygRnP', #"FAST EPIQ X5-1 3D Swine"
    5: '3VB59Bov'  #FAST Clinical (Healthy Human)
}
#all lables current as of 7/30/21
COVID_LABEL_DICT = { 
'L_DeKGNe': ('Video Annotation - MZ', 'Exclude'), 'L_keZ6xe': ('Video Annotation - MZ', 'MZ Complete'), 'L_jqOp41': ('Video Annotation - MZ', 'No Lung Sliding'), 'L_3q2jXq': ('Video Annotation - MZ', 'Trace Effusion'), 'L_8qMpDV': ('Video Annotation - MZ', 'Zone'), 'L_51AGBV': ('Video Annotation - MZ', 'A-Lines'), 'L_W1dM7e': ('Video Annotation - MZ', 'B-Lines'), 'L_M1k6aq': ('Video Annotation - MZ', 'Merged B-Lines'), 'L_KV0k5e': ('Video Annotation - MZ', 'Small Con <1 I.C.'), 'L_dez6Ee': ('Video Annotation - MZ', 'Consolidation >1 cm'), 'L_MqoLX1': ('Video Annotation - MZ', 'Pleural Effusion'), 'L_PVy6Jq': ('Video Annotation - MZ', 'PL Normal'), 'L_51jZy1': ('Video Annotation - MZ', 'Transverse'), 'L_ZqpW5V': ('Video Annotation - MZ', 'PL Interrupted'), 'L_DemWPq': ('Video Annotation - MZ', 'PL Irregular'), 'L_zqBRBq': ('Video Annotation - MZ', 'Consolidation or Atelectasis'), 'L_9eg7Ze': ('Video Annotation - MZ', 'Atelectasis'), 'L_BevREe': ('Video Annotation - MZ', 'PL Thickened'), 'L_ae5g9q': ('Video Annotation - MZ', 'Weak Sliding'), 'L_Ye42xq': ('Video Annotation - MZ', '>=3 Single B-Lines'), 'L_K164gV': ('Video Annotation - MZ', 'Probe Flipped'), 'L_bq86Qe': ('Video Annotation - MZ', 'Poor Quality / Poor View'), 'L_0q9WMe': ('Video Annotation - MZ', 'Small Con >1 I.C.'), 'L_keEaWe': ('Video Annotation - NS', 'Exclude'), 'L_aexNjq': ('Video Annotation - NS', 'NS Complete'), 'L_JVLPRV': ('Video Annotation - NS', 'Weak Sliding'), 'L_MVwyg1': ('Video Annotation - NS', 'Trace Effusion'), 'L_M1X0j1': ('Video Annotation - NS', 'Zone'), 'L_7Vaxxe': ('Video Annotation - NS', 'A-Lines'), 'L_MeWwme': ('Video Annotation - NS', 'B-Lines'), 'L_LqPzAe': ('Video Annotation - NS', 'Merged B-Lines'), 'L_Bq3kNq': ('Video Annotation - NS', 'Small Con <1 I.C.'), 'L_mqndKe': ('Video Annotation - NS', 'Consolidation >1 cm'), 'L_pqY0YV': ('Video Annotation - NS', 'Pleural Effusion'), 'L_L1Qax1': ('Video Annotation - NS', 'PL Normal'), 'L_a1lAMe': ('Video Annotation - NS', 'Transverse'), 'L_717N3q': ('Video Annotation - NS', 'PL Interrupted'), 'L_0q9w2e': ('Video Annotation - NS', 'PL Irregular'), 'L_8ebAl1': ('Video Annotation - NS', 'Consolidation or Atelectasis'), 'L_EqG63V': ('Video Annotation - NS', 'Atelectasis'), 'L_jqRzJq': ('Video Annotation - NS', 'PL Thickened'), 'L_9egPZV': ('Video Annotation - NS', 'No Lung Sliding'), 'L_BevdEq': ('Video Annotation - NS', '>=3 Single B-Lines'), 'L_Bq3klq': ('Video Annotation - NS', 'Probe Flipped'), 'L_mqndxe': ('Video Annotation - NS', 'Poor Quality / Poor View'), 'L_8ebRke': ('Video Annotation - NS', 'Small Con >1 I.C.'), 'L_6qrlve': ('Video Annotation - NS', 'B-Line Severity'), 'L_M1kgG1': ('Video Annotation - NS', 'PL Severity'), 'L_KV0XZV': ('Video Annotation - NS', 'Consolidation Severity'), 'L_pqY0GV': ('Frame Annotations', 'FA Complete'), 'L_8ebAk1': ('Frame Annotations', 'A-Lines'), 'L_EqG6QV': ('Frame Annotations', 'B-Lines'), 'L_jqRzlq': ('Frame Annotations', 'Merged B-Lines'), 'L_9egPpV': ('Frame Annotations', 'Small Con <1 I.C.'), 'L_BevdKq': ('Frame Annotations', 'Consolidation >1 cm'), 'L_ae5jAV': ('Frame Annotations', 'Pleural Effusion'), 'L_6qrzZq': ('Frame Annotations', 'PL Normal'), 'L_keZEG1': ('Frame Annotations', 'PL Interrupted'), 'L_jqOD61': ('Frame Annotations', 'PL Irregular'), 'L_3q2wa1': ('Frame Annotations', 'Consolidation or Atelectasis'), 'L_8qMm7q': ('Frame Annotations', 'Atelectasis'), 'L_51Alrq': ('Frame Annotations', 'PL Thickened'), 'L_M1km0V': ('Frame Annotations', '>=3 Single B-lines'), 'L_EqGgQq': ('Frame Annotations', 'Small Con >1 I.C.'), 'L_jqRmlV': ('Frame Annotations', 'Trace Effusion'), 'L_0q9pkV': ('Frame Annotations', 'Other Organ'), 'L_8ebGNV': ('Frame Annotations', 'Group Review Needed'), 'L_EqGWoq': ('Frame Annotations', 'Poor Quality / Poor View'), 'L_bq8Xjq': ('Adjudication', 'VA REVIEW COMPLETE'), 'L_keE4O1': ('Adjudication', 'FA ALL COMPLETE'), 'L_aexgp1': ('Adjudication', 'FA REVIEW COMPLETE'), 'L_pqY47V': ('Adjudication', 'FA B-lines Complete'), 'L_L1QPoq': ('Adjudication', 'FA Pleural Line Complete'), 'L_a1lMre': ('Adjudication', 'FA Consolidation Complete'), 'L_717p9e': ('Adjudication', 'FA Pleural Effusion Complete'), 'L_KV0OPe': ('Video Annotation - MK', 'Exclude'), 'L_dezwMV': ('Video Annotation - MK', 'MK Complete'), 'L_Mqowxq': ('Video Annotation - MK', 'No Lung Sliding'), 'L_PVyw01': ('Video Annotation - MK', 'Trace Effusion'), 'L_51jwNe': ('Video Annotation - MK', 'Zone'), 'L_ZqpwRV': ('Video Annotation - MK', 'A-Lines'), 'L_DemN2V': ('Video Annotation - MK', 'B-Lines'), 'L_zqBydV': ('Video Annotation - MK', 'Merged B-Lines'), 'L_xVDpyV': ('Video Annotation - MK', 'Small Con <1 I.C.'), 'L_WeN3MV': ('Video Annotation - MK', 'Consolidation >1 cm'), 'L_BVJ4k1': ('Video Annotation - MK', 'Pleural Effusion'), 'L_Ye4vxq': ('Video Annotation - MK', 'PL Normal'), 'L_K16rg1': ('Video Annotation - MK', 'Transverse'), 'L_bq8ZQe': ('Video Annotation - MK', 'PL Interrupted'), 'L_keEmWe': ('Video Annotation - MK', 'PL Irregular'), 'L_aex7j1': ('Video Annotation - MK', 'Consolidation or Atelectasis'), 'L_JVL8RV': ('Video Annotation - MK', 'Atelectasis'), 'L_MVwlgq': ('Video Annotation - MK', 'PL Thickened'), 'L_M1Xgjq': ('Video Annotation - MK', 'Weak Sliding'), 'L_7VaAxV': ('Video Annotation - MK', '>=3 Single B-Lines'), 'L_MeWRm1': ('Video Annotation - MK', 'Probe Flipped'), 'L_LqPYA1': ('Video Annotation - MK', 'Poor Quality / Poor View'), 'L_Bq3gNq': ('Video Annotation - MK', 'Small Con >1 I.C.'), 'L_LqPZDe': ('Video Annotation - BH', 'Exclude'), 'L_Bq3yle': ('Video Annotation - BH', 'BH Complete'), 'L_mqn9xV': ('Video Annotation - BH', 'No Lung Sliding'), 'L_pqYoGe': ('Video Annotation - BH', 'Trace Effusion'), 'L_L1QO5V': ('Video Annotation - BH', 'Zone'), 'L_a1llY1': ('Video Annotation - BH', 'A-Lines'), 'L_717BMq': ('Video Annotation - BH', 'B-Lines'), 'L_0q9NM1': ('Video Annotation - BH', 'Merged B-Lines'), 'L_8eb4kq': ('Video Annotation - BH', 'Small Con <1 I.C.'), 'L_EqG9Qe': ('Video Annotation - BH', 'Consolidation >1 cm'), 'L_jqR2lq': ('Video Annotation - BH', 'Pleural Effusion'), 'L_9egLpV': ('Video Annotation - BH', 'PL Normal'), 'L_BevKKV': ('Video Annotation - BH', 'Transverse'), 'L_ae5pA1': ('Video Annotation - BH', 'PL Interrupted'), 'L_6qrgZ1': ('Video Annotation - BH', 'PL Irregular'), 'L_DeKg3e': ('Video Annotation - BH', 'Consolidation or Atelectasis'), 'L_keZyG1': ('Video Annotation - BH', 'Atelectasis'), 'L_jqO76q': ('Video Annotation - BH', 'PL Thickened'), 'L_3q2Oa1': ('Video Annotation - BH', 'Weak Sliding'), 'L_8qMQ7q': ('Video Annotation - BH', '>=3 Single B-Lines'), 'L_51ANre': ('Video Annotation - BH', 'Probe Flipped'), 'L_W1djPV': ('Video Annotation - BH', 'Poor Quality / Poor View'), 'L_M1k40e': ('Video Annotation - BH', 'Small Con >1 I.C.')
}
SI_ANIMAL_LABEL_DICT = {
'L_keEP21': ('Video Annotation 1 - MZ', 'Exclude'), 'L_aexvmq': ('Video Annotation 1 - MZ', 'MZ Complete'), 'L_MeWb61': ('Video Annotation 1 - MZ', 'Zone'), 'L_LqPrEe': ('Video Annotation 1 - MZ', 'A-Lines'), 'L_Bq3PE1': ('Video Annotation 1 - MZ', 'B-Lines'), 'L_mqnzdq': ('Video Annotation 1 - MZ', 'Merged B-Lines'), 'L_717vgq': ('Video Annotation 1 - MZ', 'Small Con <1 I.C.'), 'L_8ebZpe': ('Video Annotation 1 - MZ', 'Pleural Effusion'), 'L_EqG2WV': ('Video Annotation 1 - MZ', 'Consolidation >1 cm'), 'L_BVJk6q': ('Video Annotation 1 - MZ', 'PL normal'), 'L_Ye46Eq': ('Video Annotation 1 - MZ', 'PL thickening'), 'L_K16yWq': ('Video Annotation 1 - MZ', 'PL irregular'), 'L_bq8krV': ('Video Annotation 1 - MZ', 'PL interrupted'), 'L_keE22V': ('Video Annotation 1 - MZ', 'Transverse'), 'L_zqBk91': ('Video Annotation 1 - MZ', 'Poor Quality / poor view'), 'L_xVDvn1': ('Video Annotation 1 - MZ', 'Probe Flipped'), 'L_6qr6nq': ('Video Annotation 1 - MZ', '>=3 Single B-Lines'), 'L_PVyGQ1': ('Video Annotation 1 - MZ', 'No Lung Sliding'), 'L_51jg8e': ('Video Annotation 1 - MZ', 'Weak Sliding'), 'L_ZqpOMV': ('Video Annotation 1 - MZ', 'Trace Effusion'), 'L_DemrKV': ('Video Annotation 1 - MZ', 'Atelectasis'), 'L_zqB02e': ('Video Annotation 1 - MZ', 'Small Con >1 I.C.'), 'L_xVD09V': ('Video Annotation 1 - MZ', 'Consolidation or Atelectasis'), 'L_Ye4J2q': ('Video Annotation 2 - NS', 'Exclude'), 'L_K16goe': ('Video Annotation 2 - NS', 'NS Complete'), 'L_keErZV': ('Video Annotation 2 - NS', 'Zone'), 'L_aexob1': ('Video Annotation 2 - NS', 'A-Lines'), 'L_JVLZN1': ('Video Annotation 2 - NS', 'B-Lines'), 'L_MVwoQV': ('Video Annotation 2 - NS', 'Merged B-Lines'), 'L_M1X74q': ('Video Annotation 2 - NS', 'Small Con <1 I.C.'), 'L_7Va43e': ('Video Annotation 2 - NS', 'Pleural Effusion'), 'L_MeWlQV': ('Video Annotation 2 - NS', 'Consolidation >1 cm'), 'L_LqPOoV': ('Video Annotation 2 - NS', 'PL normal'), 'L_Bq3xm1': ('Video Annotation 2 - NS', 'PL thickening'), 'L_mqn5aV': ('Video Annotation 2 - NS', 'PL irregular'), 'L_pqYmnq': ('Video Annotation 2 - NS', 'PL interrupted'), 'L_L1QEB1': ('Video Annotation 2 - NS', 'Transverse'), 'L_a1loWq': ('Video Annotation 2 - NS', 'Poor Quality / poor view'), 'L_717jbq': ('Video Annotation 2 - NS', 'Probe Flipped'), 'L_pqYymq': ('Video Annotation 2 - NS', '>=3 Single B-Lines'), 'L_BVJ0p1': ('Video Annotation 2 - NS', 'No Lung Sliding'), 'L_Ye4blq': ('Video Annotation 2 - NS', 'Weak Sliding'), 'L_K16RQ1': ('Video Annotation 2 - NS', 'Trace Effusion'), 'L_bq8vLe': ('Video Annotation 2 - NS', 'Atelectasis'), 'L_keEoXq': ('Video Annotation 2 - NS', 'Small Con >1 I.C.'), 'L_aexb2q': ('Video Annotation 2 - NS', 'Consolidation or Atelectasis'), 'L_EqGa8e': ('Frame Annotations', 'Frame Annotation Complete'), 'L_Bev29e': ('Frame Annotations', 'A-Lines'), 'L_Bq3xA1': ('Frame Annotations', 'B-Lines'), 'L_mqn5JV': ('Frame Annotations', 'Merged B-Lines'), 'L_pqYmrq': ('Frame Annotations', 'Small Con <1 I.C.'), 'L_L1QEO1': ('Frame Annotations', 'Pleural Effusion'), 'L_a1lo6q': ('Frame Annotations', 'Consolidation >1 cm'), 'L_717jLq': ('Frame Annotations', 'PL normal'), 'L_0q94oV': ('Frame Annotations', 'PL thickening'), 'L_8ebboe': ('Frame Annotations', 'PL irregular'), 'L_EqGKZq': ('Frame Annotations', 'PL interrupted'), 'L_MVw9b1': ('Frame Annotations', 'Atelectasis'), 'L_M1XRdV': ('Frame Annotations', '>=3 Single B-lines'), 'L_7VanAq': ('Frame Annotations', 'Small Con >1 I.C.'), 'L_MeWGve': ('Frame Annotations', 'Trace Effusion'), 'L_LqPnZe': ('Frame Annotations', 'Consolidation or Atelectasis'), 'L_6qrNDq': ('Adjudication', 'Exclude disagree'), 'L_jqOyEe': ('Adjudication', 'Zone disagree'), 'L_3q2lJe': ('Adjudication', 'A-Lines disagree'), 'L_8qMPpV': ('Adjudication', 'B-Lines disagree'), 'L_51AkwV': ('Adjudication', 'Merged B-Lines disagree'), 'L_W1dLN1': ('Adjudication', 'Small Con >1 I.C. disagree'), 'L_M1kO81': ('Adjudication', 'Pleural Effusion disagree'), 'L_KV0YDq': ('Adjudication', 'Consolidation >1 cm disagree'), 'L_dezpKq': ('Adjudication', 'PL normal disagree'), 'L_MqoyRe': ('Adjudication', 'PL thickening disagree'), 'L_PVyPGe': ('Adjudication', 'PL irregular disagree'), 'L_51jdnV': ('Adjudication', 'PL interrupted disagree'), 'L_Zqpvke': ('Adjudication', 'Transverse disagree'), 'L_DemvAV': ('Adjudication', 'Poor Quality / poor view disagree'), 'L_zqBrvq': ('Adjudication', 'Probe Flipped disagree'), 'L_L1QpDq': ('Adjudication', '>=3 Single B-Line disagree'), 'L_Bq392e': ('Adjudication', 'Consolidation or Atelectasis disagree'), 'L_mqnKv1': ('Adjudication', 'Atelectasis disagree'), 'L_pqYgKe': ('Adjudication', 'Small con <1 I.C. disagree'), 'L_L1QY41': ('Adjudication', 'Trace Effusion disagree'), 'L_a1lQxe': ('Adjudication', 'No Lung Sliding disagree'), 'L_717Dde': ('Adjudication', 'Weak sliding disagree')
}
SI_CLINICAL_LABEL_DICT = {
'L_jqO4v1': ('Video Annotation 1 - MZ', 'Exclude'), 'L_3q2pRe': ('Video Annotation 1 - MZ', 'Poor Quality / poor view'), 'L_8qM4nV': ('Video Annotation 1 - MZ', 'Zone'), 'L_51AX3q': ('Video Annotation 1 - MZ', 'Probe Flipped'), 'L_dez5B1': ('Video Annotation 1 - MZ', 'Transverse'), 'L_MqoKpq': ('Video Annotation 1 - MZ', 'No Lung Sliding'), 'L_PVyQ5V': ('Video Annotation 1 - MZ', 'Weak Sliding'), 'L_51jRo1': ('Video Annotation 1 - MZ', 'A-Lines'), 'L_ZqpZpe': ('Video Annotation 1 - MZ', 'B-Lines'), 'L_Dem5oe': ('Video Annotation 1 - MZ', 'Merged B-Lines'), 'L_zqBv3q': ('Video Annotation 1 - MZ', '>=3 Single B-Lines'), 'L_xVDrv1': ('Video Annotation 1 - MZ', 'Small Con <1 I.C.'), 'L_WeNLyq': ('Video Annotation 1 - MZ', 'Small Con > 1 I.C.'), 'L_BVJPL1': ('Video Annotation 1 - MZ', 'Consolidation >1 cm'), 'L_Ye4Xke': ('Video Annotation 1 - MZ', 'Consolidation or Atelectasis'), 'L_K16XAV': ('Video Annotation 1 - MZ', 'Atelectasis'), 'L_bq8n4e': ('Video Annotation 1 - MZ', 'Pleural Effusion'), 'L_keEK7q': ('Video Annotation 1 - MZ', 'Trace Effusion'), 'L_aexYNV': ('Video Annotation 1 - MZ', 'PL normal'), 'L_JVLLBV': ('Video Annotation 1 - MZ', 'PL thickening'), 'L_MVwnve': ('Video Annotation 1 - MZ', 'PL irregular'), 'L_M1XLY1': ('Video Annotation 1 - MZ', 'PL interrupted'), 'L_7Va3n1': ('Video Annotation 1 - MZ', 'MZ Complete'), 'L_MeWL3V': ('Video Annotation 2 - NS', 'Exclude'), 'L_LqPLxq': ('Video Annotation 2 - NS', 'Poor Quality / poor view'), 'L_Bq3Xp1': ('Video Annotation 2 - NS', 'Zone'), 'L_mqnrrq': ('Video Annotation 2 - NS', 'Probe Flipped'), 'L_pqYL7V': ('Video Annotation 2 - NS', 'Transverse'), 'L_L1QLoq': ('Video Annotation 2 - NS', 'No Lung Sliding'), 'L_a1lvrV': ('Video Annotation 2 - NS', 'Weak Sliding'), 'L_717391': ('Video Annotation 2 - NS', 'A-Lines'), 'L_0q9Ykq': ('Video Annotation 2 - NS', 'B-Lines'), 'L_8ebnNe': ('Video Annotation 2 - NS', 'Merged B-Lines'), 'L_EqGOoq': ('Video Annotation 2 - NS', '>=3 Single B-Lines'), 'L_jqRLPe': ('Video Annotation 2 - NS', 'Small Con <1 I.C.'), 'L_9eg90q': ('Video Annotation 2 - NS', 'Small Con > 1 I.C.'), 'L_Bev3MV': ('Video Annotation 2 - NS', 'Consolidation >1 cm'), 'L_ae5X81': ('Video Annotation 2 - NS', 'Consolidation or Atelectasis'), 'L_6qr2vq': ('Video Annotation 2 - NS', 'Atelectasis'), 'L_DeKdYV': ('Video Annotation 2 - NS', 'Pleural Effusion'), 'L_keZLrq': ('Video Annotation 2 - NS', 'Trace Effusion'), 'L_jqOLv1': ('Video Annotation 2 - NS', 'PL normal'), 'L_3q2XRe': ('Video Annotation 2 - NS', 'PL thickening'), 'L_8qMLnV': ('Video Annotation 2 - NS', 'PL irregular'), 'L_51Ag3V': ('Video Annotation 2 - NS', 'PL interrupted'), 'L_W1dQje': ('Video Annotation 2 - NS', 'NS Complete'), 'L_PVyB5q': ('Frame Annotations', 'A-Lines'), 'L_51j8oV': ('Frame Annotations', 'B-Lines'), 'L_ZqpBpe': ('Frame Annotations', 'Merged B-Lines'), 'L_DemBoV': ('Frame Annotations', '>=3 Single B-Lines'), 'L_zqBj3q': ('Frame Annotations', 'Small Con <1 I.C.'), 'L_xVDJv1': ('Frame Annotations', 'Small Con >1 I.C.'), 'L_WeNjye': ('Frame Annotations', 'Consolidation >1 cm'), 'L_BVJBLV': ('Frame Annotations', 'Consolidation or Atelectasis'), 'L_Ye45kV': ('Frame Annotations', 'Atelectasis'), 'L_K16KAe': ('Frame Annotations', 'Pleural Effusion'), 'L_bq8O4V': ('Frame Annotations', 'Trace Effusion'), 'L_keEj7V': ('Frame Annotations', 'PL normal'), 'L_aexBNq': ('Frame Annotations', 'PL thickening'), 'L_JVLpBV': ('Frame Annotations', 'PL irregular'), 'L_MVwBve': ('Frame Annotations', 'PL interrupted'), 'L_M1XPY1': ('Frame Annotations', 'Frame Annotation Complete')
}
FAST_ANIMAL_LABEL_DICT = {
'L_L1Q2Be': ('Video Annotation LUQ - Meihua', 'Negative'), 'L_a1lbWV': ('Video Annotation LUQ - Meihua', 'Small'), 'L_717Xbe': ('Video Annotation LUQ - Meihua', 'Moderate'), 'L_0q9j91': ('Video Annotation LUQ - Meihua', 'Large'), 'L_8ebxBq': ('Video Annotation LUQ - Meihua', 'Stomach'), 'L_EqG78q': ('Video Annotation LUQ - Meihua', 'IVC'), 'L_jqRw51': ('Video Annotation LUQ - Meihua', 'Clot'), 'L_Bevx9q': ('Video Annotation LUQ - Meihua', 'Kidney'), 'L_ae54k1': ('Video Annotation LUQ - Meihua', 'Spleen'), 'L_6qrpEe': ('Video Annotation LUQ - Meihua', 'Exclude From Annotation'), 'L_keZDyq': ('Video Annotation LUQ - Meihua', 'Diaphragm'), 'L_jqO071': ('Video Annotation LUQ - Meihua', 'Inconclusive'), 'L_3q2x4e': ('Video Annotation LUQ - Meihua', 'LUQ'), 'L_8qM2Y1': ('Video Annotation LUQ - Meihua', 'Meihua Complete'), 'L_Ye408e': ('Video Annotation LUQ - Meihua', 'NDI KEY FRAME'), 'L_717pNe': ('Video Annotation LUQ - Meihua', 'Low IQ - Set Aside '), 'L_51Adnq': ('Video Annotation LUQ - Nikolai', 'Negative'), 'L_M1k0Ze': ('Video Annotation LUQ - Nikolai', 'Small'), 'L_KV0xrV': ('Video Annotation LUQ - Nikolai', 'Moderate'), 'L_deznDe': ('Video Annotation LUQ - Nikolai', 'Large'), 'L_MqoD01': ('Video Annotation LUQ - Nikolai', 'Inconclusive'), 'L_51j07V': ('Video Annotation LUQ - Nikolai', 'LUQ'), 'L_ZqpDvq': ('Video Annotation LUQ - Nikolai', 'Exclude From Annotation'), 'L_Dem0z1': ('Video Annotation LUQ - Nikolai', 'Stomach'), 'L_zqB391': ('Video Annotation LUQ - Nikolai', 'IVC'), 'L_xVDYnq': ('Video Annotation LUQ - Nikolai', 'Clot'), 'L_WeN25e': ('Video Annotation LUQ - Nikolai', 'Kidney'), 'L_BVJGgq': ('Video Annotation LUQ - Nikolai', 'Spleen'), 'L_Ye4x2e': ('Video Annotation LUQ - Nikolai', 'Diaphragm'), 'L_K16aoq': ('Video Annotation LUQ - Nikolai', 'Nikolai Complete'), 'L_K16Ekq': ('Video Annotation LUQ - Nikolai', 'NDI KEY FRAME'), 'L_0q9pWV': ('Video Annotation LUQ - Nikolai', 'Low IQ - Set Aside '), 'L_W1dRdV': ('Frame Annotation LUQ', 'IVC'), 'L_bq83WV': ('Frame Annotation LUQ', 'Stomach'), 'L_keEQZe': ('Frame Annotation LUQ', 'Free Fluid 1'), 'L_aexmbV': ('Frame Annotation LUQ', 'Free Fluid 2'), 'L_JVLENq': ('Frame Annotation LUQ', 'Free Fluid 3'), 'L_MVw6Qe': ('Frame Annotation LUQ', 'Free Fluid 4'), 'L_M1XO4q': ('Frame Annotation LUQ', 'Free Fluid 5'), 'L_7Va53V': ('Frame Annotation LUQ', 'VA Concordant'), 'L_MeWzQ1': ('Frame Annotation LUQ', 'FA COMPLETE'), 'L_LqPGoV': ('Frame Annotation LUQ', 'FA REVIEW COMPLETE'), 'L_JVL4OV': ('Frame Annotation LUQ', 'Group Review'), 'L_LqP4yq': ('Frame Annotation LUQ', 'Pre-Annotation Keep'), 'L_BevXEq': ('Frame Annotation LUQ', 'Free Fluid Predict'), 'L_7Vab5q': ('pre-annotation', 'Prediction_Okay'), 'L_xVDRD1': ('Data_info', 'Ok_to_annotate'), 'L_BVJZ3V': ('Data_info', 'NDI Key Frame Philips')
}
FAST_CLINICAL_LABEL_DICT = {
'L_mqnDre': ('Video Annotation - Meihua', 'Negative'), 'L_pqY77e': ('Video Annotation - Meihua', 'Small'), 'L_L1Qjoe': ('Video Annotation - Meihua', 'Moderate'), 'L_a1lBrV': ('Video Annotation - Meihua', 'Large'), 'L_8ebKNV': ('Video Annotation - Meihua', 'Clot'), 'L_9egA0q': ('Video Annotation - Meihua', 'Exclude From Annotation'), 'L_Bq3v8V': ('Video Annotation - Meihua', 'Inconclusive'), 'L_pqY7Oe': ('Video Annotation - Meihua', 'Meihua Complete'), 'L_L1Qjle': ('Video Annotation - Meihua', 'NDI KEY FRAME'), 'L_a1lBwV': ('Video Annotation - Meihua', 'Low IQ - Set Aside '), 'L_a1labe': ('Video Annotation - Meihua', 'IVC'), 'L_7179RV': ('Video Annotation - Meihua', 'Aorta'), 'L_8ebJ6e': ('Video Annotation - Meihua', 'Gallbladder'), 'L_EqG0E1': ('Video Annotation - Meihua', 'Spine'), 'L_9egadq': ('Video Annotation - Meihua', 'Stomach'), 'L_BevaR1': ('Video Annotation - Meihua', 'Diaphragm'), 'L_Ye4QZV': ('Video Annotation - Meihua', 'Liver'), 'L_K167Ze': ('Video Annotation - Meihua', 'Kidney'), 'L_bq8bKe': ('Video Annotation - Meihua', 'Spleen'), 'L_keEdn1': ('Video Annotation - Meihua', 'Bladder'), 'L_717ZKq': ('Video Annotation - Nikolai', 'Negative'), 'L_0q92A1': ('Video Annotation - Nikolai', 'Small'), 'L_8ebK4V': ('Video Annotation - Nikolai', 'Moderate'), 'L_EqGjxV': ('Video Annotation - Nikolai', 'Large'), 'L_jqRjoq': ('Video Annotation - Nikolai', 'Inconclusive'), 'L_BevBke': ('Video Annotation - Nikolai', 'Exclude From Annotation'), 'L_DeKDZV': ('Video Annotation - Nikolai', 'Clot'), 'L_8qMoge': ('Video Annotation - Nikolai', 'Nikolai Complete'), 'L_51ABke': ('Video Annotation - Nikolai', 'NDI KEY FRAME'), 'L_W1d9Ee': ('Video Annotation - Nikolai', 'Low IQ - Set Aside '), 'L_aexa7V': ('Video Annotation - Nikolai', 'IVC'), 'L_JVLJ31': ('Video Annotation - Nikolai', 'Aorta'), 'L_MVwaZ1': ('Video Annotation - Nikolai', 'Gallbladder'), 'L_M1XJKV': ('Video Annotation - Nikolai', 'Spine'), 'L_7VaawV': ('Video Annotation - Nikolai', 'Stomach'), 'L_MeWJ51': ('Video Annotation - Nikolai', 'Diaphragm'), 'L_LqPJNe': ('Video Annotation - Nikolai', 'Liver'), 'L_Bq3ZwV': ('Video Annotation - Nikolai', 'Kidney'), 'L_mqn0Re': ('Video Annotation - Nikolai', 'Spleen'), 'L_pqYnb1': ('Video Annotation - Nikolai', 'Bladder'), 'L_M1krMq': ('Frame Annotation LUQ', 'IVC'), 'L_dezWYV': ('Frame Annotation LUQ', 'Free Fluid'), 'L_DemZbV': ('Frame Annotation LUQ', 'VA Concordant'), 'L_zqBW01': ('Frame Annotation LUQ', 'FA COMPLETE'), 'L_xVDX4V': ('Frame Annotation LUQ', 'FA REVIEW COMPLETE'), 'L_WeNoxV': ('Frame Annotation LUQ', 'Group Review'), 'L_BVJmxe': ('Frame Annotation LUQ', 'PA_FF_Predict'), 'L_Ye4BXq': ('Frame Annotation LUQ', 'PA_Predict_Keep'), 'L_L1QolV': ('Frame Annotation LUQ', 'Aorta'), 'L_a1lKwq': ('Frame Annotation LUQ', 'Diaphragm'), 'L_717wK1': ('Frame Annotation LUQ', 'Spine'), 'L_8ebl4q': ('Frame Annotation LUQ', 'Stomach'), 'L_EqGmxe': ('Frame Annotation LUQ', 'Kidney'), 'L_jqRaoV': ('Frame Annotation LUQ', 'Spleen'), 'L_9egRm1': ('Frame Annotation RUQ', 'IVC'), 'L_BevWkV': ('Frame Annotation RUQ', 'Gallbladder'), 'L_ae5mWe': ('Frame Annotation RUQ', 'Free Fluid'), 'L_3q2m6V': ('Frame Annotation RUQ', 'VA Concordant'), 'L_8qM9gq': ('Frame Annotation RUQ', 'FA COMPLETE'), 'L_51AEk1': ('Frame Annotation RUQ', 'FA REVIEW COMPLETE'), 'L_W1d7Eq': ('Frame Annotation RUQ', 'Group Review'), 'L_M1k5MV': ('Frame Annotation RUQ', 'PA_FF_Predict'), 'L_KV0mkq': ('Frame Annotation RUQ', 'PA_Predict_Keep'), 'L_dezQY1': ('Frame Annotation RUQ', 'Aorta'), 'L_MqoONq': ('Frame Annotation RUQ', 'Diaphragm'), 'L_PVyYdV': ('Frame Annotation RUQ', 'Spine'), 'L_51jvx1': ('Frame Annotation RUQ', 'Bowel'), 'L_Zqp2le': ('Frame Annotation RUQ', 'Kidney'), 'L_DemKbq': ('Frame Annotation RUQ', 'Liver'), 'L_zqBN0q': ('Frame Annotation SP', 'Bladder'), 'L_xVDm4q': ('Frame Annotation SP', 'Free Fluid'), 'L_bq8mB1': ('Frame Annotation SP', 'VA Concordant'), 'L_keExx1': ('Frame Annotation SP', 'FA COMPLETE'), 'L_aexnaq': ('Frame Annotation SP', 'FA REVIEW COMPLETE'), 'L_JVL7Ke': ('Frame Annotation SP', 'Group Review'), 'L_7VaY8V': ('Frame Annotation SP', 'Uterus + Cervix'), 'L_MeWO9e': ('Frame Annotation SP', 'Bowel'), 'L_LqPRve': ('Frame Annotation SP', 'lateral bladder edge  '), 'L_Bq3m8e': ('Frame Annotation SP', 'Prostate'), 'L_L1QglV': ('Frame Annotation SP', 'transverse bladder edge')
}

# input: valid datafile in MD.ai file format as of 7/27/21
# output: df in format fit for output to Excel for input into Smartsheet
def format_df(df, project_ID) -> DataFrame:
    df = df[['StudyInstanceUID', 'dataset', 'number', 'groupId', 'groupName', 'labelName', 'note']]
    df = df.sort_values(by=['dataset', 'number'])
    studyID = ''
    annoGroup = ''
    #annoGroupName = ''
    labelName = ''
    annoNote = ''

    if(project_ID == 'gaq3pBlV'):    #COVID
        #set up the output df to match tracker columns
        # columns = {
        #     'Study ID':[],
        #     'Site':[],
        #     'Day':[],
        #     'Transducer':[],
        #     'Exam #':[],
        #     'Lung Zone':[],
        #     'Orientation':[],
        #     'VA Read (MZ)':[],
        #     'VA Image Quality Comments (MZ)':[],
        #     'VA Comments (MZ)':[],
        #     'VA Read (NS)':[],
        #     'VA Image Quality Comments (NS)':[],
        #     'VA Comments (NS)':[],
        #     'VA Read (MK)':[],
        #     'VA Image Quality Comments (MK)':[],
        #     'VA Comments (MK)':[]
        # }
        columns = {
            'Dataset':[],
            'Exam #':[],
            'Lung Zone':[],
            'Orientation':[],
            'VA Read (MZ)':[],
            'VA Comments (MZ)':[],
            'VA Read (NS)':[],
            'VA Comments (NS)':[],
            'VA Read (MK)':[],
            'VA Comments (MK)':[]
        }
        working_df = DataFrame(columns)
        # next_row = {
        #     'Study ID':'',
        #     'Site':'',
        #     'Day':'',
        #     'Transducer':'',
        #     'Exam #':'',
        #     'Lung Zone':'',
        #     'Orientation':'',
        #     'VA Read (MZ)':'',
        #     'VA Image Quality Comments (MZ)':'',
        #     'VA Comments (MZ)':'',
        #     'VA Read (NS)':'',
        #     'VA Image Quality Comments (NS)':'',
        #     'VA Comments (NS)':'',
        #     'VA Read (MK)':'',
        #     'VA Image Quality Comments (MK)':'',
        #     'VA Comments (MK)':''
        # }
        working_row = {
            'Dataset': '',
            'Exam #': '',
            'Lung Zone': '',
            'Orientation': '',
            'VA Read (MZ)': '',
            'VA Comments (MZ)': '',
            'VA Read (NS)': '',
            'VA Comments (NS)': '',
            'VA Read (MK)': '',
            'VA Comments (MK)': ''
        }

        #pull input df data and put it in the output df
        for row in df.itertuples():

            if(row.StudyInstanceUID != studyID): #this is either a new exam or the very first row
                if(studyID != ''): #this is a new exam && not the very first row
                    #write previous exam's data
                    working_df = working_df.append(working_row, ignore_index=True)
                    #reset our working row
                    working_row['Dataset'] = ''
                    working_row['Exam #'] = ''
                    working_row['Lung Zone'] = ''
                    working_row['Orientation'] = ''
                    working_row['VA Read (MZ)'] = ''
                    working_row['VA Comments (MZ)'] = ''
                    working_row['VA Read (NS)'] = ''
                    working_row['VA Comments (NS)'] = ''
                    working_row['VA Read (MK)'] = ''
                    working_row['VA Comments (MK)'] = ''
                # else: #this is the very first row
                #     working_row['Orientation'] = 'longitudinal'
                
                working_row['Orientation'] = 'longitudinal' #default is longi and is changed w/the below label
                studyID = row.StudyInstanceUID
                working_row['Dataset'] = row.dataset
                working_row['Exam #'] = str(row.number)

            #process the row
            annoGroup = row.groupId
            # annoGroupName = row.groupName
            labelName = row.labelName
            if(labelName == 'None'): labelName = ""
            #labelName += "\n"
            annoNote = str(row.note)
            if(annoNote == 'None'): annoNote = ""
            #annoNote += "; "

            #check for zone
            if(labelName == 'Zone'):
                annoNote = annoNote.replace('t', '')
                annoNote = annoNote.replace('T', '')
                working_row['Lung Zone'] = annoNote
            #handle orientation
            elif(labelName == 'Transverse'):
                working_row['Orientation'] = 'transverse'
            elif(annoGroup == 'G_dga6wY'): #MZ
                #add to mz columns (annotation label & annotation note)
                if(labelName != 'MZ Complete'):
                    if(working_row['VA Read (MZ)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (MZ)'] += labelName
                    if(working_row['VA Comments (MZ)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (MZ)'] += annoNote
            elif(annoGroup == 'G_jYoLjR'): #NS
                #add to ns columns
                if(labelName != 'NS Complete'):
                    if(working_row['VA Read (NS)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (NS)'] += labelName
                    if(working_row['VA Comments (NS)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (NS)'] += annoNote
            elif(annoGroup == 'G_zYPwag'): #MK
                #add to mk columns
                if(labelName != 'MK Complete'):
                    if(working_row['VA Read (MK)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (MK)'] += labelName
                    if(working_row['VA Comments (MK)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (MK)'] += annoNote
                

    elif(project_ID == 'glBE9BVE'): #SI Animal
        x = 1+2
    elif(project_ID == 'rLRAXB2k'): #SI Clinical
        x = 1+2
    elif(project_ID == 'W7qygRnP'): #"FAST EPIQ X5-1 3D Swine"
        x = 1+2
    elif(project_ID == '3VB59Bov'): #FAST Clinical (Healthy Human)
        x = 1+2
    else:
        print('Unknown project selected')
 
    return working_df

# input: valid datafile, valid output filename
def write_df_to_csv(df, outFile):
    df.to_csv(outFile, index=False)
    print('wrote csv file to: ', outFile)

# input: valid json filename ending in ".json"
# dataCategory could be "annotations", "studies", or "labels"
def df_from_json(json_file, dataCategory='annotations') -> DataFrame:
    # read in JSON file to results as a df
    results = mdai.common_utils.json_to_dataframe(json_file)

    # pull 'dataCategory' data from the df and write to csv
    if(dataCategory == 'annotations'):
        df = results['annotations']
    elif(dataCategory == 'studies'):
        df = results['studies']
    elif(dataCategory == 'labels'):
        df = results['labels']
    else:
        print('Error: no such dataCategory: ', dataCategory)

    return df

# user input handler
# important: change PROJ_ID_MAP <--> change menu order
def get_project() -> str:
    print('=============================')
    print('MD.ai project data downloader')
    print('=============================')
    print('')
    print('Enter project: ')
    print('\t1: COVID')
    print('\t2: SI Animal')
    print('\t3: SI Clinical')
    print('\t4: FAST Animal X5-1')
    print('\t5: FAST Clinical (6a Healthy Human)')

    selection = pyip.inputInt(min=1, max=5)
    return PROJ_ID_MAP[selection]


project_ID = get_project()
###mdai_client = mdai.Client(domain=DOMAIN, access_token=AUTH_TOKEN)

# Download the project data
# downloads to path given in format "mdai_philips_project_gaq3pBlV_annotations_2021-07-27-223645.json"
###mdai_client.project(project_ID, path='.',  annotations_only=True)

# find & open json file
filePath_candidates = list(Path('./').glob('mdai_philips_project_*.json'))

if(filePath_candidates): #not an empty list
    if(len(filePath_candidates) > 1): #more than one .json file here
        print('error: more than one json file here')
    else:
        jsonFilePath = filePath_candidates[0]
        print('found json file: ', jsonFilePath)
        source_df = df_from_json(jsonFilePath)

        # create output filename by stripping .json off of filepath
        outFilename = str(jsonFilePath)[:-5]
        outFilename += '.csv'

        output_df = format_df(source_df, project_ID)

        write_df_to_csv(output_df, outFilename)

        #delete downloaded json file
        ###send2trash.send2trash(jsonFilePath.name)
else:
    print('failure')

