# Task 3 & Task 4: Detailed Explanation

## 📊 TASK 3: A/B HYPOTHESIS TESTING

### **What is A/B Hypothesis Testing?**

A/B hypothesis testing is a statistical method to determine if there's a significant difference between two groups. In insurance analytics, we use it to validate whether certain factors (like province, zipcode, gender) actually impact risk metrics.

### **Key Concepts:**

#### **1. Null Hypothesis (H₀)**
- The assumption that there's **NO difference** between groups
- Example: "There are no risk differences across provinces"
- We try to **reject** this if we find evidence of differences

#### **2. Alternative Hypothesis (H₁)**
- The opposite: there **IS a difference**
- Example: "There ARE risk differences across provinces"

#### **3. P-value**
- Probability of observing the data if the null hypothesis is true
- **If p < 0.05**: Reject H₀ (significant difference exists)
- **If p ≥ 0.05**: Fail to reject H₀ (no significant difference)

### **Metrics to Test:**

#### **1. Claim Frequency**
- **Definition**: Proportion of policies with at least one claim
- **Formula**: `(TotalClaims > 0).sum() / total_policies`
- **Example**: If 100 out of 1000 policies had claims, frequency = 0.10 (10%)

#### **2. Claim Severity**
- **Definition**: Average claim amount when a claim occurs
- **Formula**: `TotalClaims[TotalClaims > 0].mean()`
- **Example**: If claims were [0, 5000, 0, 10000, 0], severity = (5000 + 10000) / 2 = 7500

#### **3. Loss Ratio**
- **Definition**: TotalClaims / TotalPremium
- **Interpretation**: 
  - < 1.0 = Profitable (premiums exceed claims)
  - = 1.0 = Break-even
  - > 1.0 = Loss-making (claims exceed premiums)

#### **4. Margin**
- **Definition**: TotalPremium - TotalClaims (profit)
- **Higher margin = More profitable**

### **Hypotheses to Test:**

#### **H₀₁: No risk differences across provinces**
- **Groups**: Each province (Gauteng, Western Cape, KwaZulu-Natal, etc.)
- **Metric**: Claim Frequency or Loss Ratio
- **Test**: Chi-square test (categorical) or ANOVA (continuous)
- **Business Impact**: If rejected → adjust premiums by province

#### **H₀₂: No risk differences between zip codes**
- **Groups**: Different postal codes
- **Metric**: Claim Frequency or Loss Ratio
- **Test**: Chi-square test or t-test
- **Business Impact**: If rejected → location-based pricing

#### **H₀₃: No margin difference between zip codes**
- **Groups**: Different postal codes
- **Metric**: Margin (TotalPremium - TotalClaims)
- **Test**: t-test or ANOVA
- **Business Impact**: If rejected → identify profitable vs unprofitable areas

#### **H₀₄: No risk difference between Women and Men**
- **Groups**: Gender (Male vs Female)
- **Metric**: Claim Frequency or Claim Severity
- **Test**: Chi-square test (frequency) or t-test (severity)
- **Business Impact**: If rejected → gender-based pricing (with regulatory considerations)

### **Statistical Tests to Use:**

#### **For Categorical Outcomes (Claim Frequency):**
- **Chi-square Test**: Tests if proportions differ significantly
- **Example**: 
  ```python
  from scipy.stats import chi2_contingency
  contingency_table = pd.crosstab(df['Province'], df['HasClaim'])
  chi2, p_value, dof, expected = chi2_contingency(contingency_table)
  ```

#### **For Continuous Outcomes (Claim Severity, Margin, Loss Ratio):**
- **t-test**: Compare means between two groups
- **ANOVA**: Compare means across multiple groups
- **Example**:
  ```python
  from scipy.stats import ttest_ind, f_oneway
  # Two groups
  t_stat, p_value = ttest_ind(group_a['LossRatio'], group_b['LossRatio'])
  # Multiple groups
  f_stat, p_value = f_oneway(*[group['LossRatio'] for group in groups])
  ```

### **Implementation Steps:**

1. **Select Metrics**: Choose Claim Frequency, Severity, Loss Ratio, or Margin
2. **Data Segmentation**: Split data into groups (provinces, zipcodes, gender)
3. **Statistical Testing**: Run appropriate test (chi-square, t-test, ANOVA)
4. **Interpret Results**: 
   - If p < 0.05 → Reject H₀ → Significant difference exists
   - If p ≥ 0.05 → Fail to reject H₀ → No significant difference
5. **Business Recommendations**: Translate statistical findings into actionable insights

### **Example Interpretation:**

> "We reject the null hypothesis for provinces (p < 0.01). Specifically, Gauteng exhibits a 15% higher loss ratio than the Western Cape (1.25 vs 1.10), suggesting a regional risk adjustment to our premiums may be warranted. We recommend increasing premiums in Gauteng by 10-15% to account for higher risk."

---

## 🤖 TASK 4: MACHINE LEARNING MODELING

### **What is Machine Learning Modeling?**

Building predictive models that learn patterns from historical data to predict future outcomes. In insurance, we predict:
- **Claim amounts** (how much will a claim cost?)
- **Optimal premiums** (what should we charge?)

### **Two Main Modeling Goals:**

#### **1. Claim Severity Prediction (Risk Model)**
- **Target**: `TotalClaims` (for policies with claims > 0)
- **Purpose**: Predict how much a claim will cost
- **Evaluation**: RMSE (Root Mean Squared Error), R² (R-squared)
- **Use Case**: Estimate financial liability for a policy

