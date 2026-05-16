from pathlib import Path
import re
import pandas as pd

RAW_FILE = Path("data/raw/ecommerce_orders_raw.xlsx")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def label_review(value):
    text = clean_text(value)

    if text == "":
        return "无效", "空白"

    if re.fullmatch(r"\d+", text) or re.fullmatch(r"[？?。.,，!！~～\s]+", text):
        return "无效", "无有效语义"

    if any(word in text for word in ["评价返现", "返现", "好评返现", "默认好评", "无评价"]):
        return "无效", "疑似非真实评价"

    positive_words = ["很好", "不错", "满意", "推荐", "好用", "物流很快", "包装完整", "下次还会买", "性价比不错", "客服态度很好", "质量很好", "喜欢", "超出预期"]
    negative_words = ["质量差", "不推荐", "太慢", "破损", "坏了", "不一样", "退货", "失望", "不好用", "有问题", "投诉", "偏贵", "差"]
    neutral_words = ["还可以", "一般", "一般般", "正常", "基本一致", "暂时没发现问题", "价格正常", "还行"]

    positive_hit = any(word in text for word in positive_words)
    negative_hit = any(word in text for word in negative_words)
    neutral_hit = any(word in text for word in neutral_words)

    if positive_hit and negative_hit:
        return "不确定", "同时包含正负信息"
    if negative_hit:
        return "负向", "负面词命中"
    if positive_hit:
        return "正向", "正面词命中"
    if neutral_hit:
        return "中性", "弱情绪表达"

    return "不确定", "未命中明确规则"

def main():
    df = pd.read_excel(RAW_FILE, sheet_name="04_标注练习")
    df["文本内容_清理后"] = df["文本内容"].apply(clean_text)

    result = df["文本内容_清理后"].apply(label_review)
    df["标注类别"] = result.apply(lambda x: x[0])
    df["备注"] = result.apply(lambda x: x[1])

    df.to_excel(OUT_DIR / "review_labeling_result.xlsx", index=False)
    df.to_csv(OUT_DIR / "review_labeling_result.csv", index=False, encoding="utf-8-sig")

    print("文本标注完成")
    print(df["标注类别"].value_counts())

if __name__ == "__main__":
    main()
