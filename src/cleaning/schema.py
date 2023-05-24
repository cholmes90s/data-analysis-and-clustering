import pandas as pd
import functools
from src.cleaning import type_converters


class Schema:
    required_keys = {'data_type', 'nullable'}
    type_mapping = {
        'integer': type_converters.IntConverter,
        'string': type_converters.StringConverter,
        'float': type_converters.FloatConverter,
        'decimal': type_converters.FloatConverter,
        'datetime': type_converters.DateTimeConverter
    }

    def __init__(self, schema_dictionary: dict = None):
        self.__schema_dictionary = schema_dictionary
        self.validate_schema(schema_dictionary=schema_dictionary)
        self.renaming_dict = self.__create_renaming_dict(schema_dictionary=schema_dictionary)
        self.non_nullable_columns = self.__nullable_columns(schema_dictionary=schema_dictionary)
        self.datatype_enforcer = self.build_datatype_enforcer(schema_dictionary=schema_dictionary)

    def __validate_schema_keys(self, column_name: str, column_parameters: dict) -> None:
        diff_to_required = self.required_keys.difference(column_parameters)
        if diff_to_required:
            raise KeyError(f'All columns must contain the following keys {self.required_keys} - column "{column_name}" is missing "{diff_to_required}"')
        
    @staticmethod
    def __validate_datetime_requirements(column_name: str, column_parameters: dict):
        if column_parameters['data_type'].lower() == 'datetime':
            assert 'datetime_format' in column_parameters.keys(), \
                f'If data_type is datetime, datetime_format must be specified - column {column_name} has no datetime_format attribute'

    @staticmethod
    def __create_renaming_dict(schema_dictionary: dict) -> dict:
        renaming_dict = dict()
        for column_name, column_parameters in schema_dictionary.items():
            try:
                renaming_dict.setdefault(column_name, column_parameters['new_column_name'])
            except KeyError as e:
                renaming_dict.setdefault(column_name, column_name)
        return renaming_dict

    @staticmethod
    def __nullable_columns(schema_dictionary: dict) -> list:
        nullables = list()
        for column_name, column_parameters in schema_dictionary.items():
            if not column_parameters['nullable']:
                nullables.append(column_name)
        return nullables

    def __null_check(self, dataframe: pd.DataFrame) -> None:
        non_nullable = dataframe[self.non_nullable_columns]
        nulls = non_nullable.isna()
        if nulls.any().any():
            raise ValueError(f'Non Nullable columns contain nulls: \nColumns:{nulls.columns[nulls.any()].tolist()} \nRows: {list(nulls.loc[nulls.any(axis=1), :].index)} \n Note, row indexs are one less for headers and one less for being 0 indexed')

    def build_datatype_enforcer(self, schema_dictionary: dict):
        datatype_enforcer = dict()
        for column_name, column_parameters in schema_dictionary.items():
            data_type = column_parameters['data_type'].lower()
            if data_type == 'datetime':
                enforcer = functools.partial(self.type_mapping[data_type].convert_column, **{'datetime_format': column_parameters['datetime_format']})
            else:
                enforcer = self.type_mapping[data_type].convert_column

            datatype_enforcer.setdefault(column_name, enforcer)

        return datatype_enforcer

    def enforce_datatypes(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        working_dataframe = dataframe.copy()
        for column_name, enforcer in self.datatype_enforcer.items():
            working_dataframe = working_dataframe.assign(**{column_name: enforcer(working_dataframe[column_name])})
        return working_dataframe

    def enforce_schema(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        self.__null_check(dataframe=dataframe)
        enforced_datatypes = self.enforce_datatypes(dataframe=dataframe)
        renamed_columns = enforced_datatypes.rename(columns=self.renaming_dict)
        return renamed_columns

    def required_columns(self):
        return tuple(self.__schema_dictionary.keys())

    def validate_schema(self, schema_dictionary: dict) -> None:
        for column_name, parameters in schema_dictionary.items():
            self.__validate_schema_keys(column_name=column_name, column_parameters=parameters)
            self.__validate_datetime_requirements(column_name=column_name, column_parameters=parameters)