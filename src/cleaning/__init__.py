import pandas as pd
import src.cleaning.schema_anon_data as anon_data_schema
def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Data Cleaning Assumptions:
    - Null values in brand and product type are errors in the data and are removed due to inability to see what was sold, could be fake.
        Worth investigating as all occurred in a 4 day window of October 2021.
    - Null values in supplier Id that have brand and product type kept due to ability to see what was sold. Items could be supplied by a pile or returned items, not
        enough information to be clear. Majority of these nulls occur in 2021, system change occur?
    - Rows where quantity is positive and revenue is negative are errors in data as formula for revenue does not allow for thos unless the company is paying people to buy them?
    - Order with shipping dates separated by a large number of days, such as sale_order_number 1004226145 (in the data as 1004226145.0) are kept on the assumption this is correct data
        However, this should be investigated as shipping date is almost a year later. 
    - Negative freight costs is strange but possibility is that customer pays shipping costs both ways if items are returned? This is supported by all negative freight costs have negative quantity
        therefore are refunds.
    - Rows with 0 revenue but positive profit have been removed as this is not possible. Negative profit is possible but if no money is made on the sale then there can be no profit.
    - Rows with positive quantity and a profit greater than revenue are also removed, possible that these items were given for free but questionable. Could items have been given on credit?
    """
    # Fix to correct types
    data_schema = anon_data_schema.schema
    typed_data = data_schema.enforce_schema(dataframe=dataframe)
    # Remove rows where brand or product type are null
    null_removed = typed_data.dropna(axis=0, how='any', subset=['brand', 'product_type'])
    # Remove rows where quantity > 0 but revenue < 0
    quantity_revenue_filter = ((typed_data['quantity'] >  0) & (typed_data['revenue'] < 0))
    irregular_data_removed = null_removed.loc[~quantity_revenue_filter, :]
    revenue_profit_filter = ((irregular_data_removed['quantity'] >  0) & (irregular_data_removed['revenue'] < irregular_data_removed['profit']))
    irregular_data_removed = irregular_data_removed.loc[~revenue_profit_filter, :]
    zero_revenue_filter = ((irregular_data_removed['quantity'] == 0) & (irregular_data_removed['profit'] > 0))
    irregular_data_removed = irregular_data_removed.loc[~zero_revenue_filter, :]
    outlier_profit = irregular_data_removed['profit']>150_000
    irregular_data_removed = irregular_data_removed.loc[~outlier_profit, :]

    return irregular_data_removed
