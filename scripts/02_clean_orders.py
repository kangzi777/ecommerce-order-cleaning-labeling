from pathlib import Path
import re
import numpy as np
import pandas as pd

RAW_FILE = Path("data/raw/ecommerce_orders_raw.xlsx")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

category_map = {
    "数码": "数码", "数码产品": "数码", "手机数码": "数码", "电脑数码": "数码", "电子产品": "数码",
    "digital": "数码", "electronics": "数码",
    "服装": "服装", "服饰": "服装", "服饰-服装": "服装", "服装类": "服装", "衣服": "服装",
    "男装": "服装", "女装": "服装", "clothing": "服装",
    "食品": "食品", "食品类": "食品", "零食": "食品", "饮料": "食品", "food": "食品",
    "美妆": "美妆", "美妆类": "美妆", "化妆品": "美妆", "护肤": "美妆", "护肤品": "美妆", "beauty": "美妆",
    "家居": "家居", "家居用品": "家居", "家具": "家居", "居家": "家居", "home": "家居",
}

payment_map = {
    "支付宝": "支付宝", "alipay": "支付宝",
    "微信": "微信支付", "微信支付": "微信支付", "wechat": "微信支付", "wechat pay": "微信支付",
    "银行卡": "银行卡", "信用卡": "信用卡", "货到付款": "货到付款", "cod": "货到付款"
}

status_map = {
    "已完成": "已完成", "完成": "已完成", "交易成功": "已完成",
    "已取消": "已取消", "取消": "已取消", "取消订单": "已取消",
    "待发货": "待发货", "等待发货": "待发货",
    "退货中": "退货中", "退款中": "退货中",
}

def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def parse_date(value):
    if pd.isna(value):
        return pd.NaT, "缺失日期"

    if isinstance(value, (int, float, np.integer, np.floating)) and not isinstance(value, bool):
        if 20000 <= float(value) <= 60000:
            dt = pd.to_datetime(float(value), unit="D", origin="1899-12-30", errors="coerce")
            if pd.notna(dt):
                return dt.normalize(), ""
        return pd.NaT, "非法日期"

    text = clean_text(value)
    if text == "":
        return pd.NaT, "缺失日期"

    if re.fullmatch(r"\d+(\.0)?", text):
        num = float(text)
        if 20000 <= num <= 60000:
            dt = pd.to_datetime(num, unit="D", origin="1899-12-30", errors="coerce")
            if pd.notna(dt):
                return dt.normalize(), ""

    if re.fullmatch(r"\d{8}", text):
        dt = pd.to_datetime(text, format="%Y%m%d", errors="coerce")
        if pd.notna(dt):
            return dt.normalize(), ""
        return pd.NaT, "非法日期"

    text = text.replace("年", "/").replace("月", "/").replace("日", "")
    text = text.replace("-", "/").replace(".", "/")
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"/+", "/", text)

    dt = pd.to_datetime(text, errors="coerce")
    if pd.isna(dt):
        return pd.NaT, "非法日期"
    return dt.normalize(), ""

def standardize_category(value):
    text = clean_text(value).lower()
    if text == "":
        return "", "商品类别缺失"
    if text in category_map:
        return category_map[text], ""
    return "", "商品类别无法识别"

