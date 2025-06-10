import os
import pandas as pd
import io
import base64
import warnings

# Helper function to safely import visualization libraries
def get_visualization_imports():
    """Safely import matplotlib and seaborn, return dummy functions if not available"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        import numpy as np
        return plt, sns, np, FigureCanvas
    except ImportError:
        warnings.warn("Matplotlib or Seaborn not available. Using dummy chart generation.")
        
        # Define dummy functions/classes to prevent errors
        class DummyPlt:
            @staticmethod
            def figure(*args, **kwargs):
                return DummyFig()
                
            @staticmethod
            def close(*args, **kwargs):
                pass
                
            @staticmethod
            def title(*args, **kwargs):
                pass
                
            @staticmethod
            def xlabel(*args, **kwargs):
                pass
                
            @staticmethod
            def ylabel(*args, **kwargs):
                pass
                
            @staticmethod
            def grid(*args, **kwargs):
                pass
                
            @staticmethod
            def xticks(*args, **kwargs):
                pass
                
            @staticmethod
            def tight_layout(*args, **kwargs):
                pass
        
        class DummyFig:
            def savefig(self, *args, **kwargs):
                # Create an empty file at the specified path
                path = args[0]
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    f.write('')
        
        class DummySNS:
            @staticmethod
            def histplot(*args, **kwargs):
                pass
                
            @staticmethod
            def boxplot(*args, **kwargs):
                pass
                
            @staticmethod
            def heatmap(*args, **kwargs):
                pass
                
            @staticmethod
            def barplot(*args, **kwargs):
                pass
                
            @staticmethod
            def regplot(*args, **kwargs):
                pass
        
        class DummyNP:
            @staticmethod
            def random(seed):
                return DummyNP()
                
            @staticmethod
            def choice(*args, **kwargs):
                return []
                
            @staticmethod
            def normal(*args, **kwargs):
                return []
                
            @staticmethod
            def triu(*args, **kwargs):
                return []
        
        class DummyFigureCanvas:
            def __init__(self, fig):
                pass
                
            @staticmethod
            def print_png(*args, **kwargs):
                pass
        
        return DummyPlt(), DummySNS(), DummyNP(), DummyFigureCanvas

# Import the visualization libraries
plt, sns, np, FigureCanvas = get_visualization_imports()

def ensure_dir(directory):
    """Ensure that a directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_charts():
    """Generate all the charts needed for the visualization page"""
    # Create directories if they don't exist
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    images_dir = os.path.join(static_dir, 'images')
    charts_dir = os.path.join(images_dir, 'charts')
    
    ensure_dir(static_dir)
    ensure_dir(images_dir)
    ensure_dir(charts_dir)
    
    # Load the dataset - try different possible locations
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'artifact', 'raw.csv'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebook', 'data', 'stud.csv'),
        'artifact/raw.csv',
        'notebook/data/stud.csv'
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading data from: {path}")
            df = pd.read_csv(path)
            break
    
    if df is None:
        print("Warning: Could not find dataset. Using sample data.")
        # Create sample data if file not found
        np.random.seed(42)
        df = pd.DataFrame({
            'gender': np.random.choice(['male', 'female'], size=1000),
            'race_ethnicity': np.random.choice(['group A', 'group B', 'group C', 'group D', 'group E'], size=1000),
            'parental_level_of_education': np.random.choice(["bachelor's degree", "some college", "master's degree", "associate's degree", "high school", "some high school"], size=1000),
            'lunch': np.random.choice(['standard', 'free/reduced'], size=1000),
            'test_preparation_course': np.random.choice(['none', 'completed'], size=1000),
            'math_score': np.random.normal(70, 15, size=1000).clip(0, 100).astype(int),
            'reading_score': np.random.normal(70, 15, size=1000).clip(0, 100).astype(int),
            'writing_score': np.random.normal(70, 15, size=1000).clip(0, 100).astype(int)
        })
    
    # Generate and save charts
    charts_info = []
    
    # Chart 1: Distribution of Math Scores
    plt.figure(figsize=(10, 6))
    sns.histplot(df['math_score'], kde=True, color='#3498db')
    plt.title('Distribution of Math Scores', fontsize=16)
    plt.xlabel('Math Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(charts_dir, 'math_score_distribution.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Distribution of Math Scores',
        'filename': 'math_score_distribution.png',
        'description': 'This chart shows the distribution of math scores across all students. The bell-shaped curve indicates a normal distribution with most students scoring between 60-80.'
    })
    
    # Chart 2: Math Score by Gender
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='gender', y='math_score', data=df, palette=['#3498db', '#e74c3c'])
    plt.title('Math Scores by Gender', fontsize=16)
    plt.xlabel('Gender', fontsize=12)
    plt.ylabel('Math Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(charts_dir, 'math_score_by_gender.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Math Scores by Gender',
        'filename': 'math_score_by_gender.png',
        'description': 'This box plot compares math scores between male and female students. The median scores and distributions show gender-based performance differences.'
    })
    
    # Chart 3: Math Score by Test Preparation
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='test_preparation_course', y='math_score', data=df, palette=['#3498db', '#2ecc71'])
    plt.title('Math Scores by Test Preparation', fontsize=16)
    plt.xlabel('Test Preparation Course', fontsize=12)
    plt.ylabel('Math Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(charts_dir, 'math_score_by_test_prep.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Math Scores by Test Preparation',
        'filename': 'math_score_by_test_prep.png',
        'description': 'Students who completed the test preparation course tend to have higher math scores than those who did not complete any preparation.'
    })
    
    # Chart 4: Math Score by Parental Education
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='parental_level_of_education', y='math_score', data=df, palette='viridis')
    plt.title('Math Scores by Parental Education', fontsize=16)
    plt.xlabel('Parental Level of Education', fontsize=12)
    plt.ylabel('Math Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'math_score_by_parent_education.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Math Scores by Parental Education',
        'filename': 'math_score_by_parent_education.png',
        'description': 'This chart shows how parental education level affects student math performance. Higher education levels generally correlate with better student performance.'
    })
    
    # Chart 5: Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    correlation = df[numeric_cols].corr()
    mask = np.triu(correlation)
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', mask=mask)
    plt.title('Correlation Between Scores', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'correlation_heatmap.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Correlation Between Scores',
        'filename': 'correlation_heatmap.png',
        'description': 'This heatmap shows the correlation between math, reading, and writing scores. Strong positive correlations indicate that students who do well in one subject tend to do well in others.'
    })
    
    # Chart 6: Math Score by Lunch Type
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='lunch', y='math_score', data=df, palette=['#9b59b6', '#f1c40f'])
    plt.title('Math Scores by Lunch Type', fontsize=16)
    plt.xlabel('Lunch Type', fontsize=12)
    plt.ylabel('Math Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(charts_dir, 'math_score_by_lunch.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Math Scores by Lunch Type',
        'filename': 'math_score_by_lunch.png',
        'description': 'Students with standard lunch tend to have higher math scores compared to those with free/reduced lunch, which may indicate socioeconomic factors.'
    })
    
    # Chart 7: Average Scores by Race/Ethnicity
    plt.figure(figsize=(12, 6))
    race_scores = df.groupby('race_ethnicity')[['math_score', 'reading_score', 'writing_score']].mean().reset_index()
    race_scores_melted = pd.melt(race_scores, id_vars='race_ethnicity', var_name='Subject', value_name='Average Score')
    
    sns.barplot(x='race_ethnicity', y='Average Score', hue='Subject', data=race_scores_melted, palette='Set2')
    plt.title('Average Scores by Race/Ethnicity', fontsize=16)
    plt.xlabel('Race/Ethnicity Group', fontsize=12)
    plt.ylabel('Average Score', fontsize=12)
    plt.legend(title='Subject')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'average_scores_by_race.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Average Scores by Race/Ethnicity',
        'filename': 'average_scores_by_race.png',
        'description': 'This chart compares the average math, reading, and writing scores across different racial/ethnic groups, highlighting performance variations between groups.'
    })
    
    # Chart 8: Score Scatter Plot with Regression Line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='reading_score', y='math_score', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Math Score vs. Reading Score', fontsize=16)
    plt.xlabel('Reading Score', fontsize=12)
    plt.ylabel('Math Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(charts_dir, 'math_vs_reading.png'), bbox_inches='tight')
    plt.close()
    
    charts_info.append({
        'title': 'Math Score vs. Reading Score',
        'filename': 'math_vs_reading.png',
        'description': 'This scatter plot with regression line shows the relationship between reading and math scores. The positive correlation suggests that students with good reading skills tend to perform well in math.'
    })
    
    return charts_info


def get_chart_as_base64(fig):
    """Convert a matplotlib figure to a base64 encoded string for HTML embedding"""
    buffer = io.BytesIO()
    FigureCanvas(fig).print_png(buffer)
    data = base64.b64encode(buffer.getvalue()).decode('utf8')
    return data