#### **2. Premium Optimization (Pricing Model)**
- **Target**: `CalculatedPremiumPerTerm` or custom premium calculation
- **Purpose**: Determine optimal premium to charge
- **Advanced**: Predict probability of claim × predicted severity + expenses + profit margin
- **Use Case**: Set competitive yet profitable premiums

### **Model Types:**

#### **1. Linear Regression**
- **What**: Fits a straight line through data
- **Formula**: `y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ`
- **Pros**: Simple, interpretable, fast
- **Cons**: Assumes linear relationships
- **Use**: Baseline model, interpretable predictions

#### **2. Decision Trees**
- **What**: Splits data based on feature values
- **Pros**: Easy to understand, handles non-linear relationships
- **Cons**: Can overfit, unstable
- **Use**: Feature importance, interpretability

#### **3. Random Forest**
- **What**: Ensemble of many decision trees
- **Pros**: Reduces overfitting, handles non-linear relationships, feature importance
- **Cons**: Less interpretable than single tree
- **Use**: Strong baseline, feature selection

#### **4. XGBoost (Gradient Boosting)**
- **What**: Advanced boosting algorithm
- **Pros**: Very accurate, handles complex patterns
- **Cons**: Can overfit, requires tuning
- **Use**: Best performance, competition-grade

### **Data Preparation Steps:**

#### **1. Handle Missing Data**
```python
# Strategy options:
# - Mean/Median imputation for numerical
# - Mode for categorical
# - Drop if too many missing
df['Column'].fillna(df['Column'].median(), inplace=True)
```

#### **2. Feature Engineering**
Create new features that might be predictive:
- **Vehicle Age**: Current Year - Registration Year
- **Loss Ratio**: TotalClaims / TotalPremium
- **Margin**: TotalPremium - TotalClaims
- **Has Claim**: Binary indicator (1 if claim > 0, else 0)
- **Time Features**: Year, Month, Quarter from TransactionMonth

#### **3. Encode Categorical Data**
Convert text categories to numbers:
- **One-Hot Encoding**: Create binary columns for each category
- **Label Encoding**: Assign numbers to categories
```python
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['Province', 'Gender'])
```

#### **4. Train-Test Split**
Split data to avoid overfitting:
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### **Model Evaluation Metrics:**

#### **RMSE (Root Mean Squared Error)**
- **Formula**: `√(mean((actual - predicted)²))`
- **Interpretation**: Lower is better, in same units as target
- **Example**: RMSE of 1000 means average error is ±1000

#### **R² (R-squared)**
- **Formula**: Proportion of variance explained
- **Range**: 0 to 1 (or negative if worse than baseline)
- **Interpretation**: 
  - 0.9 = Model explains 90% of variance (excellent)
  - 0.5 = Model explains 50% of variance (moderate)
  - < 0 = Model worse than simple mean

#### **MAE (Mean Absolute Error)**
- **Formula**: `mean(|actual - predicted|)`
- **Interpretation**: Average absolute error

### **Model Interpretability (SHAP/LIME):**

#### **Why Important?**
- Understand which features drive predictions
- Build trust with stakeholders
- Regulatory compliance
- Identify business insights

#### **SHAP (SHapley Additive exPlanations)**
- **What**: Explains each prediction by showing feature contributions
- **Output**: Feature importance scores
- **Example**: "Vehicle age contributes +500 to predicted claim amount"

#### **LIME (Local Interpretable Model-agnostic Explanations)**
- **What**: Explains individual predictions locally
- **Output**: Feature contributions for specific predictions

### **Implementation Workflow:**

1. **Load & Prepare Data**
   ```python
   from src.data_processing import DataProcessor
   processor = DataProcessor()
   df_processed = processor.handle_missing_values(df)
   df_features = processor.create_features(df_processed)
   ```

2. **Split Data**
   ```python
   X, y = processor.prepare_for_modeling(df_features, target_column='TotalClaims')
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
   ```

3. **Train Models**
   ```python
   from src.models import LinearRegressionModel, RandomForestModel, XGBoostModel
   
   models = {
       'Linear': LinearRegressionModel(),
       'RandomForest': RandomForestModel(n_estimators=100),
       'XGBoost': XGBoostModel(n_estimators=100)
   }
   
   for name, model in models.items():
       model.train(X_train, y_train)
   ```

4. **Evaluate Models**
   ```python
   from src.models import ModelComparator
   comparator = ModelComparator()
   for model in models.values():
       comparator.add_model(model)
   
   results = comparator.evaluate_all(X_test, y_test)
   print(results)
   ```

5. **Feature Importance**
   ```python
   import shap
   explainer = shap.TreeExplainer(best_model.model)
   shap_values = explainer.shap_values(X_test)
   shap.summary_plot(shap_values, X_test)
   ```

6. **Business Interpretation**
   - "SHAP analysis reveals that for every year older a vehicle is, the predicted claim amount increases by X Rand, holding other factors constant. This provides quantitative evidence to refine our age-based premium adjustments."

### **Key Deliverables for Task 4:**

✅ **Data preparation code** (handling missing values, feature engineering)  
✅ **Three models trained** (Linear Regression, Random Forest, XGBoost)  
✅ **Model evaluation** (RMSE, R², MAE for each model)  
✅ **Model comparison table** (which model performs best?)  
✅ **Feature importance analysis** (top 5-10 features using SHAP/LIME)  
✅ **Business interpretation** (what do the findings mean for pricing strategy?)

---

## 🎯 Summary

**Task 3** = Statistical validation of hypotheses → "Do these factors actually matter?"  
**Task 4** = Predictive modeling → "Can we predict claims/premiums accurately?"

Both tasks work together:
- Task 3 identifies **which factors** are important
- Task 4 builds **predictive models** using those factors
- Together, they inform **data-driven pricing strategy**