def parse_quantity(value):
    if pd.isna(value) or clean_text(value) == "":
        return np.nan, "数量缺失"

    text = clean_text(value).replace("件", "").replace("个", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", text):
        return np.nan, "数量格式错误"

    num = float(text)
    if num <= 0:
        return np.nan, "数量非正数"
    if not num.is_integer():
        return np.nan, "数量非整数"

    num = int(num)
    if num > 100:
        return num, "数量异常偏大"
    return num, ""

def parse_price(value):
    if pd.isna(value) or clean_text(value) == "":
        return np.nan, "单价缺失"

    text = clean_text(value).replace("元", "")
    try:
        num = float(text)
    except ValueError:
        return np.nan, "单价格式错误"

    if num <= 0:
        return np.nan, "单价非正数"
    if num > 10000:
        return num, "单价异常偏高"
    return round(num, 2), ""

def parse_discount(value):
    if pd.isna(value) or clean_text(value) == "":
        return np.nan, "折扣缺失"

    text = clean_text(value)
    try:
        if text.endswith("%"):
            num = float(text[:-1]) / 100
        elif text.endswith("折"):
            num = float(text[:-1]) / 10
        else:
            num = float(text)
            if 1 < num <= 10:
                num = num / 10
            elif 10 < num <= 100:
                num = num / 100
    except ValueError:
        return np.nan, "折扣格式错误"

    if not (0 <= num <= 1):
        return np.nan, "折扣超出范围"
    return round(num, 4), ""

def map_value(value, mapper, missing_type, unknown_type):
    text = clean_text(value)
    if text == "":
        return "", missing_type

    key = text.lower()
    if key in mapper:
        return mapper[key], ""
    if text in mapper:
        return mapper[text], ""
    return "", unknown_type

def export_excel(name, data):
    data.to_excel(OUT_DIR / name, index=False)

def main():
    df = pd.read_excel(RAW_FILE, sheet_name="01_原始脏数据")
    df.insert(0, "原表行号", df.index + 2)

    df["订单ID出现次数"] = df.groupby("订单ID")["订单ID"].transform("count")
    duplicate_orders = df[df["订单ID出现次数"] > 1].copy().sort_values(["订单ID", "原表行号"])
    duplicate_orders["问题说明"] = "订单ID重复出现，需结合订单明细判断是否为重复导入或业务拆单。"
    duplicate_orders["处理建议"] = "保留原始记录，进入复核清单。"

    date_result = df["下单日期"].apply(parse_date)
    df["下单日期_标准化"] = date_result.apply(lambda x: x[0].strftime("%Y-%m-%d") if pd.notna(x[0]) else "")
    df["日期异常类型"] = date_result.apply(lambda x: x[1])
    date_errors = df[df["日期异常类型"] != ""].copy()
    date_errors["问题说明"] = date_errors["日期异常类型"].map({"缺失日期": "下单日期为空。", "非法日期": "下单日期无法转成有效日期。"})
    date_errors["处理建议"] = "暂不自动填补，保留为空并进入复核。"

    for col in ["客户ID", "省份", "城市"]:
        df[f"{col}_标准化"] = df[col].apply(clean_text)

    df["客户地区异常类型"] = df.apply(
        lambda r: "；".join(
            name for name, value in [
                ("客户ID缺失", r["客户ID_标准化"]),
                ("省份缺失", r["省份_标准化"]),
                ("城市缺失", r["城市_标准化"]),
            ] if value == ""
        ),
        axis=1
    )
    region_errors = df[df["客户地区异常类型"] != ""].copy()
    region_errors["问题说明"] = "客户或地区字段存在缺失，影响分组统计。"
    region_errors["处理建议"] = "暂不自动补全，后续结合客户资料表复核。"

    category_result = df["商品类别"].apply(standardize_category)
    df["商品类别_标准化"] = category_result.apply(lambda x: x[0])
    df["商品类别异常类型"] = category_result.apply(lambda x: x[1])
    category_errors = df[df["商品类别异常类型"] != ""].copy()
    category_errors["问题说明"] = "商品类别缺失或不在映射规则中。"
    category_errors["处理建议"] = "结合商品名称或业务分类表补充映射规则。"

    quantity_result = df["数量"].apply(parse_quantity)
    df["数量_标准化"] = quantity_result.apply(lambda x: x[0])
    df["数量异常类型"] = quantity_result.apply(lambda x: x[1])
    quantity_errors = df[df["数量异常类型"] != ""].copy()
    quantity_errors["问题说明"] = "数量字段存在缺失、非正数、非整数或异常偏大。"
    quantity_errors["处理建议"] = "不直接修正，进入复核清单。"

    price_result = df["单价"].apply(parse_price)
    discount_result = df["折扣"].apply(parse_discount)
    df["单价_标准化"] = price_result.apply(lambda x: x[0])
    df["单价异常类型"] = price_result.apply(lambda x: x[1])
    df["折扣_标准化"] = discount_result.apply(lambda x: x[0])
    df["折扣异常类型"] = discount_result.apply(lambda x: x[1])
    price_discount_errors = df[(df["单价异常类型"] != "") | (df["折扣异常类型"] != "")].copy()
    price_discount_errors["问题说明"] = "单价或折扣字段存在缺失、格式错误或范围异常。"
    price_discount_errors["处理建议"] = "保留原始值，结合订单明细复核。"

    payment_result = df["支付方式"].apply(lambda x: map_value(x, payment_map, "支付方式缺失", "支付方式无法识别"))
    status_result = df["订单状态"].apply(lambda x: map_value(x, status_map, "订单状态缺失", "订单状态无法识别"))
    df["支付方式_标准化"] = payment_result.apply(lambda x: x[0])
    df["支付方式异常类型"] = payment_result.apply(lambda x: x[1])
    df["订单状态_标准化"] = status_result.apply(lambda x: x[0])
    df["订单状态异常类型"] = status_result.apply(lambda x: x[1])
    payment_status_errors = df[(df["支付方式异常类型"] != "") | (df["订单状态异常类型"] != "")].copy()
    payment_status_errors["问题说明"] = "支付方式或订单状态无法归入标准口径。"
    payment_status_errors["处理建议"] = "人工确认后补充映射规则。"

    df["销售额"] = df["数量_标准化"] * df["单价_标准化"] * (1 - df["折扣_标准化"].fillna(0))

    summary = pd.DataFrame([
        ["原始记录数", len(df)],
        ["重复订单记录数", len(duplicate_orders)],
        ["日期异常记录数", len(date_errors)],
        ["客户地区异常记录数", len(region_errors)],
        ["商品类别异常记录数", len(category_errors)],
        ["数量异常记录数", len(quantity_errors)],
        ["单价/折扣异常记录数", len(price_discount_errors)],
        ["支付/状态异常记录数", len(payment_status_errors)],
    ], columns=["指标", "数量"])

    export_excel("cleaned_orders.xlsx", df)
    export_excel("duplicate_orders.xlsx", duplicate_orders)
    export_excel("date_errors.xlsx", date_errors)
    export_excel("region_errors.xlsx", region_errors)
    export_excel("category_errors.xlsx", category_errors)
    export_excel("quantity_errors.xlsx", quantity_errors)
    export_excel("price_discount_errors.xlsx", price_discount_errors)
    export_excel("payment_status_errors.xlsx", payment_status_errors)
    export_excel("data_quality_summary.xlsx", summary)

    df.to_csv(OUT_DIR / "cleaned_orders.csv", index=False, encoding="utf-8-sig")

    print("清洗完成")
    print(summary)

if __name__ == "__main__":
    main()
