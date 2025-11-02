"""
Predictive Analysis for Automotive Sales
Classification model to predict high/low sales based on features

Author: Son Nguyen
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare data for classification"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_path = os.path.join(project_dir, 'data', 'automotive_sales.csv')
    df = pd.read_csv(data_path)
    
    # Create target variable: High Sales (1) if Sales > median, Low Sales (0) otherwise
    sales_median = df['Sales'].median()
    df['High_Sales'] = (df['Sales'] > sales_median).astype(int)
    
    # Feature engineering
    df['Quarter'] = df['Month'].apply(lambda x: (x-1)//3 + 1)
    df['Economic_Index'] = ((df['GDP'] / 100) * 0.5 + ((100 - df['Unemployment_Rate']) / 100) * 0.5)
    
    return df

def prepare_features(df):
    """Prepare features for machine learning"""
    
    # Select features
    categorical_features = ['Vehicle_Type', 'Region', 'Season']
    numerical_features = ['Price', 'Advertising_Expenditure', 'Unemployment_Rate', 
                        'GDP', 'Quarter', 'Economic_Index', 'Year']
    
    # Encode categorical variables
    le_dict = {}
    df_encoded = df.copy()
    
    for feature in categorical_features:
        le = LabelEncoder()
        df_encoded[feature + '_encoded'] = le.fit_transform(df[feature])
        le_dict[feature] = le
    
    # Combine all features
    feature_cols = numerical_features + [f + '_encoded' for f in categorical_features]
    X = df_encoded[feature_cols]
    y = df_encoded['High_Sales']
    
    return X, y, feature_cols, le_dict

def train_models(X, y):
    """Train and evaluate multiple models"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Models to evaluate
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*60}")
        print(f"Training {name}...")
        print('='*60)
        
        # Train model
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"\nAccuracy: {accuracy:.4f}")
        print(f"ROC-AUC: {roc_auc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        results[name] = {
            'model': model,
            'scaler': scaler if name == 'Logistic Regression' else None,
            'accuracy': accuracy,
            'roc_auc': roc_auc,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'confusion_matrix': cm
        }
        
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Low Sales', 'High Sales'],
                   yticklabels=['Low Sales', 'High Sales'])
        plt.title(f'Confusion Matrix - {name}', fontsize=14, fontweight='bold')
        plt.ylabel('Actual', fontsize=12)
        plt.xlabel('Predicted', fontsize=12)
        plt.tight_layout()
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        images_dir = os.path.join(project_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        plt.savefig(os.path.join(images_dir, f'confusion_matrix_{name.lower().replace(" ", "_")}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # Plot ROC curve
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=1)
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title(f'ROC Curve - {name}', fontsize=14, fontweight='bold')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, f'roc_curve_{name.lower().replace(" ", "_")}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    # Feature importance for Random Forest
    if 'Random Forest' in results:
        rf_model = results['Random Forest']['model']
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=feature_importance, x='Importance', y='Feature', palette='viridis')
        plt.title('Feature Importance - Random Forest', fontsize=14, fontweight='bold')
        plt.xlabel('Importance', fontsize=12)
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'feature_importance.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print("\n" + "="*60)
        print("Feature Importance (Random Forest):")
        print("="*60)
        print(feature_importance.to_string(index=False))
    
    return results, X_test, y_test

def main():
    """Main execution function"""
    print("="*60)
    print("PREDICTIVE ANALYSIS: Sales Classification Model")
    print("="*60)
    
    # Load and prepare data
    df = load_and_prepare_data()
    print(f"\nDataset loaded: {df.shape}")
    print(f"High Sales ratio: {df['High_Sales'].mean():.2%}")
    
    # Prepare features
    X, y, feature_cols, le_dict = prepare_features(df)
    print(f"\nFeatures selected: {len(feature_cols)}")
    print(f"Features: {', '.join(feature_cols)}")
    
    # Train models
    results, X_test, y_test = train_models(X, y)
    
    # Select best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['accuracy'])
    print(f"\n{'='*60}")
    print(f"Best Model: {best_model_name}")
    print(f"Accuracy: {results[best_model_name]['accuracy']:.4f}")
    print(f"ROC-AUC: {results[best_model_name]['roc_auc']:.4f}")
    print('='*60)

if __name__ == "__main__":
    main()

