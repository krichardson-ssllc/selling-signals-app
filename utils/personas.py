import pandas as pd

def assign_persona(sector):
    if pd.isna(sector):
        return "Operations Leader"

    sector = sector.lower()

    if "therapeutic" in sector or "drug" in sector:
        return "Head of R&D / VP Research"
    if "cdmo" in sector or "manufacturing" in sector:
        return "Manufacturing Director / Plant Manager"
    if "diagnostic" in sector:
        return "VP Operations / Lab Director"
    if "genomic" in sector or "proteomic" in sector:
        return "Director of Genomics / Platform Lead"
    if "vaccine" in sector:
        return "Process Development / CMC Lead"

    return "Lab Operations / Scientific Director"
