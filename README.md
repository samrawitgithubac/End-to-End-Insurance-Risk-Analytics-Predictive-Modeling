# End-to-End Insurance Risk Analytics & Predictive Modeling

## Project Title and Description

**AlphaCare Insurance Solutions (ACIS) - Risk Analytics & Predictive Modeling Project**

This project is a comprehensive data analytics initiative focused on developing cutting-edge risk and predictive analytics for car insurance planning and marketing in South Africa. The primary objective is to analyze historical insurance claim data to optimize marketing strategies and discover "low-risk" customer segments, enabling premium reductions to attract new clients.

### Key Objectives

- **Risk Segmentation**: Identify low-risk customer segments through statistical analysis
- **Premium Optimization**: Build predictive models to optimize insurance premiums
- **Hypothesis Testing**: Validate key hypotheses about risk drivers across provinces, zip codes, and demographics
- **Predictive Modeling**: Develop machine learning models for claim severity prediction and premium optimization
- **Business Intelligence**: Provide actionable insights to tailor insurance products effectively

### Project Scope

The analysis covers:
- **Exploratory Data Analysis (EDA)**: Comprehensive data exploration and visualization
- **A/B Hypothesis Testing**: Statistical validation of risk differences across various segments
- **Statistical Modeling**: Linear regression models for claim prediction by zipcode
- **Machine Learning**: Advanced models (Random Forest, XGBoost) for premium optimization
- **Model Interpretability**: SHAP/LIME analysis to understand feature importance

---

