"""
Machine learning models for insurance analytics
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')


class InsuranceModel:
    """Base class for insurance prediction models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.feature_importance_ = None
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train the model"""
        raise NotImplementedError
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model must be trained first")
        return self.model.predict(X)
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        
        metrics = {
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'MAE': mean_absolute_error(y_test, y_pred),
            'R2': r2_score(y_test, y_pred),
            'Mean_Error': np.mean(y_test - y_pred)
        }
        return metrics


class LinearRegressionModel(InsuranceModel):
    """Linear Regression model"""
    
    def __init__(self):
        super().__init__("Linear Regression")
        self.model = LinearRegression()
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train linear regression model"""
        self.model.fit(X_train, y_train)
        # Feature importance for linear regression (coefficients)
        self.feature_importance_ = pd.Series(
            np.abs(self.model.coef_),
            index=X_train.columns
        ).sort_values(ascending=False)


class RandomForestModel(InsuranceModel):
    """Random Forest model"""
    
    def __init__(self, n_estimators: int = 100, max_depth: Optional[int] = None,
                 random_state: int = 42):
        super().__init__("Random Forest")
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train random forest model"""
        self.model.fit(X_train, y_train)
        # Feature importance
        self.feature_importance_ = pd.Series(
            self.model.feature_importances_,
            index=X_train.columns
        ).sort_values(ascending=False)


class XGBoostModel(InsuranceModel):
    """XGBoost model"""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 6,
                 learning_rate: float = 0.1, random_state: int = 42):
        super().__init__("XGBoost")
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=-1
        )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train XGBoost model"""
        self.model.fit(X_train, y_train)
        # Feature importance
        self.feature_importance_ = pd.Series(
            self.model.feature_importances_,
            index=X_train.columns
        ).sort_values(ascending=False)


class ModelComparator:
    """Compare multiple models"""
    
    def __init__(self):
        self.models: Dict[str, InsuranceModel] = {}
        self.results: Dict[str, Dict[str, float]] = {}
    
    def add_model(self, model: InsuranceModel):
        """Add a model to compare"""
        self.models[model.model_name] = model
    
    def train_all(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Train all models"""
        for model in self.models.values():
            model.train(X_train, y_train)
    
    def evaluate_all(self, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
        """Evaluate all models and return comparison"""
        results = []
        for name, model in self.models.items():
            metrics = model.evaluate(X_test, y_test)
            metrics['Model'] = name
            results.append(metrics)
            self.results[name] = metrics
        
        return pd.DataFrame(results)
    
    def get_feature_importance(self, top_n: int = 10) -> Dict[str, pd.Series]:
        """Get feature importance for all models"""
        importance_dict = {}
        for name, model in self.models.items():
            if model.feature_importance_ is not None:
                importance_dict[name] = model.feature_importance_.head(top_n)
        return importance_dict


def train_zipcode_models(df: pd.DataFrame, 
                         target_col: str = 'TotalClaims',
                         feature_cols: Optional[List[str]] = None) -> Dict[str, InsuranceModel]:
    """
    Train separate linear regression models for each zipcode
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    target_col : str
        Target variable column
    feature_cols : list, optional
        Feature columns to use
    
    Returns:
    --------
    dict
        Dictionary of zipcode -> model
    """
    if 'PostalCode' not in df.columns:
        raise ValueError("PostalCode column not found in dataframe")
    
    zipcode_models = {}
    
    for zipcode in df['PostalCode'].unique():
        zipcode_data = df[df['PostalCode'] == zipcode].copy()
        
        if len(zipcode_data) < 10:  # Skip if too few samples
            continue
        
        if feature_cols is None:
            # Use numerical columns as features
            feature_cols = zipcode_data.select_dtypes(include=[np.number]).columns.tolist()
            feature_cols = [col for col in feature_cols 
                          if col not in [target_col, 'PolicyID', 'UnderwrittenCoverID']]
        
        X = zipcode_data[feature_cols]
        y = zipcode_data[target_col]
        
        # Remove columns with all NaN
        X = X.dropna(axis=1, how='all')
        
        if len(X.columns) == 0:
            continue
        
        # Fill remaining NaN
        X = X.fillna(X.median())
        
        try:
            model = LinearRegressionModel()
            model.train(X, y)
            zipcode_models[str(zipcode)] = model
        except Exception as e:
            print(f"Error training model for zipcode {zipcode}: {e}")
            continue
    
    return zipcode_models

