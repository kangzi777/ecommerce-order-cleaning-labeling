# 电商订单数据清洗与客户评价文本标注项目

## 项目说明

本项目基于一份模拟电商订单数据，完成订单字段清洗、异常数据识别、清洗结果导出和客户评价文本标注。项目重点不是复杂模型，而是把基础数据处理流程做完整：先保留原始数据，再新增标准化字段，最后将异常记录单独输出，方便后续复核。

## 目录结构

```text
ecommerce-order-cleaning-labeling/
├─ data/
│  ├─ raw/                 # 原始练习数据
│  └─ processed/           # 清洗结果与异常清单
├─ docs/                   # 清洗报告、标注规则、项目记录
├─ scripts/                # Python 处理脚本
├─ sql/                    # MySQL 建表与查询语句
├─ requirements.txt
└─ README.md
```

## 使用工具

- Python
- pandas
- MySQL
- Excel / WPS

## 已完成内容

| 模块 | 处理内容 | 结果文件 |
|---|---|---|
| 订单重复检查 | 识别重复订单ID，并保留全部重复记录 | `duplicate_orders.xlsx` |
| 日期标准化 | 将下单日期统一为 `yyyy-mm-dd`，异常日期单独输出 | `date_errors.xlsx` |
| 客户地区检查 | 检查客户ID、省份、城市缺失并清理前后空格 | `region_errors.xlsx` |
| 商品类别标准化 | 将同义类别归并为统一口径 | `category_errors.xlsx` |
| 数量检查 | 识别数量缺失、非正数、非整数、异常偏大 | `quantity_errors.xlsx` |
| 单价与折扣检查 | 识别单价、折扣字段异常 | `price_discount_errors.xlsx` |
| 支付方式与订单状态 | 将支付方式和订单状态归入标准类别 | `payment_status_errors.xlsx` |
| 文本标注 | 对客户评价进行正向、中性、负向、无效、不确定标注 | `review_labeling_result.xlsx` |

## 运行方式

安装依赖：

```bash
pip install -r requirements.txt
```

查看原始数据概况：

```bash
python scripts/01_data_overview.py
```

执行订单清洗：

```bash
python scripts/02_clean_orders.py
```

执行客户评价文本标注：

```bash
python scripts/03_label_reviews.py
```

生成适合导入 MySQL 的 CSV 文件：

```bash
python scripts/04_export_mysql_ready.py
```

## 清洗原则

1. 不直接覆盖原始字段。
2. 对可标准化的字段新增标准化列。
3. 无法确认的异常记录单独输出清单。
4. 保留原表行号，方便回到原始数据核查。
5. 文本标注中保留备注字段，便于处理边界样本。

## 主要产出

- 清洗后订单数据：`data/processed/cleaned_orders.xlsx`
- 异常清单汇总：`data/processed/data_quality_summary.xlsx`
- 客户评价标注结果：`data/processed/review_labeling_result.xlsx`
- MySQL 查询脚本：`sql/analysis_queries.sql`
- 项目报告：`docs/data_cleaning_report.md`