## Installation and Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd End-to-End-Insurance-Risk-Analytics-Predictive-Modeling
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If requirements.txt doesn't exist, install core packages manually:**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost jupyter notebook dvc shap lime scipy statsmodels
```

### Step 4: Install DVC (Data Version Control)

```bash
pip install dvc
dvc init
```

### Step 5: Set Up Data

1. Download the insurance dataset (February 2014 to August 2015)
2. Place the data file(s) in the `data/` directory
3. Track data with DVC:
   ```bash
   dvc add data/<your-data-file>.csv
   git add data/<your-data-file>.csv.dvc data/.gitignore
   ```

### Step 6: Launch Jupyter Notebook

```bash
jupyter notebook
```

Navigate to `notebooks/eda.ipynb` to start your analysis.

---

## Project Structure

```
End-to-End-Insurance-Risk-Analytics-Predictive-Modeling/
│
├── data/                          # Data directory (tracked with DVC)
│   ├── .gitignore                 # Ignore large data files in Git
│   └── <insurance-data>.csv      # Historical insurance claim data
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── eda.ipynb                  # Exploratory Data Analysis
│   ├── hypothesis_testing.ipynb  # A/B hypothesis testing (Task 3)
│   └── modeling.ipynb            # Machine learning models (Task 4)
│
├── src/                           # Source code modules
│   ├── __init__.py
│   ├── utils.py                  # Utility functions
│   ├── data_processing.py        # Data cleaning and preprocessing
│   ├── visualization.py           # Custom visualization functions
│   └── models.py                  # Model training and evaluation
│
├── reports/                       # Generated reports and visualizations
│   ├── interim_report.md         # Interim submission report
│   ├── final_report.md           # Final submission report
│   └── figures/                  # Saved plots and charts
│
├── .github/                       # GitHub Actions CI/CD
│   └── workflows/
│       └── ci.yml                # Continuous Integration workflow
│
├── .dvc/                          # DVC configuration and cache
│
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── LICENSE                        # License file (if applicable)
```

### Directory Descriptions

- **`data/`**: Contains all datasets. Files are tracked with DVC to manage large files efficiently.
- **`notebooks/`**: Jupyter notebooks for interactive analysis and exploration.
- **`src/`**: Reusable Python modules for data processing, modeling, and utilities.
- **`reports/`**: Documentation, reports, and saved visualizations.
- **`.github/workflows/`**: CI/CD pipeline configuration for automated testing and validation.

---

## How to Run the Code

### Running Exploratory Data Analysis (Task 1)

1. **Open Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Navigate to EDA Notebook:**
   - Open `notebooks/eda.ipynb`
   - Execute cells sequentially or run all cells

3. **Expected Outputs:**
   - Data summary statistics
   - Missing value analysis
   - Distribution plots
   - Correlation matrices
   - Geographic and temporal trend visualizations
   - Loss ratio calculations

### Running Hypothesis Testing (Task 3)

1. **Open the Hypothesis Testing Notebook:**
   ```bash
   jupyter notebook notebooks/hypothesis_testing.ipynb
   ```

2. **Tests to Execute:**
   - Province risk differences
   - Zipcode risk differences
   - Zipcode margin differences
   - Gender risk differences

### Running Predictive Models (Task 4)

1. **Open the Modeling Notebook:**
   ```bash
   jupyter notebook notebooks/modeling.ipynb
   ```

2. **Models to Run:**
   - Linear Regression (by zipcode)
   - Random Forest
   - XGBoost
   - Model evaluation and comparison
   - SHAP/LIME interpretability analysis

### Running Python Scripts

If you have standalone Python scripts in `src/`:

```bash
python src/data_processing.py
python src/models.py
```

### Using DVC for Data Management

**Add new data version:**
```bash
dvc add data/new_data.csv
git add data/new_data.csv.dvc
git commit -m "Add new data version"
dvc push
```

**Pull data:**
```bash
dvc pull
```

---

## Data Source Information

### Dataset Overview

- **Source**: Historical insurance claim data
- **Time Period**: February 2014 to August 2015 (18 months)
- **Location**: South Africa
- **Industry**: Car Insurance

### Data Structure

The dataset contains the following column categories:

#### Insurance Policy Information
- `UnderwrittenCoverID`: Unique identifier for the cover
- `PolicyID`: Unique policy identifier
- `TransactionMonth`: Date of the transaction

#### Client Information
- `IsVATRegistered`: VAT registration status
- `Citizenship`: Citizenship information
- `LegalType`: Legal entity type
- `Title`: Client title
- `Language`: Preferred language
- `Bank`: Banking institution
- `AccountType`: Type of account
- `MaritalStatus`: Marital status
- `Gender`: Client gender

#### Client Location
- `Country`: Country of residence
- `Province`: South African province
- `PostalCode`: Postal/ZIP code
- `MainCrestaZone`: Main CRESTA zone classification
- `SubCrestaZone`: Sub CRESTA zone classification

#### Vehicle Information
- `ItemType`: Type of item insured
- `Mmcode`: Make/model code
- `VehicleType`: Type of vehicle
- `RegistrationYear`: Year of vehicle registration
- `Make`: Vehicle manufacturer
- `Model`: Vehicle model
- `Cylinders`: Number of cylinders
- `Cubiccapacity`: Engine capacity
- `Kilowatts`: Engine power
- `Bodytype`: Vehicle body type
- `NumberOfDoors`: Number of doors
- `VehicleIntroDate`: Vehicle introduction date
- `CustomValueEstimate`: Estimated custom value
- `AlarmImmobiliser`: Security alarm/immobilizer status
- `TrackingDevice`: GPS tracking device status
- `CapitalOutstanding`: Outstanding capital
- `NewVehicle`: New vehicle indicator
- `WrittenOff`: Written-off status
- `Rebuilt`: Rebuilt vehicle indicator
- `Converted`: Converted vehicle indicator
- `CrossBorder`: Cross-border usage indicator
- `NumberOfVehiclesInFleet`: Fleet size

#### Insurance Plan Details
- `SumInsured`: Total sum insured
- `TermFrequency`: Premium payment frequency
- `CalculatedPremiumPerTerm`: Calculated premium per term
- `ExcessSelected`: Selected excess amount
- `CoverCategory`: Category of coverage
- `CoverType`: Type of coverage
- `CoverGroup`: Coverage group
- `Section`: Policy section
- `Product`: Insurance product type
- `StatutoryClass`: Statutory classification
- `StatutoryRiskType`: Statutory risk type

#### Financial Metrics
- `TotalPremium`: Total premium amount (target for pricing model)
- `TotalClaims`: Total claims amount (target for risk model)

### Key Metrics to Calculate

- **Loss Ratio**: `TotalClaims / TotalPremium`
- **Claim Frequency**: Proportion of policies with at least one claim
- **Claim Severity**: Average claim amount (given a claim occurred)
- **Margin**: `TotalPremium - TotalClaims` (profit metric)

### Data Access

The dataset should be placed in the `data/` directory and tracked using DVC. Ensure you have proper access rights to the data before proceeding with analysis.

### Data Privacy and Compliance

- All data handling must comply with data protection regulations
- Sensitive customer information should be anonymized if required
- Data versioning through DVC ensures reproducibility and auditability

---

## Key Dates and Deliverables

### Interim Submission (Sunday, 07 Dec 2025 - 8:00 PM UTC)
- GitHub link to main branch with merged work from Task 1 and Task 2
- Interim report covering EDA findings and DVC setup

### Final Submission (Tuesday, 09 Dec 2025 - 8:00 PM UTC)
- GitHub link to main branch with all completed tasks
- Final report in Medium blog post format
- Complete analysis including EDA, hypothesis testing, and modeling results

---

## Contributing

This is a learning project for the Week 3 challenge. Contributions should follow best practices:

- Use descriptive commit messages
- Create feature branches for each task
- Submit pull requests for code review
- Follow Python PEP 8 style guidelines
- Document code and findings thoroughly

---

## License

[Specify your license here, if applicable]

## References

- [Insurance Analytics Resources](https://www.fsrao.ca/media/11501/download)
- [A/B Testing Guide](https://www.optimizely.com/insights/blog/why-an-experiment-without-a-hypothesis-is-dead-on-arrival/)
- [DVC Documentation](https://dvc.org/doc/user-guide)
- [Statistical Modeling](https://www.heavy.ai/technical-glossary/statistical-modeling)
- [Git Version Control](https://www.atlassian.com/git/tutorials/what-is-version-control)

---

**Last Updated**: December 2025
