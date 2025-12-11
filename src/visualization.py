"""
Custom visualization functions for insurance analytics
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def plot_loss_ratio_by_category(df: pd.DataFrame, 
                                category_col: str,
                                title: str = "Loss Ratio by Category",
                                figsize: tuple = (12, 6)) -> plt.Figure:
    """
    Plot loss ratio by category (Province, Gender, VehicleType, etc.)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    category_col : str
        Categorical column to group by
    title : str
        Plot title
    figsize : tuple
        Figure size
    
    Returns:
    --------
    plt.Figure
        Matplotlib figure object
    """
    # Calculate loss ratio by category
    loss_ratio = df.groupby(category_col).apply(
        lambda x: x['TotalClaims'].sum() / x['TotalPremium'].sum() 
        if x['TotalPremium'].sum() > 0 else 0
    ).sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=figsize)
    loss_ratio.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_xlabel('Loss Ratio', fontsize=12)
    ax.set_ylabel(category_col, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='Break-even (1.0)')
    ax.legend()
    plt.tight_layout()
    
    return fig


def plot_temporal_trends(df: pd.DataFrame,
                         date_col: str = 'TransactionMonth',
                         value_col: str = 'TotalClaims',
                         title: str = "Temporal Trends") -> plt.Figure:
    """
    Plot temporal trends over time
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_col : str
        Date column name
    value_col : str
        Value column to plot
    title : str
        Plot title
    
    Returns:
    --------
    plt.Figure
        Matplotlib figure object
    """
    df_temp = df.copy()
    df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
    monthly_data = df_temp.groupby(df_temp[date_col].dt.to_period('M'))[value_col].sum()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    monthly_data.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=6)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel(value_col, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def plot_correlation_heatmap(df: pd.DataFrame,
                             columns: Optional[List[str]] = None,
                             figsize: tuple = (12, 10)) -> plt.Figure:
    """
    Plot correlation heatmap for numerical columns
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        Specific columns to include
    figsize : tuple
        Figure size
    
    Returns:
    --------
    plt.Figure
        Matplotlib figure object
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Limit to top 15 columns for readability
        if len(numeric_cols) > 15:
            # Select columns with highest variance
            variances = df[numeric_cols].var().sort_values(ascending=False)
            columns = variances.head(15).index.tolist()
        else:
            columns = numeric_cols
    
    corr_matrix = df[columns].corr()
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig


def plot_distribution_comparison(df: pd.DataFrame,
                                column: str,
                                group_by: Optional[str] = None,
                                figsize: tuple = (12, 6)) -> plt.Figure:
    """
    Plot distribution comparison (histogram or box plot)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Numerical column to plot
    group_by : str, optional
        Categorical column to group by
    figsize : tuple
        Figure size
    
    Returns:
    --------
    plt.Figure
        Matplotlib figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram
    if group_by:
        for group in df[group_by].unique():
            subset = df[df[group_by] == group]
            axes[0].hist(subset[column].dropna(), alpha=0.6, label=group, bins=30)
        axes[0].legend()
        axes[0].set_title(f'Distribution of {column} by {group_by}', fontweight='bold')
    else:
        axes[0].hist(df[column].dropna(), bins=30, color='steelblue', alpha=0.7)
        axes[0].set_title(f'Distribution of {column}', fontweight='bold')
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Frequency')
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    if group_by:
        df.boxplot(column=column, by=group_by, ax=axes[1])
        axes[1].set_title(f'{column} by {group_by}', fontweight='bold')
    else:
        axes[1].boxplot(df[column].dropna())
        axes[1].set_title(f'Box Plot of {column}', fontweight='bold')
    axes[1].set_ylabel(column)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_claim_frequency_severity(df: pd.DataFrame,
                                  group_by: str,
                                  figsize: tuple = (14, 6)) -> plt.Figure:
    """
    Plot claim frequency and severity by category
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    group_by : str
        Column to group by
    figsize : tuple
        Figure size
    
    Returns:
    --------
    plt.Figure
        Matplotlib figure object
    """
    grouped = df.groupby(group_by).agg({
        'TotalClaims': [
            lambda x: (x > 0).mean(),  # Frequency
            lambda x: x[x > 0].mean() if (x > 0).any() else 0  # Severity
        ]
    })
    grouped.columns = ['ClaimFrequency', 'ClaimSeverity']
    grouped = grouped.sort_values('ClaimFrequency', ascending=False)
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Frequency plot
    grouped['ClaimFrequency'].plot(kind='barh', ax=axes[0], color='coral')
    axes[0].set_xlabel('Claim Frequency', fontsize=11)
    axes[0].set_ylabel(group_by, fontsize=11)
    axes[0].set_title('Claim Frequency by ' + group_by, fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='x')
    
    # Severity plot
    grouped['ClaimSeverity'].plot(kind='barh', ax=axes[1], color='steelblue')
    axes[1].set_xlabel('Claim Severity (Average Claim Amount)', fontsize=11)
    axes[1].set_ylabel('')
    axes[1].set_title('Claim Severity by ' + group_by, fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    return fig

