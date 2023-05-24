import abc
import pandas as pd


class DataTypeConverter(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        pass

    @staticmethod
    def _remove_punctuation_and_spaces(column: pd.Series, null_values: pd.Series) -> pd.Series:
        working_column = column.astype(str).str.replace(',', '', regex=True)
        working_column = working_column.astype(str).str.replace('O', '0', regex=True)
        working_column.loc[null_values] = None
        return working_column


class IntConverter(DataTypeConverter):
    @classmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        working_column = column.copy()
        null_values = column.isna()
        if str(column.dtype) in ['object', 'string']:
            working_column = cls._remove_punctuation_and_spaces(column=working_column, null_values=null_values)

        numerical_column = pd.to_numeric(working_column)
        final_column = cls.__convert_to_integer(column=numerical_column, null_values=null_values)

        return final_column

    @staticmethod
    def __convert_to_integer(column: pd.Series, null_values: pd.Series) -> pd.Series:
        if null_values.any():
            try:
                final_column = column.astype('Int64')
            except TypeError as e:
                float_index = (column % 1) > 0
                float_values = column[float_index]
                raise TypeError(f'Column contains float values - {float_values}') from e
        else:
            final_column = column.astype(int)
        return final_column


class StringConverter(DataTypeConverter):
    @classmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        return column.astype('string')


class FloatConverter(DataTypeConverter):
    @classmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        working_column = column.copy()
        null_values = column.isna()
        if str(column.dtype) in ['object', 'string']:
            working_column = cls._remove_punctuation_and_spaces(column=working_column, null_values=null_values)

        numerical_column = pd.to_numeric(working_column)
        final_column = numerical_column.astype(float)

        return final_column


class BoolConverter(DataTypeConverter):
    @classmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        pass


class DateTimeConverter(DataTypeConverter):
    @classmethod
    def convert_column(cls, column: pd.Series, datetime_format: str = None) -> pd.Series:
        final_column = pd.to_datetime(column, format=datetime_format)
        return final_column


