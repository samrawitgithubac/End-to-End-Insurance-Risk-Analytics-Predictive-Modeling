"""
Utility functions for insurance analytics project
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


def calculate_loss_ratio(claims: pd.Series, premiums: pd.Series) -> pd.Series:
    """
    Calculate loss ratio: TotalClaims / TotalPremium
    
    Parameters:
    -----------
    claims : pd.Series
        Total claims amount
    premiums : pd.Series
        Total premium amount
    
    Returns:
    --------
    pd.Series
        Loss ratio values
    """
    return claims / premiums.replace(0, np.nan)


def calculate_claim_frequency(df: pd.DataFrame) -> float:
    """
    Calculate claim frequency: proportion of policies with at least one claim
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with TotalClaims column
    
    Returns:
    --------
    float
        Claim frequency (0-1)
    """
    return (df['TotalClaims'] > 0).mean()


def calculate_claim_severity(df: pd.DataFrame) -> float:
    """
    Calculate claim severity: average claim amount given a claim occurred
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with TotalClaims column
    
    Returns:
    --------
    float
        Average claim severity
    """
    claims_only = df[df['TotalClaims'] > 0]
    if len(claims_only) == 0:
        return 0.0
    return claims_only['TotalClaims'].mean()


def calculate_margin(premiums: pd.Series, claims: pd.Series) -> pd.Series:
    """
    Calculate margin: TotalPremium - TotalClaims (profit metric)
    
    Parameters:
    -----------
    premiums : pd.Series
        Total premium amount
    claims : pd.Series
        Total claims amount
    
    Returns:
    --------
    pd.Series
        Margin values
    """
    return premiums - claims


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load insurance data from CSV file
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe
    """
    df = pd.read_csv(filepath, low_memory=False)
    return df


def get_data_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get comprehensive data summary statistics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    
    Returns:
    --------
    pd.DataFrame
        Summary statistics
    """
    summary = pd.DataFrame({
        'dtype': df.dtypes,
        'non_null_count': df.count(),
        'null_count': df.isnull().sum(),
        'null_percentage': (df.isnull().sum() / len(df)) * 100,
        'unique_values': df.nunique()
    })
    return summary


def detect_outliers_iqr(series: pd.Series, factor: float = 1.5) -> pd.Series:
    """
    Detect outliers using Interquartile Range (IQR) method
    
    Parameters:
    -----------
    series : pd.Series
        Numerical series
    factor : float
        IQR factor (default 1.5)
    
    Returns:
    --------
    pd.Series
        Boolean series indicating outliers
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR
    return (series < lower_bound) | (series > upper_bound)

