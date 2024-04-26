
import pandas as pd

# Map the sample names to the GSM ID and add it to the metadata file
if __name__ == '__main__':

    data = pd.read_csv('../R/metadata.csv')

    # Dictionary to map the sample names to the GSM ID
    name_to_id = {
            "CD3_M_121_Mucosa": "GSM4983128",
            "CD3_M_121_Blood": "GSM4983132",
            
            "CD3_M_122_Mucosa": "GSM4983129",
            "CD3_M_122_Blood": "GSM4983133",
            
            "CD3_M_124_Mucosa": "GSM4983130",
            "CD3_M_124_Blood": "GSM4983134",
            
            "CD3_M_125_Mucosa": "GSM4983131",
            "CD3_M_125_Blood": "GSM4983135",
            
            "CD3_T002_Inf": "GSM4983144",
            "CD3_T002_Blood": "GSM4983148",
            
            "CD3_T015_Blood": "GSM4983149",
            
            "CD3_T020_Inf": "GSM4983146",
            "CD3_T020_Blood": "GSM4983150",
            
            "CD3_T027_Inf": "GSM4983147",
            "CD3_T027_Blood": "GSM4983151",
            
            "HLADR_M_121_Mucosa": "GSM4983136",
            "HLADR_M_121_Blood": "GSM4983140",
            
            "HLADR_M_122_Mucosa": "GSM4983137",
            "HLADR_M_122_Blood": "GSM4983141",
            
            "HLADR_M_124_Mucosa": "GSM4983138",
            
            "HLADR_M_125_Mucosa": "GSM4983139",
            "HLADR_M_125_Blood": "GSM4983143",
            
            "HLADR_T002_Inf": "GSM4983152",
            "HLADR_T002_Blood": "GSM4983156",
            
            "HLADR_T015_Inf": "GSM4983153",
            
            "HLADR_T020_Inf": "GSM4983154",
            "HLADR_T020_Blood": "GSM4983158",
            
            "HLADR_T027_Inf": "GSM4983155",
            "HLADR_T027_Blood": "GSM4983159",
        }

    # Add the GSM ID to the metadata file
    data['GSMID'] = data['sample'].map(name_to_id)
    data.to_csv('../R/metadata.csv', index=False)