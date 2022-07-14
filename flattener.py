def type_cols(df_dtypes, filter_type):
    cols = []
    for col_name, col_type in df_dtypes:
        if col_type.startswith(filter_type):
            cols.append(col_name)
    return cols


def flatten_df(nested_df, sep='_'):
    nested_cols = type_cols(nested_df.dtypes, "struct")
    flatten_cols = [fc for fc, _ in nested_df.dtypes if fc not in nested_cols]
    for nc in nested_cols:
        for cc in nested_df.select(f"{nc}.*").columns:
            if sep is None:
                flatten_cols.append(col(f"{nc}.{cc}").alias(f"{cc}"))
            else:
                flatten_cols.append(col(f"{nc}.{cc}").alias(f"{nc}{sep}{cc}"))
    return nested_df.select(flatten_cols)


def explode_df(nested_df):
    nested_cols = type_cols(nested_df.dtypes, "array")
    exploded_df = nested_df
    for nc in nested_cols:
        exploded_df = exploded_df.withColumn(nc, explode(col(nc)))
    return exploded_df


def flatten_explode_df(nested_df):
    df = nested_df
    struct_cols = type_cols(nested_df.dtypes, "struct")
    array_cols = type_cols(nested_df.dtypes, "array")
    if struct_cols:
        df = flatten_df(df)
        return flatten_explode_df(df)
    if array_cols:
        df = explode_df(df)
        return flatten_explode_df(df)
    return df


#df = flatten_explode_df(df)
#display(df)
