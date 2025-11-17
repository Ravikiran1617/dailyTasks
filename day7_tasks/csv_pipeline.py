import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import os

class CSVDataPipeline:
    """
    Comprehensive data processing pipeline for CSV files
    Includes: loading, cleaning, validation, transformation, analysis, and export
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.df_original = None
        self.report = {
            'initial_shape': None,
            'final_shape': None,
            'missing_values': {},
            'duplicates_removed': 0,
            'outliers_detected': {},
            'transformations': []
        }
    
    def load_data(self, encoding='utf-8', sep=','):
        """Step 1: Load CSV file"""
        print("=" * 60)
        print("STEP 1: LOADING DATA")
        print("=" * 60)
        
        try:
            self.df = pd.read_csv(self.filepath, encoding=encoding, sep=sep)
            self.df_original = self.df.copy()
            self.report['initial_shape'] = self.df.shape
            
            print(f"✓ File loaded successfully: {self.filepath}")
            print(f"  Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            print(f"\nColumns: {list(self.df.columns)}")
            print(f"\nFirst 3 rows:")
            print(self.df.head(3))
            
            return True
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    def inspect_data(self):
        """Step 2: Inspect data quality"""
        print("\n" + "=" * 60)
        print("STEP 2: DATA INSPECTION")
        print("=" * 60)
        
        print("\n📊 Data Types:")
        print(self.df.dtypes)
        
        print("\n📈 Basic Statistics:")
        print(self.df.describe())
        
        print("\n🔍 Missing Values:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0])
        self.report['missing_values'] = missing_df.to_dict()
        
        print("\n🔄 Duplicate Rows:")
        duplicates = self.df.duplicated().sum()
        print(f"  Found {duplicates} duplicate rows")
        
        return self.df.info()
    
    def clean_data(self, remove_duplicates=True, handle_missing='auto'):
        """Step 3: Clean the data"""
        print("\n" + "=" * 60)
        print("STEP 3: DATA CLEANING")
        print("=" * 60)
        
        # Clean column names
        self.df.columns = self.df.columns.str.strip().str.replace(' ', '_')
        print("✓ Column names cleaned (spaces removed)")
        self.report['transformations'].append('Cleaned column names')
        
        # Remove duplicates
        if remove_duplicates:
            before = len(self.df)
            self.df = self.df.drop_duplicates()
            after = len(self.df)
            removed = before - after
            self.report['duplicates_removed'] = removed
            print(f"✓ Removed {removed} duplicate rows")
        
        # Handle missing values
        if handle_missing == 'auto':
            for col in self.df.columns:
                missing_count = self.df[col].isnull().sum()
                
                if missing_count > 0:
                    missing_pct = (missing_count / len(self.df)) * 100
                    
                    # If more than 50% missing, consider dropping the column
                    if missing_pct > 50:
                        print(f"  ⚠ Column '{col}' has {missing_pct:.1f}% missing - Consider dropping")
                    
                    # Fill numeric columns with median
                    elif self.df[col].dtype in ['int64', 'float64']:
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                        print(f"✓ Filled {missing_count} missing values in '{col}' with median")
                    
                    # Fill categorical columns with mode
                    else:
                        if len(self.df[col].mode()) > 0:
                            self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                            print(f"✓ Filled {missing_count} missing values in '{col}' with mode")
        
        # Strip whitespace from string columns
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        print(f"✓ Stripped whitespace from {len(string_cols)} text columns")
        
        return self.df
    
    def validate_data(self, validation_rules=None):
        """Step 4: Validate data against rules"""
        print("\n" + "=" * 60)
        print("STEP 4: DATA VALIDATION")
        print("=" * 60)
        
        issues = []
        
        # Check for empty strings
        for col in self.df.select_dtypes(include=['object']).columns:
            empty_count = (self.df[col] == '').sum()
            if empty_count > 0:
                issues.append(f"Column '{col}' has {empty_count} empty strings")
        
        # Check for negative values in numeric columns that shouldn't be negative
        for col in self.df.select_dtypes(include=['int64', 'float64']).columns:
            if 'price' in col.lower() or 'amount' in col.lower() or 'quantity' in col.lower():
                negative_count = (self.df[col] < 0).sum()
                if negative_count > 0:
                    issues.append(f"Column '{col}' has {negative_count} negative values")
        
        # Custom validation rules
        if validation_rules:
            for rule_name, rule_func in validation_rules.items():
                try:
                    result = rule_func(self.df)
                    if not result:
                        issues.append(f"Validation failed: {rule_name}")
                except Exception as e:
                    issues.append(f"Error in validation '{rule_name}': {e}")
        
        if issues:
            print("⚠ Validation Issues Found:")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print("✓ All validation checks passed!")
        
        return issues
    
    def detect_outliers(self, columns=None, method='iqr'):
        """Step 5: Detect outliers in numeric columns"""
        print("\n" + "=" * 60)
        print("STEP 5: OUTLIER DETECTION")
        print("=" * 60)
        
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        
        if columns:
            numeric_cols = [col for col in columns if col in numeric_cols]
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                outlier_count = len(outliers)
                
                if outlier_count > 0:
                    self.report['outliers_detected'][col] = outlier_count
                    print(f"  {col}: {outlier_count} outliers detected (range: {lower_bound:.2f} to {upper_bound:.2f})")
        
        if not self.report['outliers_detected']:
            print("✓ No outliers detected")
        
        return self.report['outliers_detected']
    
    def transform_data(self, transformations=None):
        """Step 6: Apply transformations"""
        print("\n" + "=" * 60)
        print("STEP 6: DATA TRANSFORMATION")
        print("=" * 60)
        
        if transformations:
            for transform_name, transform_func in transformations.items():
                try:
                    self.df = transform_func(self.df)
                    print(f"✓ Applied transformation: {transform_name}")
                    self.report['transformations'].append(transform_name)
                except Exception as e:
                    print(f"✗ Error in transformation '{transform_name}': {e}")
        else:
            print("  No custom transformations provided")
        
        return self.df
    
    def analyze_data(self):
        """Step 7: Perform statistical analysis"""
        print("\n" + "=" * 60)
        print("STEP 7: DATA ANALYSIS")
        print("=" * 60)
        
        analysis = {}
        
        # Analyze categorical columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        print(f"\n📊 Categorical Analysis ({len(categorical_cols)} columns):")
        
        for col in categorical_cols[:5]:  # Limit to first 5
            unique_count = self.df[col].nunique()
            top_value = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'N/A'
            print(f"  {col}: {unique_count} unique values, top: '{top_value}'")
            analysis[col] = {
                'unique': unique_count,
                'top_value': top_value
            }
        
        # Analyze numeric columns
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        print(f"\n📈 Numeric Analysis ({len(numeric_cols)} columns):")
        
        for col in numeric_cols[:5]:  # Limit to first 5
            mean_val = self.df[col].mean()
            median_val = self.df[col].median()
            std_val = self.df[col].std()
            print(f"  {col}: mean={mean_val:.2f}, median={median_val:.2f}, std={std_val:.2f}")
            analysis[col] = {
                'mean': mean_val,
                'median': median_val,
                'std': std_val
            }
        
        return analysis
    
    def visualize_data(self, output_dir='output'):
        """Step 8: Create visualizations"""
        print("\n" + "=" * 60)
        print("STEP 8: DATA VISUALIZATION")
        print("=" * 60)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create a comprehensive dashboard
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Missing values heatmap
        plt.subplot(2, 3, 1)
        missing_data = self.df.isnull().sum()
        if missing_data.sum() > 0:
            missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
            plt.barh(range(len(missing_data)), missing_data.values, color='coral')
            plt.yticks(range(len(missing_data)), missing_data.index)
            plt.xlabel('Missing Values Count')
            plt.title('Missing Values by Column')
            plt.gca().invert_yaxis()
        else:
            plt.text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
            plt.title('Missing Values by Column')
        
        # 2. Data types distribution
        plt.subplot(2, 3, 2)
        dtype_counts = self.df.dtypes.value_counts()
        plt.pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Data Types Distribution')
        
        # 3. Numeric columns distribution (first numeric column)
        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            plt.subplot(2, 3, 3)
            self.df[numeric_cols[0]].hist(bins=30, color='steelblue', edgecolor='black')
            plt.xlabel(numeric_cols[0])
            plt.ylabel('Frequency')
            plt.title(f'Distribution of {numeric_cols[0]}')
        
        # 4. Top categories (first categorical column)
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            plt.subplot(2, 3, 4)
            top_categories = self.df[categorical_cols[0]].value_counts().head(10)
            plt.barh(range(len(top_categories)), top_categories.values, color='lightgreen')
            plt.yticks(range(len(top_categories)), top_categories.index, fontsize=8)
            plt.xlabel('Count')
            plt.title(f'Top 10 {categorical_cols[0]}')
            plt.gca().invert_yaxis()
        
        # 5. Correlation heatmap (if multiple numeric columns)
        if len(numeric_cols) > 1:
            plt.subplot(2, 3, 5)
            corr_matrix = self.df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8})
            plt.title('Correlation Matrix')
        
        # 6. Processing summary
        plt.subplot(2, 3, 6)
        summary_text = f"""
