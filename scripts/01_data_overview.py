from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/ecommerce_orders_raw.xlsx")

def main():
    df = pd.read_excel(RAW_FILE, sheet_name="01_原始脏数据")
    print("数据规模:", df.shape)
    print("字段列表:")
    print(df.columns.tolist())
    print("\n每列缺失值数量:")
    print(df.isna().sum())
    print("\n前5行:")
    print(df.head())

if __name__ == "__main__":
    main()
