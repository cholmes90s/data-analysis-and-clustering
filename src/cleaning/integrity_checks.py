import pandas as pd

def mapping_check(dataframe: pd.DataFrame, groupby_column: str, check_column: str, number_unique_values: int = 1) -> None:
    unique_counters = dataframe.groupby(groupby_column)[check_column].nunique()
    exceeding_filter = unique_counters > number_unique_values
    values_exceeding = unique_counters[exceeding_filter]
    if values_exceeding.any():
        return values_exceeding
    else:
        return None