Processing Summary
━━━━━━━━━━━━━━━━━━
Initial Rows: {self.report['initial_shape'][0]}
Final Rows: {len(self.df)}
Duplicates Removed: {self.report['duplicates_removed']}

Columns: {len(self.df.columns)}
Numeric: {len(numeric_cols)}
Categorical: {len(categorical_cols)}

Transformations: {len(self.report['transformations'])}
"""
        plt.text(0.1, 0.5, summary_text, fontsize=11, family='monospace', 
                verticalalignment='center')
        plt.axis('off')
        plt.title('Pipeline Summary', fontweight='bold')
        
        plt.tight_layout()
        viz_path = os.path.join(output_dir, 'data_pipeline_report.png')
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved: {viz_path}")
        plt.show()
    
    def export_data(self, output_path=None, format='csv'):
        """Step 9: Export processed data"""
        print("\n" + "=" * 60)
        print("STEP 9: EXPORTING DATA")
        print("=" * 60)
        
        if output_path is None:
            output_path = self.filepath.replace('.csv', '_processed.csv')
        
        self.report['final_shape'] = self.df.shape
        
        try:
            if format == 'csv':
                self.df.to_csv(output_path, index=False)
                print(f"✓ Data exported to: {output_path}")
            elif format == 'excel':
                output_path = output_path.replace('.csv', '.xlsx')
                self.df.to_excel(output_path, index=False)
                print(f"✓ Data exported to: {output_path}")
            elif format == 'json':
                output_path = output_path.replace('.csv', '.json')
                self.df.to_json(output_path, orient='records', indent=2)
                print(f"✓ Data exported to: {output_path}")
            
            return output_path
        except Exception as e:
            print(f"✗ Error exporting data: {e}")
            return None
    
    def generate_report(self, output_dir='output'):
        """Step 10: Generate processing report"""
        print("\n" + "=" * 60)
        print("STEP 10: GENERATING REPORT")
        print("=" * 60)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        report_path = os.path.join(output_dir, 'processing_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("CSV DATA PROCESSING PIPELINE REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source File: {self.filepath}\n\n")
            
            f.write("PROCESSING SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Initial Shape: {self.report['initial_shape']}\n")
            f.write(f"Final Shape: {self.report['final_shape']}\n")
            f.write(f"Duplicates Removed: {self.report['duplicates_removed']}\n")
            f.write(f"Transformations Applied: {len(self.report['transformations'])}\n\n")
            
            if self.report['transformations']:
                f.write("TRANSFORMATIONS:\n")
                for t in self.report['transformations']:
                    f.write(f"  • {t}\n")
                f.write("\n")
            
            if self.report['outliers_detected']:
                f.write("OUTLIERS DETECTED:\n")
                for col, count in self.report['outliers_detected'].items():
                    f.write(f"  • {col}: {count} outliers\n")
                f.write("\n")
            
            f.write("FINAL COLUMNS:\n")
            for col in self.df.columns:
                f.write(f"  • {col} ({self.df[col].dtype})\n")
        
        print(f"✓ Report saved: {report_path}")
        return report_path
    
    def run_pipeline(self, steps=None):
        """Run the complete pipeline"""
        print("\n" + "🚀" * 30)
        print("CSV DATA PROCESSING PIPELINE")
        print("🚀" * 30 + "\n")
        
        if steps is None:
            steps = ['load', 'inspect', 'clean', 'validate', 'outliers', 
                    'analyze', 'visualize', 'export', 'report']
        
        if 'load' in steps:
            if not self.load_data():
                return False
        
        if 'inspect' in steps:
            self.inspect_data()
        
        if 'clean' in steps:
            self.clean_data()
        
        if 'validate' in steps:
            self.validate_data()
        
        if 'outliers' in steps:
            self.detect_outliers()
        
        if 'analyze' in steps:
            self.analyze_data()
        
        if 'visualize' in steps:
            self.visualize_data()
        
        if 'export' in steps:
            self.export_data()
        
        if 'report' in steps:
            self.generate_report()
        
        print("\n" + "✅" * 30)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print("✅" * 30)
        
        return True


# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = CSVDataPipeline('customers.csv')
    
    # Run the complete pipeline
    pipeline.run_pipeline()
    
    # Or run specific steps
    # pipeline.run_pipeline(steps=['load', 'clean', 'export'])
    
    # Access the processed dataframe
    # processed_df = pipeline.df