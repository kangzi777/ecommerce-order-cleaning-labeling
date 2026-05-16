from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/cleaned_orders.xlsx")
OUTPUT_FILE = Path("data/processed/orders_mysql_ready.csv")

columns = {
    "订单ID": "order_id",
    "下单日期_标准化": "order_date",
    "客户ID_标准化": "customer_id",
    "省份_标准化": "province",
    "城市_标准化": "city",
    "商品类别_标准化": "category",
    "商品名称": "product_name",
    "数量_标准化": "quantity",
    "单价_标准化": "unit_price",
    "折扣_标准化": "discount",
    "支付方式_标准化": "payment_method",
    "订单状态_标准化": "order_status",
    "客户评价": "customer_review",
}

def main():
    df = pd.read_excel(INPUT_FILE)
    out = df[list(columns.keys())].rename(columns=columns)
    out.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"导出完成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
