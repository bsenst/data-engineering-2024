import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    # Replace uppercase letters with an underscore followed by the lowercase version
    snake_case = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    
    # Convert the whole string to lowercase
    return snake_case.lower()

@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    columns_before = df.columns
    df.columns = [camel_to_snake(col) for col in df.columns]
    columns_after = df.columns

    print(set(columns_before).difference(set(columns_after)))
    print(df.vendor_id.unique())

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_vendorid(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert all(df['vendor_id'].isin(df['vendor_id'].unique())), "Assertion Error: vendor_id contains values not in the existing set"

@test
def test_passengercount(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # Assertion 2: passenger_count is greater than 0
    assert all(df['passenger_count'] > 0), "Assertion Error: passenger_count should be greater than 0"

@test
def test_tripdistance(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # Assertion 3: trip_distance is greater than 0
    assert all(df['trip_distance'] > 0), "Assertion Error: trip_distance should be greater than 0"
