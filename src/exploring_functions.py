import numpy as np
import pandas as pd


def column_type(df):
    '''
    This function gives you information about the column type of a datframe. You have to give it a DataFrame and it returns nothing
    
    Parameters:
    df (DataFrame): DataFrame 
    '''
    integer_columns = df.select_dtypes(include=['int64']).columns 
    float_columns = df.select_dtypes(include=['float64']).columns 
    object_columns = df.select_dtypes(include=['object']).columns 
    print('El número de columnas enteras es:', len(integer_columns))
    print('El número de columnas float es:', len(float_columns))
    print('El número de columnas object es:', len(object_columns))


def null_sum(df):
    '''
    This function gives you information about the nan data in a dataframe. You have to give it a DataFrame and it returns another dataframe with nan information
    
    Parameters:
    df (DataFrame): DataFrame 

    Returns:
    DataFrame: Dataframe with nan information
    '''

    nullsum = df.isnull().sum()
    nulltotal = (df.isnull().sum()/df.isnull().count()*100)
    tt = pd.concat([nullsum, nulltotal], axis=1, keys=['null_count', 'null_percent'])
    types = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return np.transpose(tt)


def donwcast_df(df, objet_to_category=False, verbose=1):
    '''
    This function takes a dataframe and gives another dataframe with the same information but with the column type combination that uses less memory. 

    Parameters:
    df (DataFrame): DataFrame to reduce the space it occupies.

    object_to_category (boolean): option to transform object columns to category ones.

    verbose (int): option to modify the amount of prints with information about the data transformation. It goes from 0 to 2.

    Returns:
    DataFrame: Dataframe with column type combination that uses less memory. 
    '''
    if verbose >= 1:
        # Print initial state
        start_mem_usg = df.memory_usage().sum() / 1024**2 
        print("Memory usage of properties dataframe is :",start_mem_usg," MB")

    if objet_to_category:
        for e in df.select_dtypes('object').columns:

            if verbose == 2:
                # Print current column type
                print("******************************")
                print("Column: ",e)
                print("dtype before: object")
        
            df[e]=df[e].astype('category')

            if verbose == 2:
            # Print new column type
                print("dtype after: ",df[e].dtype)
                print("******************************")

    for e in df.select_dtypes('integer').columns:

        if verbose == 2:
            # Print current column type
            print("******************************")
            print("Column: ",e)
            print("dtype before: category")

        df[e]=pd.to_numeric(df[e], downcast='integer')

        if verbose == 2:
            # Print new column type
            print("dtype after: ",df[e].dtype)
            print("******************************")

    for e in df.select_dtypes('float').columns:
        
        if verbose == 2:
            # Print current column type
            print("******************************")
            print("Column: ",e)
            print("dtype before: float")

        df[e]=pd.to_numeric(df[e], downcast='float')

        if verbose == 2:
            # Print new column type
            print("dtype after: ",df[e].dtype)
            print("******************************")

    if verbose >= 1:
        # Print final result
        print("___MEMORY USAGE AFTER COMPLETION:___")
        mem_usg = df.memory_usage().sum() / 1024**2 
        print("Memory usage is: ",mem_usg," MB")
        print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")

    return df
