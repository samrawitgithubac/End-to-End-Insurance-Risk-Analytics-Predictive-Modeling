"""
Data processing and cleaning functions
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    """Class for data processing operations"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputers = {}
    
    def handle_missing_values(self, df: pd.DataFrame, 
                             strategy: str = 'median',
                             columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Handle missing values in dataframe
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        strategy : str
            Imputation strategy ('mean', 'median', 'mode', 'drop')
        columns : list, optional
            Specific columns to process
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with handled missing values
        """
        df_processed = df.copy()
        
        if columns is None:
            columns = df_processed.select_dtypes(include=[np.number]).columns.tolist()
        
        if strategy == 'drop':
            df_processed = df_processed.dropna(subset=columns)
        else:
            for col in columns:
                if df_processed[col].isnull().sum() > 0:
                    if strategy == 'mean':
                        fill_value = df_processed[col].mean()
                    elif strategy == 'median':
                        fill_value = df_processed[col].median()
                    elif strategy == 'mode':
                        fill_value = df_processed[col].mode()[0] if len(df_processed[col].mode()) > 0 else 0
                    else:
                        fill_value = 0
                    
                    df_processed[col].fillna(fill_value, inplace=True)
        
        return df_processed
    
    def encode_categorical(self, df: pd.DataFrame, 
                          columns: Optional[List[str]] = None,
                          method: str = 'onehot') -> pd.DataFrame:
        """
        Encode categorical variables
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : list, optional
            Categorical columns to encode
        method : str
            Encoding method ('onehot' or 'label')
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with encoded categorical variables
        """
        df_encoded = df.copy()
        
        if columns is None:
            columns = df_encoded.select_dtypes(include=['object']).columns.tolist()
        
        if method == 'onehot':
            df_encoded = pd.get_dummies(df_encoded, columns=columns, prefix=columns)
        elif method == 'label':
            for col in columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                df_encoded[col] = self.label_encoders[col].fit_transform(
                    df_encoded[col].astype(str)
                )
        
        return df_encoded
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create engineered features
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with new features
        """
        df_features = df.copy()
        
        # Convert TransactionMonth to datetime if not already
        if 'TransactionMonth' in df_features.columns:
            df_features['TransactionMonth'] = pd.to_datetime(
                df_features['TransactionMonth'], errors='coerce'
            )
            df_features['Year'] = df_features['TransactionMonth'].dt.year
            df_features['Month'] = df_features['TransactionMonth'].dt.month
            df_features['Quarter'] = df_features['TransactionMonth'].dt.quarter
        
        # Calculate vehicle age if RegistrationYear exists
        if 'RegistrationYear' in df_features.columns:
            current_year = df_features['TransactionMonth'].dt.year.max() if 'TransactionMonth' in df_features.columns else 2015
            df_features['VehicleAge'] = current_year - df_features['RegistrationYear']
            df_features['VehicleAge'] = df_features['VehicleAge'].clip(lower=0)
        
        # Calculate loss ratio
        if 'TotalClaims' in df_features.columns and 'TotalPremium' in df_features.columns:
            df_features['LossRatio'] = df_features['TotalClaims'] / df_features['TotalPremium'].replace(0, np.nan)
        
        # Calculate margin
        if 'TotalClaims' in df_features.columns and 'TotalPremium' in df_features.columns:
            df_features['Margin'] = df_features['TotalPremium'] - df_features['TotalClaims']
        
        # Claim indicator
        if 'TotalClaims' in df_features.columns:
            df_features['HasClaim'] = (df_features['TotalClaims'] > 0).astype(int)
        
        return df_features
    
    def prepare_for_modeling(self, df: pd.DataFrame, 
                            target_column: str,
                            exclude_columns: Optional[List[str]] = None) -> tuple:
        """
        Prepare data for machine learning modeling
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        target_column : str
            Name of target variable
        exclude_columns : list, optional
            Columns to exclude from features
        
        Returns:
        --------
        tuple
            (X, y) features and target
        """
        if exclude_columns is None:
            exclude_columns = ['PolicyID', 'UnderwrittenCoverID', 'TransactionMonth']
        
        feature_columns = [col for col in df.columns 
                          if col not in exclude_columns + [target_column]]
        
        X = df[feature_columns].select_dtypes(include=[np.number])
        y = df[target_column]
        
        # Handle missing values
        X = self.handle_missing_values(X, strategy='median')
        
        return X, y

