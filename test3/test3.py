import pandas as pd
import sys
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(cur_dir, 'sales-data.csv')
output_file = os.path.join(cur_dir, 'filtered-sales-data.csv')

try:
    df = pd.read_csv(input_file)
    df_valid = df[df['sq__ft'] > 0].copy()
    df_valid['price_per_sqft'] = df_valid['price']/df_valid['sq__ft']
    avg_price = df_valid['price_per_sqft'].mean()
    
    df_below = df_valid[df_valid['price_per_sqft']<avg_price]
    df_output = df_below.drop(columns=['price_per_sqft'])
    df_output.to_csv(output_file, index=False)
    print(f"\nAverage price per sq ft: ${avg_price:.2f}")
    print(f"Filtered data written to {output_file}")
except FileNotFoundError:
    print(f"Error: Could not find file '{input_file}'")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
