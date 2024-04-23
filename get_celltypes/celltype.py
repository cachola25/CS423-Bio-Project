import pandas as pd

if __name__ == "__main__":
    # Read in CSV file
    data = pd.read_csv("metadata.csv")

    # Get unique cell types
    track = []
    with open("celltypes.txt", "w") as f:
        # Loop through the data and write to file if a cell type is not already in the list
        for i in range(0, len(data)):
            if data["labels.fine"][i] not in track:
                f.write(data["labels.fine"][i] + "\n")
                track.append(data["labels.fine"][i])

    name_to_id = {
        "CD3_M_121_Blood": "GSM4983132",
        "CD3_M_121_Mucosa": "GSM4983129",
        "CD3_M_122_Blood": "GSM4983130",
        "CD3_M_122_Mucosa": "GSM4983131",
        "CD3_M_124_Blood": "GSM4983132",
        "CD3_M_124_Mucosa": "GSM4983133",
        "CD3_M_125_Blood": "GSM4983134",
        "CD3_M_125_Mucosa": "GSM4983135",
        "CD3_T002_Blood": "GSM4983136",
        "CD3_T002_Inf": "GSM4983137",
        "CD3_T015_Blood": "GSM4983138",
        "CD3_T020_Blood": "GSM4983139",
        "CD3_T020_Inf": "GSM4983140",
        "CD3_T027_Blood": "GSM4983141",
        "CD3_T027_Inf": "GSM4983142",
        "HLADR_M_121_Blood": "GSM4983143",
        "HLADR_M_121_Mucosa": "GSM4983144",
        "HLADR_M_122_Blood": "GSM4983145",
        "HLADR_M_122_Mucosa": "GSM4983146",
        "HLADR_M_124_Mucosa": "GSM4983147",
        "HLADR_M_125_Blood": "GSM4983148",
        "HLADR_M_125_Mucosa": "GSM4983149",
        "HLADR_T002_Blood": "GSM4983150",
        "HLADR_T002_Inf": "GSM4983151",
        "HLADR_T015_Inf": "GSM4983152",
        "HLADR_T020_Blood": "GSM4983153",
        "HLADR_T020_Inf": "GSM4983154",
        "HLADR_T027_Blood": "GSM4983155",
        "HLADR_T027_Inf": "GSM4983156",
    }

    data["GSMID"] = data["sample"].map(name_to_id)

    data.to_csv("metadata.csv", index=False)
