"""Seed script to populate DB-GPT with extensive dummy data."""
import asyncio
import json
import uuid
import random
from datetime import datetime, timezone, timedelta

import sys
sys.path.insert(0, ".")

from sqlalchemy import select, text
from app.database import engine, async_session
from app.models.user import User
from app.models.datasource import Datasource
from app.models.query import Query
from app.models.skill import Skill
from app.models.dashboard import Dashboard, DashboardWidget
from app.models.report import Report


def uid():
    return str(uuid.uuid4())


def past_date(days_ago):
    return datetime.now(timezone.utc) - timedelta(days=days_ago)


DATASOURCES = [
    {
        "name": "E-Commerce Production DB",
        "type": "postgresql",
        "description": "Main e-commerce PostgreSQL database with orders, products, customers, and inventory data",
        "config": json.dumps({"host": "db.ecommerce.local", "port": 5432, "database": "ecommerce_prod", "username": "analyst", "password": "****"}),
    },
    {
        "name": "Sales Analytics Warehouse",
        "type": "postgresql",
        "description": "Data warehouse for sales analytics, revenue tracking, and business intelligence",
        "config": json.dumps({"host": "warehouse.analytics.local", "port": 5432, "database": "sales_dw", "username": "bi_user", "password": "****"}),
    },
    {
        "name": "Customer Support MySQL",
        "type": "mysql",
        "description": "MySQL database for customer support tickets, agent performance, and SLA tracking",
        "config": json.dumps({"host": "support-db.internal", "port": 3306, "database": "support_system", "username": "support_reader", "password": "****"}),
    },
    {
        "name": "HR & Payroll Database",
        "type": "postgresql",
        "description": "Human resources database with employee records, departments, salaries, and attendance",
        "config": json.dumps({"host": "hr-db.corp.local", "port": 5432, "database": "hr_payroll", "username": "hr_analyst", "password": "****"}),
    },
    {
        "name": "Marketing Analytics",
        "type": "postgresql",
        "description": "Marketing campaigns, ad spend, conversion tracking, and social media metrics",
        "config": json.dumps({"host": "marketing-db.analytics.local", "port": 5432, "database": "marketing_analytics", "username": "marketer", "password": "****"}),
    },
    {
        "name": "Inventory Management",
        "type": "mysql",
        "description": "Real-time inventory tracking, warehouse locations, stock levels, and supplier data",
        "config": json.dumps({"host": "inventory.warehouse.local", "port": 3306, "database": "inventory_mgmt", "username": "inv_reader", "password": "****"}),
    },
    {
        "name": "Financial Reporting DB",
        "type": "postgresql",
        "description": "Financial data including P&L, balance sheet, cash flow, and budget tracking",
        "config": json.dumps({"host": "finance-db.corp.local", "port": 5432, "database": "financial_reports", "username": "finance_analyst", "password": "****"}),
    },
    {
        "name": "Website Analytics (Clickstream)",
        "type": "postgresql",
        "description": "Clickstream data, page views, user sessions, conversion funnels, and A/B test results",
        "config": json.dumps({"host": "clickstream.analytics.local", "port": 5432, "database": "web_analytics", "username": "web_analyst", "password": "****"}),
    },
]

QUERIES_DATA = [
    {
        "question": "What are the top 10 products by revenue this month?",
        "sql_generated": "SELECT p.name AS product, SUM(oi.quantity * oi.price) AS revenue, SUM(oi.quantity) AS units_sold\nFROM order_items oi\nJOIN products p ON p.id = oi.product_id\nJOIN orders o ON o.id = oi.order_id\nWHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE)\nGROUP BY p.name\nORDER BY revenue DESC\nLIMIT 10;",
        "result_json": json.dumps({
            "columns": ["product", "revenue", "units_sold"],
            "rows": [
                ["MacBook Pro 16\"", 124500.00, 83],
                ["iPhone 15 Pro Max", 98750.00, 79],
                ["Sony WH-1000XM5", 45600.00, 152],
                ["Samsung Galaxy S24 Ultra", 41200.00, 34],
                ["iPad Air M2", 38900.00, 65],
                ["AirPods Pro 2", 29800.00, 119],
                ["Dell XPS 15", 27650.00, 23],
                ["Nintendo Switch OLED", 22400.00, 64],
                ["LG C3 65\" OLED TV", 19800.00, 12],
                ["Dyson V15 Detect", 17500.00, 25],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "product", "y": "revenue"}),
        "summary": "MacBook Pro 16\" leads with $124,500 in revenue (83 units). iPhone 15 Pro Max is second at $98,750. Top 10 products generated $466,100 total this month.",
        "execution_time": 0.234,
        "status": "completed",
        "ds_idx": 0,
    },
    {
        "question": "Show monthly revenue trend for the last 12 months",
        "sql_generated": "SELECT DATE_TRUNC('month', created_at)::date AS month, SUM(total_amount) AS revenue, COUNT(*) AS order_count\nFROM orders\nWHERE created_at >= CURRENT_DATE - INTERVAL '12 months'\nGROUP BY month\nORDER BY month;",
        "result_json": json.dumps({
            "columns": ["month", "revenue", "order_count"],
            "rows": [
                ["2025-07-01", 185000, 1240],
                ["2025-08-01", 192000, 1310],
                ["2025-09-01", 178000, 1180],
                ["2025-10-01", 205000, 1420],
                ["2025-11-01", 289000, 2100],
                ["2025-12-01", 342000, 2650],
                ["2026-01-01", 198000, 1350],
                ["2026-02-01", 175000, 1190],
                ["2026-03-01", 215000, 1480],
                ["2026-04-01", 228000, 1560],
                ["2026-05-01", 245000, 1680],
                ["2026-06-01", 262000, 1790],
            ]
        }),
        "chart_config": json.dumps({"type": "line", "x": "month", "y": "revenue"}),
        "summary": "Revenue peaked in December 2025 ($342K) during holiday season. Steady growth from March-June 2026 with current month at $262K. YoY growth is approximately 18%.",
        "execution_time": 0.189,
        "status": "completed",
        "ds_idx": 1,
    },
    {
        "question": "Customer acquisition by channel this quarter",
        "sql_generated": "SELECT acquisition_channel, COUNT(*) AS new_customers, ROUND(AVG(first_order_value), 2) AS avg_first_order\nFROM customers\nWHERE created_at >= DATE_TRUNC('quarter', CURRENT_DATE)\nGROUP BY acquisition_channel\nORDER BY new_customers DESC;",
        "result_json": json.dumps({
            "columns": ["acquisition_channel", "new_customers", "avg_first_order"],
            "rows": [
                ["Organic Search", 2340, 85.50],
                ["Paid Social (Meta)", 1890, 72.30],
                ["Google Ads", 1560, 95.20],
                ["Email Marketing", 980, 110.40],
                ["Referral Program", 750, 125.80],
                ["Direct", 620, 68.90],
                ["Affiliate", 450, 78.60],
                ["TikTok Ads", 380, 55.40],
            ]
        }),
        "chart_config": json.dumps({"type": "pie", "values": "new_customers", "labels": "acquisition_channel"}),
        "summary": "Organic Search drives the most new customers (2,340) but Referral Program has the highest avg first order ($125.80). Total 8,970 new customers this quarter.",
        "execution_time": 0.156,
        "status": "completed",
        "ds_idx": 4,
    },
    {
        "question": "Average ticket resolution time by support category",
        "sql_generated": "SELECT category, COUNT(*) AS ticket_count, ROUND(AVG(resolution_hours), 1) AS avg_resolution_hrs,\n  ROUND(AVG(customer_satisfaction), 1) AS avg_csat\nFROM support_tickets\nWHERE created_at >= CURRENT_DATE - INTERVAL '30 days'\nGROUP BY category\nORDER BY avg_resolution_hrs;",
        "result_json": json.dumps({
            "columns": ["category", "ticket_count", "avg_resolution_hrs", "avg_csat"],
            "rows": [
                ["Password Reset", 342, 0.5, 4.8],
                ["Order Status", 567, 1.2, 4.5],
                ["Billing Inquiry", 289, 2.8, 4.2],
                ["Product Question", 445, 3.5, 4.3],
                ["Return/Refund", 378, 6.2, 3.9],
                ["Technical Issue", 234, 8.4, 3.7],
                ["Shipping Problem", 189, 12.1, 3.4],
                ["Account Security", 67, 15.3, 4.1],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "category", "y": "avg_resolution_hrs"}),
        "summary": "Password Resets are resolved fastest (0.5 hrs avg). Shipping Problems and Account Security take longest (12-15 hrs). Overall CSAT average is 4.1/5.0.",
        "execution_time": 0.312,
        "status": "completed",
        "ds_idx": 2,
    },
    {
        "question": "Employee headcount by department with average salary",
        "sql_generated": "SELECT d.name AS department, COUNT(e.id) AS headcount, ROUND(AVG(e.salary), 0) AS avg_salary,\n  ROUND(SUM(e.salary), 0) AS total_payroll\nFROM employees e\nJOIN departments d ON d.id = e.department_id\nWHERE e.is_active = true\nGROUP BY d.name\nORDER BY headcount DESC;",
        "result_json": json.dumps({
            "columns": ["department", "headcount", "avg_salary", "total_payroll"],
            "rows": [
                ["Engineering", 145, 125000, 18125000],
                ["Sales", 89, 78000, 6942000],
                ["Customer Support", 67, 52000, 3484000],
                ["Marketing", 45, 85000, 3825000],
                ["Product", 38, 115000, 4370000],
                ["Operations", 34, 68000, 2312000],
                ["Finance", 28, 95000, 2660000],
                ["HR", 22, 72000, 1584000],
                ["Legal", 12, 130000, 1560000],
                ["Executive", 8, 250000, 2000000],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "department", "y": "headcount"}),
        "summary": "Total headcount: 488 employees. Engineering is largest (145). Total monthly payroll: $46.8M annually. Executive avg salary is highest at $250K.",
        "execution_time": 0.098,
        "status": "completed",
        "ds_idx": 3,
    },
    {
        "question": "Top performing marketing campaigns by ROI",
        "sql_generated": "SELECT campaign_name, channel, spend, revenue_attributed, ROUND((revenue_attributed - spend) / spend * 100, 1) AS roi_pct,\n  conversions\nFROM campaigns\nWHERE start_date >= CURRENT_DATE - INTERVAL '90 days'\nORDER BY roi_pct DESC\nLIMIT 10;",
        "result_json": json.dumps({
            "columns": ["campaign_name", "channel", "spend", "revenue_attributed", "roi_pct", "conversions"],
            "rows": [
                ["Summer Sale Email Blast", "Email", 2500, 89000, 3460.0, 890],
                ["Referral Bonus 2x", "Referral", 8000, 156000, 1850.0, 520],
                ["Brand Ambassador Program", "Influencer", 15000, 178000, 1086.7, 445],
                ["Google Shopping Ads", "Google Ads", 25000, 185000, 640.0, 1230],
                ["Facebook Retargeting", "Meta Ads", 18000, 98000, 444.4, 654],
                ["LinkedIn B2B Campaign", "LinkedIn", 12000, 62000, 416.7, 124],
                ["TikTok Product Showcase", "TikTok", 8500, 38000, 347.1, 380],
                ["YouTube Pre-roll", "YouTube", 20000, 75000, 275.0, 500],
                ["Instagram Stories", "Meta Ads", 10000, 35000, 250.0, 350],
                ["Podcast Sponsorship", "Audio", 5000, 16500, 230.0, 55],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "campaign_name", "y": "roi_pct"}),
        "summary": "Email campaigns deliver the highest ROI (3,460%). Referral program is second (1,850%). Total spend: $124K across top 10 campaigns generating $932.5K revenue.",
        "execution_time": 0.267,
        "status": "completed",
        "ds_idx": 4,
    },
    {
        "question": "Inventory stock levels below reorder point",
        "sql_generated": "SELECT p.sku, p.name, w.warehouse_name, i.current_stock, i.reorder_point, i.reorder_point - i.current_stock AS deficit,\n  p.unit_cost\nFROM inventory i\nJOIN products p ON p.id = i.product_id\nJOIN warehouses w ON w.id = i.warehouse_id\nWHERE i.current_stock < i.reorder_point\nORDER BY deficit DESC;",
        "result_json": json.dumps({
            "columns": ["sku", "name", "warehouse_name", "current_stock", "reorder_point", "deficit", "unit_cost"],
            "rows": [
                ["SKU-1042", "Wireless Earbuds Pro", "East Coast Warehouse", 12, 200, 188, 45.00],
                ["SKU-2087", "USB-C Hub 7-in-1", "Central Distribution", 34, 150, 116, 22.50],
                ["SKU-3156", "Laptop Stand Adjustable", "West Coast Warehouse", 8, 100, 92, 35.00],
                ["SKU-1589", "Phone Case Premium", "East Coast Warehouse", 45, 500, 455, 8.50],
                ["SKU-4201", "Mechanical Keyboard RGB", "Central Distribution", 5, 80, 75, 65.00],
                ["SKU-2344", "Monitor Arm Dual", "West Coast Warehouse", 18, 60, 42, 55.00],
                ["SKU-5012", "Webcam 4K HDR", "East Coast Warehouse", 22, 50, 28, 78.00],
                ["SKU-3789", "Desk Mat XXL", "Central Distribution", 30, 45, 15, 18.00],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "name", "y": "deficit"}),
        "summary": "8 products below reorder point. Phone Case Premium has the largest deficit (455 units). Wireless Earbuds Pro critically low (12 units vs 200 reorder point). Estimated reorder cost: ~$52K.",
        "execution_time": 0.145,
        "status": "completed",
        "ds_idx": 5,
    },
    {
        "question": "Quarterly P&L summary comparison",
        "sql_generated": "SELECT category, q1_2026 AS q1, q2_2026 AS q2, q2_2026 - q1_2026 AS change,\n  ROUND((q2_2026 - q1_2026)::numeric / NULLIF(q1_2026, 0) * 100, 1) AS change_pct\nFROM financial_summary\nWHERE fiscal_year = 2026\nORDER BY sort_order;",
        "result_json": json.dumps({
            "columns": ["category", "q1", "q2", "change", "change_pct"],
            "rows": [
                ["Revenue", 2450000, 2780000, 330000, 13.5],
                ["Cost of Goods Sold", -980000, -1050000, -70000, 7.1],
                ["Gross Profit", 1470000, 1730000, 260000, 17.7],
                ["Operating Expenses", -890000, -920000, -30000, 3.4],
                ["Marketing Spend", -245000, -310000, -65000, 26.5],
                ["R&D Expenses", -380000, -395000, -15000, 3.9],
                ["EBITDA", 580000, 810000, 230000, 39.7],
                ["Net Income", 435000, 625000, 190000, 43.7],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "category", "y": ["q1", "q2"]}),
        "summary": "Q2 shows strong improvement: Revenue up 13.5% to $2.78M, Net Income up 43.7% to $625K. Marketing spend increased 26.5% driving growth. EBITDA margin improved from 23.7% to 29.1%.",
        "execution_time": 0.089,
        "status": "completed",
        "ds_idx": 6,
    },
    {
        "question": "Website conversion funnel analysis",
        "sql_generated": "SELECT stage, users_count, ROUND(users_count::numeric / LAG(users_count) OVER (ORDER BY stage_order) * 100, 1) AS conversion_rate,\n  ROUND(users_count::numeric / FIRST_VALUE(users_count) OVER (ORDER BY stage_order) * 100, 1) AS overall_rate\nFROM conversion_funnel\nWHERE period = 'last_30_days'\nORDER BY stage_order;",
        "result_json": json.dumps({
            "columns": ["stage", "users_count", "conversion_rate", "overall_rate"],
            "rows": [
                ["Homepage Visit", 285000, None, 100.0],
                ["Product Page View", 142500, 50.0, 50.0],
                ["Add to Cart", 42750, 30.0, 15.0],
                ["Begin Checkout", 21375, 50.0, 7.5],
                ["Payment Info", 14962, 70.0, 5.2],
                ["Order Completed", 11400, 76.2, 4.0],
            ]
        }),
        "chart_config": json.dumps({"type": "funnel", "x": "users_count", "y": "stage"}),
        "summary": "Overall conversion rate: 4.0% (11,400 orders from 285K visits). Biggest drop: Product Page → Add to Cart (30%). Payment → Order completion is strong at 76.2%.",
        "execution_time": 0.178,
        "status": "completed",
        "ds_idx": 7,
    },
    {
        "question": "Customer lifetime value by cohort",
        "sql_generated": "SELECT cohort_month, customer_count, ROUND(avg_ltv, 2) AS avg_ltv, ROUND(avg_orders, 1) AS avg_orders,\n  ROUND(retention_rate_6m, 1) AS retention_6m_pct\nFROM customer_cohorts\nWHERE cohort_month >= '2025-07-01'\nORDER BY cohort_month;",
        "result_json": json.dumps({
            "columns": ["cohort_month", "customer_count", "avg_ltv", "avg_orders", "retention_6m_pct"],
            "rows": [
                ["2025-07", 1850, 345.20, 4.2, 42.5],
                ["2025-08", 2100, 312.80, 3.8, 39.8],
                ["2025-09", 1920, 298.50, 3.5, 38.2],
                ["2025-10", 2340, 278.90, 3.2, 35.6],
                ["2025-11", 3200, 256.40, 2.8, 32.1],
                ["2025-12", 4100, 234.70, 2.5, 28.9],
                ["2026-01", 2450, 198.30, 2.1, 25.4],
                ["2026-02", 2180, 165.50, 1.8, None],
                ["2026-03", 2560, 142.80, 1.5, None],
                ["2026-04", 2890, 98.60, 1.2, None],
                ["2026-05", 3100, 65.40, 0.8, None],
                ["2026-06", 2780, 32.10, 0.4, None],
            ]
        }),
        "chart_config": json.dumps({"type": "line", "x": "cohort_month", "y": "avg_ltv"}),
        "summary": "July 2025 cohort has highest LTV ($345.20) with 42.5% 6-month retention. December spike (4,100 customers) shows lower retention (28.9%) - likely holiday buyers. Recent cohorts still maturing.",
        "execution_time": 0.342,
        "status": "completed",
        "ds_idx": 1,
    },
    {
        "question": "Daily active users and session duration trend",
        "sql_generated": "SELECT date, dau, ROUND(avg_session_minutes, 1) AS avg_session_min, page_views, bounce_rate\nFROM daily_metrics\nWHERE date >= CURRENT_DATE - INTERVAL '14 days'\nORDER BY date;",
        "result_json": json.dumps({
            "columns": ["date", "dau", "avg_session_min", "page_views", "bounce_rate"],
            "rows": [
                ["2026-06-06", 12500, 8.2, 87500, 35.2],
                ["2026-06-07", 11800, 7.9, 82600, 36.1],
                ["2026-06-08", 9200, 6.5, 55200, 42.3],
                ["2026-06-09", 13400, 8.5, 93800, 33.8],
                ["2026-06-10", 14200, 8.8, 99400, 32.5],
                ["2026-06-11", 13900, 8.6, 97300, 33.1],
                ["2026-06-12", 13100, 8.3, 91700, 34.2],
                ["2026-06-13", 12800, 8.1, 89600, 34.8],
                ["2026-06-14", 11500, 7.7, 80500, 36.5],
                ["2026-06-15", 8900, 6.2, 53400, 43.1],
                ["2026-06-16", 14800, 9.1, 103600, 31.2],
                ["2026-06-17", 15200, 9.3, 106400, 30.8],
                ["2026-06-18", 14600, 8.9, 102200, 31.5],
                ["2026-06-19", 13900, 8.6, 97300, 33.0],
            ]
        }),
        "chart_config": json.dumps({"type": "line", "x": "date", "y": "dau"}),
        "summary": "Weekday DAU averages ~13.5K, weekends drop to ~9-10K. Peak was June 17 (15,200 DAU). Bounce rate inversely correlates with session duration. Avg pages per session: ~7.",
        "execution_time": 0.112,
        "status": "completed",
        "ds_idx": 7,
    },
    {
        "question": "Sales by region and product category",
        "sql_generated": "SELECT r.region_name, c.category_name, SUM(o.total_amount) AS revenue, COUNT(o.id) AS orders\nFROM orders o\nJOIN customers cust ON cust.id = o.customer_id\nJOIN regions r ON r.id = cust.region_id\nJOIN order_items oi ON oi.order_id = o.id\nJOIN products p ON p.id = oi.product_id\nJOIN categories c ON c.id = p.category_id\nGROUP BY r.region_name, c.category_name\nORDER BY revenue DESC\nLIMIT 15;",
        "result_json": json.dumps({
            "columns": ["region_name", "category_name", "revenue", "orders"],
            "rows": [
                ["North America", "Electronics", 450000, 3200],
                ["Europe", "Electronics", 380000, 2800],
                ["North America", "Fashion", 285000, 4500],
                ["Asia Pacific", "Electronics", 265000, 2100],
                ["Europe", "Fashion", 245000, 3800],
                ["North America", "Home & Living", 198000, 2200],
                ["Asia Pacific", "Fashion", 175000, 2900],
                ["Europe", "Home & Living", 165000, 1800],
                ["North America", "Sports", 142000, 1600],
                ["Latin America", "Electronics", 125000, 980],
                ["Asia Pacific", "Home & Living", 118000, 1400],
                ["Europe", "Sports", 112000, 1200],
                ["Latin America", "Fashion", 98000, 1500],
                ["North America", "Beauty", 95000, 1800],
                ["Asia Pacific", "Sports", 88000, 950],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "region_name", "y": "revenue", "color": "category_name"}),
        "summary": "North America leads in Electronics ($450K) and overall revenue. Electronics is the top category globally. Fashion has highest order volume. Total: $2.94M across all region-category combos shown.",
        "execution_time": 0.456,
        "status": "completed",
        "ds_idx": 1,
    },
    {
        "question": "Support agent performance leaderboard",
        "sql_generated": "SELECT agent_name, tickets_resolved, ROUND(avg_resolution_hours, 1) AS avg_hours,\n  ROUND(avg_csat, 2) AS csat, first_contact_resolution_pct\nFROM agent_performance\nWHERE month = DATE_TRUNC('month', CURRENT_DATE)\nORDER BY tickets_resolved DESC;",
        "result_json": json.dumps({
            "columns": ["agent_name", "tickets_resolved", "avg_hours", "csat", "first_contact_resolution_pct"],
            "rows": [
                ["Sarah Johnson", 186, 1.8, 4.82, 89],
                ["Ahmed Khan", 172, 2.1, 4.75, 85],
                ["Maria Garcia", 168, 1.5, 4.91, 92],
                ["James Wilson", 155, 2.4, 4.68, 82],
                ["Lisa Chen", 149, 1.9, 4.79, 87],
                ["David Park", 142, 2.8, 4.55, 78],
                ["Emma Thompson", 138, 2.2, 4.72, 84],
                ["Carlos Rivera", 135, 3.1, 4.48, 75],
                ["Priya Patel", 128, 2.5, 4.61, 80],
                ["Michael Brown", 118, 3.5, 4.42, 72],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "agent_name", "y": "tickets_resolved"}),
        "summary": "Maria Garcia has best CSAT (4.91) and FCR (92%) despite not being #1 in volume. Sarah Johnson leads in volume (186). Team average: 149 tickets, 4.67 CSAT.",
        "execution_time": 0.134,
        "status": "completed",
        "ds_idx": 2,
    },
    {
        "question": "Monthly recurring revenue (MRR) breakdown",
        "sql_generated": "SELECT plan_name, subscriber_count, mrr, ROUND(mrr::numeric / subscriber_count, 2) AS arpu,\n  churn_rate_pct\nFROM subscription_metrics\nWHERE month = DATE_TRUNC('month', CURRENT_DATE)\nORDER BY mrr DESC;",
        "result_json": json.dumps({
            "columns": ["plan_name", "subscriber_count", "mrr", "arpu", "churn_rate_pct"],
            "rows": [
                ["Enterprise", 125, 187500, 1500.00, 1.2],
                ["Business Pro", 890, 133500, 150.00, 3.5],
                ["Team", 2340, 116850, 49.93, 4.8],
                ["Professional", 4500, 112500, 25.00, 5.2],
                ["Starter", 8900, 89000, 10.00, 8.1],
                ["Free Trial", 12000, 0, 0.00, None],
            ]
        }),
        "chart_config": json.dumps({"type": "pie", "values": "mrr", "labels": "plan_name"}),
        "summary": "Total MRR: $639,350. Enterprise plan contributes most ($187.5K) with lowest churn (1.2%). 12,000 free trial users represent conversion opportunity. Overall blended ARPU: $38.18.",
        "execution_time": 0.078,
        "status": "completed",
        "ds_idx": 6,
    },
    {
        "question": "Product return rates and reasons",
        "sql_generated": "SELECT p.category, COUNT(r.id) AS returns, COUNT(DISTINCT o.id) AS total_orders,\n  ROUND(COUNT(r.id)::numeric / COUNT(DISTINCT o.id) * 100, 1) AS return_rate,\n  MODE() WITHIN GROUP (ORDER BY r.reason) AS top_reason\nFROM returns r\nJOIN orders o ON o.id = r.order_id\nJOIN products p ON p.id = r.product_id\nWHERE r.created_at >= CURRENT_DATE - INTERVAL '30 days'\nGROUP BY p.category\nORDER BY return_rate DESC;",
        "result_json": json.dumps({
            "columns": ["category", "returns", "total_orders", "return_rate", "top_reason"],
            "rows": [
                ["Fashion", 890, 4500, 19.8, "Wrong Size"],
                ["Electronics", 420, 3200, 13.1, "Defective"],
                ["Shoes", 350, 2100, 16.7, "Doesn't Fit"],
                ["Beauty", 180, 1800, 10.0, "Allergic Reaction"],
                ["Home & Living", 155, 2200, 7.0, "Not As Described"],
                ["Sports", 98, 1600, 6.1, "Changed Mind"],
                ["Books", 25, 950, 2.6, "Damaged in Shipping"],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "category", "y": "return_rate"}),
        "summary": "Fashion has highest return rate (19.8%) primarily due to sizing issues. Overall return rate: 12.8%. Returns cost estimate: ~$156K/month. Recommendation: improve size guide and product photos.",
        "execution_time": 0.289,
        "status": "completed",
        "ds_idx": 0,
    },
    {
        "question": "Server response time percentiles by endpoint",
        "sql_generated": "SELECT endpoint, request_count, p50_ms, p95_ms, p99_ms, error_rate_pct\nFROM endpoint_metrics\nWHERE date = CURRENT_DATE\nORDER BY p99_ms DESC\nLIMIT 10;",
        "result_json": json.dumps({
            "columns": ["endpoint", "request_count", "p50_ms", "p95_ms", "p99_ms", "error_rate_pct"],
            "rows": [
                ["/api/search", 45000, 120, 850, 2400, 0.3],
                ["/api/checkout", 8500, 95, 450, 1800, 0.1],
                ["/api/recommendations", 32000, 80, 380, 1200, 0.2],
                ["/api/products", 68000, 45, 180, 650, 0.05],
                ["/api/cart", 22000, 35, 150, 520, 0.08],
                ["/api/auth/login", 12000, 30, 120, 480, 0.5],
                ["/api/user/profile", 15000, 25, 95, 350, 0.02],
                ["/api/orders", 18000, 55, 220, 780, 0.12],
                ["/api/inventory", 9500, 40, 160, 420, 0.06],
                ["/api/analytics", 5000, 200, 1200, 3500, 0.8],
            ]
        }),
        "chart_config": json.dumps({"type": "bar", "x": "endpoint", "y": ["p50_ms", "p95_ms", "p99_ms"]}),
        "summary": "/api/analytics has worst p99 (3.5s) and highest error rate (0.8%). /api/search also slow at p99. /api/products handles highest volume (68K) with best performance. Target: all p99 < 1s.",
        "execution_time": 0.067,
        "status": "completed",
        "ds_idx": 7,
    },
]

SKILLS_DATA = [
    {
        "name": "Monthly Sales Report",
        "description": "Generate comprehensive monthly sales analysis with revenue breakdown, top products, and trend comparison",
        "prompt_template": "Analyze the sales data for {month} {year}. Show: 1) Total revenue and order count compared to previous month, 2) Top 10 products by revenue, 3) Revenue by category, 4) Daily revenue trend, 5) Average order value trend. Highlight any significant changes.",
        "parameters": json.dumps([{"name": "month", "type": "string"}, {"name": "year", "type": "string"}]),
        "category": "sales",
    },
    {
        "name": "Customer Churn Analysis",
        "description": "Identify at-risk customers and analyze churn patterns with predictive indicators",
        "prompt_template": "Analyze customer churn for the last {period}. Find: 1) Customers who haven't ordered in 90+ days, 2) Churn rate by acquisition channel, 3) Common patterns before churn (order frequency decline, support tickets), 4) Revenue impact of churned customers, 5) Suggested retention actions.",
        "parameters": json.dumps([{"name": "period", "type": "string"}]),
        "category": "sales",
    },
    {
        "name": "Financial Health Check",
        "description": "Quick overview of key financial metrics, ratios, and budget variance analysis",
        "prompt_template": "Run a financial health check for {period}. Include: 1) Revenue vs budget variance, 2) Gross margin trend, 3) Operating expense ratio, 4) Cash flow summary, 5) Key financial ratios (current ratio, quick ratio, debt-to-equity). Flag any metrics outside target range.",
        "parameters": json.dumps([{"name": "period", "type": "string"}]),
        "category": "finance",
    },
    {
        "name": "Marketing Campaign ROI",
        "description": "Calculate and compare ROI across all marketing channels and campaigns",
        "prompt_template": "Analyze marketing ROI for {channel} campaigns in {period}. Show: 1) Spend vs revenue attribution, 2) Cost per acquisition (CPA), 3) Customer lifetime value (CLV) by channel, 4) Campaign performance ranking, 5) Budget reallocation recommendations based on ROI.",
        "parameters": json.dumps([{"name": "channel", "type": "string"}, {"name": "period", "type": "string"}]),
        "category": "marketing",
    },
    {
        "name": "Inventory Optimization",
        "description": "Analyze stock levels, identify overstock/understock, and suggest optimal reorder quantities",
        "prompt_template": "Optimize inventory for {warehouse}. Analyze: 1) Products below reorder point, 2) Overstocked items (> 90 days supply), 3) Dead stock identification, 4) Suggested reorder quantities using EOQ model, 5) Estimated savings from optimization. Consider lead times and seasonality.",
        "parameters": json.dumps([{"name": "warehouse", "type": "string"}]),
        "category": "operations",
    },
    {
        "name": "Employee Performance Summary",
        "description": "Generate employee performance metrics, team comparisons, and productivity analysis",
        "prompt_template": "Create a performance summary for {department} department. Include: 1) Individual KPIs vs targets, 2) Team productivity metrics, 3) Attendance and overtime analysis, 4) Quarter-over-quarter improvement, 5) Top performers and those needing support.",
        "parameters": json.dumps([{"name": "department", "type": "string"}]),
        "category": "general",
    },
    {
        "name": "A/B Test Analysis",
        "description": "Statistical analysis of A/B test results with significance testing and recommendations",
        "prompt_template": "Analyze A/B test results for {test_name}. Calculate: 1) Conversion rate for control vs variant, 2) Statistical significance (p-value, confidence interval), 3) Lift percentage, 4) Sample size adequacy, 5) Revenue impact projection. Recommend: ship, iterate, or discard.",
        "parameters": json.dumps([{"name": "test_name", "type": "string"}]),
        "category": "marketing",
    },
    {
        "name": "Support SLA Compliance Report",
        "description": "Track support team SLA adherence, identify bottlenecks, and suggest improvements",
        "prompt_template": "Generate SLA compliance report for {period}. Show: 1) First response time vs SLA target, 2) Resolution time by priority level, 3) SLA breach analysis (which categories, when), 4) Agent workload distribution, 5) Customer satisfaction correlation with response time.",
        "parameters": json.dumps([{"name": "period", "type": "string"}]),
        "category": "operations",
    },
    {
        "name": "Revenue Forecast",
        "description": "Predict future revenue using historical trends, seasonality, and growth factors",
        "prompt_template": "Forecast revenue for the next {months} months. Method: 1) Analyze last 24 months of revenue data, 2) Identify seasonal patterns, 3) Apply growth rate from recent trend, 4) Factor in known upcoming events/promotions, 5) Provide optimistic, base, and pessimistic scenarios with confidence intervals.",
        "parameters": json.dumps([{"name": "months", "type": "string"}]),
        "category": "finance",
    },
    {
        "name": "Product Performance Deep Dive",
        "description": "Comprehensive analysis of a specific product including sales, returns, reviews, and market position",
        "prompt_template": "Deep dive into {product_name} performance. Analyze: 1) Sales volume and revenue trend (30/60/90 days), 2) Return rate and reasons, 3) Customer review sentiment, 4) Price point analysis vs competitors, 5) Cross-sell and bundle opportunities. Include actionable recommendations.",
        "parameters": json.dumps([{"name": "product_name", "type": "string"}]),
        "category": "sales",
    },
    {
        "name": "Data Quality Audit",
        "description": "Check data completeness, accuracy, and consistency across database tables",
        "prompt_template": "Audit data quality for {table_name}. Check: 1) Null/empty values per column, 2) Duplicate records, 3) Referential integrity violations, 4) Data type consistency, 5) Outlier detection using IQR method. Assign a data quality score (0-100) and list critical issues.",
        "parameters": json.dumps([{"name": "table_name", "type": "string"}]),
        "category": "general",
    },
    {
        "name": "Cohort Retention Analysis",
        "description": "Analyze user retention by signup cohort with visual retention matrix",
        "prompt_template": "Build a cohort retention analysis for users who signed up in {period}. Show: 1) Monthly retention rates per cohort, 2) Retention curve comparison, 3) Identify best/worst performing cohorts, 4) Correlation with acquisition channel, 5) Revenue retention vs user retention.",
        "parameters": json.dumps([{"name": "period", "type": "string"}]),
        "category": "marketing",
    },
]


DASHBOARDS_DATA = [
    {
        "name": "Executive KPI Dashboard",
        "description": "High-level business metrics for leadership team - revenue, growth, customer satisfaction, and operational efficiency",
        "widgets": [
            {"title": "Monthly Revenue", "type": "metric", "config": json.dumps({"value": "$2.78M", "change": "+13.5%", "period": "vs last month", "color": "green"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Active Customers", "type": "metric", "config": json.dumps({"value": "28,450", "change": "+8.2%", "period": "vs last month", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "Avg Order Value", "type": "metric", "config": json.dumps({"value": "$156.80", "change": "+4.3%", "period": "vs last month", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "Customer NPS", "type": "metric", "config": json.dumps({"value": "72", "change": "+3", "period": "vs last quarter", "color": "green"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "Revenue Trend (12 Months)", "type": "line_chart", "config": json.dumps({"query_ref": "monthly_revenue", "x": "month", "y": "revenue"}), "position_x": 0, "position_y": 2, "width": 8, "height": 4},
            {"title": "Revenue by Category", "type": "pie_chart", "config": json.dumps({"data": [{"label": "Electronics", "value": 45}, {"label": "Fashion", "value": 25}, {"label": "Home", "value": 15}, {"label": "Sports", "value": 10}, {"label": "Other", "value": 5}]}), "position_x": 8, "position_y": 2, "width": 4, "height": 4},
        ],
    },
    {
        "name": "Sales Analytics Dashboard",
        "description": "Detailed sales performance tracking with product analytics, regional breakdown, and sales team metrics",
        "widgets": [
            {"title": "Today's Sales", "type": "metric", "config": json.dumps({"value": "$92,340", "change": "+22%", "period": "vs yesterday", "color": "green"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Orders Today", "type": "metric", "config": json.dumps({"value": "634", "change": "+15%", "period": "vs yesterday", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "Conversion Rate", "type": "metric", "config": json.dumps({"value": "4.2%", "change": "+0.3%", "period": "vs last week", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "Cart Abandonment", "type": "metric", "config": json.dumps({"value": "68.5%", "change": "-2.1%", "period": "vs last week", "color": "red"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "Top Products by Revenue", "type": "bar_chart", "config": json.dumps({"query_ref": "top_products"}), "position_x": 0, "position_y": 2, "width": 6, "height": 4},
            {"title": "Sales by Region", "type": "bar_chart", "config": json.dumps({"query_ref": "regional_sales"}), "position_x": 6, "position_y": 2, "width": 6, "height": 4},
            {"title": "Hourly Sales Pattern", "type": "area_chart", "config": json.dumps({"query_ref": "hourly_sales"}), "position_x": 0, "position_y": 6, "width": 12, "height": 3},
        ],
    },
    {
        "name": "Customer Support Dashboard",
        "description": "Real-time support metrics including queue status, agent performance, CSAT trends, and SLA compliance",
        "widgets": [
            {"title": "Open Tickets", "type": "metric", "config": json.dumps({"value": "127", "change": "-12", "period": "vs yesterday", "color": "green"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Avg Response Time", "type": "metric", "config": json.dumps({"value": "4.2 min", "change": "-18%", "period": "vs last week", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "CSAT Score", "type": "metric", "config": json.dumps({"value": "4.6/5.0", "change": "+0.2", "period": "vs last month", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "SLA Compliance", "type": "metric", "config": json.dumps({"value": "94.8%", "change": "+1.5%", "period": "vs last month", "color": "green"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "Tickets by Category", "type": "pie_chart", "config": json.dumps({"data": [{"label": "Order Status", "value": 30}, {"label": "Returns", "value": 22}, {"label": "Product Q", "value": 18}, {"label": "Billing", "value": 15}, {"label": "Technical", "value": 15}]}), "position_x": 0, "position_y": 2, "width": 4, "height": 4},
            {"title": "Agent Performance", "type": "table", "config": json.dumps({"query_ref": "agent_performance"}), "position_x": 4, "position_y": 2, "width": 8, "height": 4},
        ],
    },
    {
        "name": "Marketing Performance",
        "description": "Campaign performance, channel attribution, conversion tracking, and marketing spend optimization",
        "widgets": [
            {"title": "Marketing Spend (MTD)", "type": "metric", "config": json.dumps({"value": "$124,500", "change": "+8%", "period": "vs budget", "color": "yellow"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Overall ROAS", "type": "metric", "config": json.dumps({"value": "7.5x", "change": "+1.2x", "period": "vs last month", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "New Customers", "type": "metric", "config": json.dumps({"value": "8,970", "change": "+18%", "period": "vs last quarter", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "Email Open Rate", "type": "metric", "config": json.dumps({"value": "32.5%", "change": "+5.2%", "period": "vs industry avg", "color": "green"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "Campaign ROI Comparison", "type": "bar_chart", "config": json.dumps({"query_ref": "campaign_roi"}), "position_x": 0, "position_y": 2, "width": 7, "height": 4},
            {"title": "Customer Acquisition by Channel", "type": "pie_chart", "config": json.dumps({"data": [{"label": "Organic", "value": 26}, {"label": "Paid Social", "value": 21}, {"label": "Google Ads", "value": 17}, {"label": "Email", "value": 11}, {"label": "Referral", "value": 8}, {"label": "Other", "value": 17}]}), "position_x": 7, "position_y": 2, "width": 5, "height": 4},
        ],
    },
    {
        "name": "Financial Overview",
        "description": "P&L overview, budget tracking, cash flow monitoring, and financial KPI summary",
        "widgets": [
            {"title": "Gross Revenue (Q2)", "type": "metric", "config": json.dumps({"value": "$2.78M", "change": "+13.5%", "period": "vs Q1", "color": "green"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Net Income", "type": "metric", "config": json.dumps({"value": "$625K", "change": "+43.7%", "period": "vs Q1", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "EBITDA Margin", "type": "metric", "config": json.dumps({"value": "29.1%", "change": "+5.4pp", "period": "vs Q1", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "Burn Rate", "type": "metric", "config": json.dumps({"value": "$358K/mo", "change": "-4.2%", "period": "vs last month", "color": "green"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "P&L Quarterly Comparison", "type": "bar_chart", "config": json.dumps({"query_ref": "pnl_comparison"}), "position_x": 0, "position_y": 2, "width": 8, "height": 4},
            {"title": "Expense Breakdown", "type": "pie_chart", "config": json.dumps({"data": [{"label": "COGS", "value": 38}, {"label": "Engineering", "value": 22}, {"label": "Marketing", "value": 16}, {"label": "Sales", "value": 12}, {"label": "G&A", "value": 12}]}), "position_x": 8, "position_y": 2, "width": 4, "height": 4},
        ],
    },
    {
        "name": "Website & Product Analytics",
        "description": "User engagement, page performance, conversion funnels, and A/B test results",
        "widgets": [
            {"title": "Daily Active Users", "type": "metric", "config": json.dumps({"value": "14,800", "change": "+12%", "period": "vs last week", "color": "green"}), "position_x": 0, "position_y": 0, "width": 3, "height": 2},
            {"title": "Avg Session Duration", "type": "metric", "config": json.dumps({"value": "8.9 min", "change": "+0.8 min", "period": "vs last week", "color": "green"}), "position_x": 3, "position_y": 0, "width": 3, "height": 2},
            {"title": "Bounce Rate", "type": "metric", "config": json.dumps({"value": "31.5%", "change": "-3.2%", "period": "vs last month", "color": "green"}), "position_x": 6, "position_y": 0, "width": 3, "height": 2},
            {"title": "Pages per Session", "type": "metric", "config": json.dumps({"value": "7.2", "change": "+0.5", "period": "vs last month", "color": "green"}), "position_x": 9, "position_y": 0, "width": 3, "height": 2},
            {"title": "DAU Trend (14 Days)", "type": "line_chart", "config": json.dumps({"query_ref": "dau_trend"}), "position_x": 0, "position_y": 2, "width": 6, "height": 4},
            {"title": "Conversion Funnel", "type": "funnel_chart", "config": json.dumps({"query_ref": "conversion_funnel"}), "position_x": 6, "position_y": 2, "width": 6, "height": 4},
        ],
    },
]


REPORTS_DATA = [
    {
        "title": "Q2 2026 Business Performance Report",
        "description": "Comprehensive quarterly business review covering revenue, operations, and strategic initiatives",
        "html_content": """<!DOCTYPE html><html><head><title>Q2 2026 Business Performance Report</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b}.header{background:linear-gradient(135deg,#1e40af,#3b82f6);color:white;padding:48px 24px;text-align:center}.header h1{font-size:2rem;margin-bottom:8px}.content{max-width:1200px;margin:0 auto;padding:32px 24px}.section{background:white;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.section h2{font-size:1.25rem;margin-bottom:16px;color:#1e40af}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}.metric-card{background:#f1f5f9;border-radius:8px;padding:16px;text-align:center}.metric-value{font-size:1.5rem;font-weight:700;color:#1e40af}.metric-label{font-size:0.875rem;color:#64748b;margin-top:4px}.metric-change{font-size:0.875rem;margin-top:4px}.positive{color:#16a34a}.negative{color:#dc2626}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #e2e8f0}th{background:#f1f5f9;font-weight:600}.footer{text-align:center;padding:24px;color:#94a3b8;font-size:0.875rem}</style></head><body>
<div class="header"><h1>Q2 2026 Business Performance Report</h1><p>April - June 2026 | Prepared by DB-GPT Analytics</p></div>
<div class="content">
<div class="metrics"><div class="metric-card"><div class="metric-value">$2.78M</div><div class="metric-label">Q2 Revenue</div><div class="metric-change positive">+13.5% vs Q1</div></div><div class="metric-card"><div class="metric-value">$625K</div><div class="metric-label">Net Income</div><div class="metric-change positive">+43.7% vs Q1</div></div><div class="metric-card"><div class="metric-value">28,450</div><div class="metric-label">Active Customers</div><div class="metric-change positive">+8.2%</div></div><div class="metric-card"><div class="metric-value">72</div><div class="metric-label">NPS Score</div><div class="metric-change positive">+3 pts</div></div></div>
<div class="section"><h2>Revenue Analysis</h2><p>Q2 2026 delivered strong revenue growth of 13.5% over Q1, reaching $2.78M. The growth was driven primarily by Electronics (+18%) and the successful Summer Sale campaign. Net income grew at a faster rate (43.7%) due to improved operational efficiency and marketing ROI optimization.</p><table><thead><tr><th>Metric</th><th>Q1 2026</th><th>Q2 2026</th><th>Change</th></tr></thead><tbody><tr><td>Revenue</td><td>$2,450,000</td><td>$2,780,000</td><td class="positive">+13.5%</td></tr><tr><td>COGS</td><td>$980,000</td><td>$1,050,000</td><td>+7.1%</td></tr><tr><td>Gross Margin</td><td>60.0%</td><td>62.2%</td><td class="positive">+2.2pp</td></tr><tr><td>Net Income</td><td>$435,000</td><td>$625,000</td><td class="positive">+43.7%</td></tr></tbody></table></div>
<div class="section"><h2>Customer Metrics</h2><p>Customer acquisition increased 18% with 8,970 new customers added this quarter. The Referral Program showed the highest quality acquisition with $125.80 average first order value. Customer lifetime value for recent cohorts is trending positively.</p></div>
<div class="section"><h2>Operational Highlights</h2><p>Support team achieved 94.8% SLA compliance (+1.5% vs last month). Average response time decreased to 4.2 minutes. Inventory optimization reduced stockouts by 23%. Website conversion rate improved to 4.2% from 3.9%.</p></div>
</div><div class="footer">Generated by DB-GPT on 2026-06-20</div></body></html>""",
    },
    {
        "title": "Monthly Sales Report - June 2026",
        "description": "Detailed sales analysis including product performance, regional breakdown, and customer segments",
        "html_content": """<!DOCTYPE html><html><head><title>Monthly Sales Report - June 2026</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b}.header{background:linear-gradient(135deg,#059669,#10b981);color:white;padding:48px 24px;text-align:center}.header h1{font-size:2rem;margin-bottom:8px}.content{max-width:1200px;margin:0 auto;padding:32px 24px}.section{background:white;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.section h2{font-size:1.25rem;margin-bottom:16px;color:#059669}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #e2e8f0}th{background:#f1f5f9;font-weight:600}.footer{text-align:center;padding:24px;color:#94a3b8;font-size:0.875rem}.highlight{background:#ecfdf5;border-left:4px solid #10b981;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0}</style></head><body>
<div class="header"><h1>Monthly Sales Report</h1><p>June 2026 | Revenue: $262,000</p></div>
<div class="content">
<div class="section"><h2>Executive Summary</h2><div class="highlight"><strong>Key Highlight:</strong> June 2026 revenue of $262K represents a 6.9% increase over May ($245K) and 41.6% YoY growth. Strong performance across all product categories with Electronics leading at $118K.</div></div>
<div class="section"><h2>Top 10 Products</h2><table><thead><tr><th>Product</th><th>Revenue</th><th>Units</th><th>Avg Price</th></tr></thead><tbody><tr><td>MacBook Pro 16"</td><td>$124,500</td><td>83</td><td>$1,500</td></tr><tr><td>iPhone 15 Pro Max</td><td>$98,750</td><td>79</td><td>$1,249</td></tr><tr><td>Sony WH-1000XM5</td><td>$45,600</td><td>152</td><td>$300</td></tr><tr><td>Samsung Galaxy S24 Ultra</td><td>$41,200</td><td>34</td><td>$1,212</td></tr><tr><td>iPad Air M2</td><td>$38,900</td><td>65</td><td>$599</td></tr></tbody></table></div>
<div class="section"><h2>Regional Performance</h2><table><thead><tr><th>Region</th><th>Revenue</th><th>Orders</th><th>Growth</th></tr></thead><tbody><tr><td>North America</td><td>$1,170,000</td><td>11,500</td><td>+15.2%</td></tr><tr><td>Europe</td><td>$902,000</td><td>9,600</td><td>+12.8%</td></tr><tr><td>Asia Pacific</td><td>$646,000</td><td>7,350</td><td>+22.1%</td></tr><tr><td>Latin America</td><td>$223,000</td><td>2,480</td><td>+18.5%</td></tr></tbody></table></div>
</div><div class="footer">Generated by DB-GPT on 2026-06-20</div></body></html>""",
    },
    {
        "title": "Customer Support Quality Report",
        "description": "Support team performance, SLA compliance, and customer satisfaction analysis",
        "html_content": """<!DOCTYPE html><html><head><title>Customer Support Quality Report</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b}.header{background:linear-gradient(135deg,#7c3aed,#a78bfa);color:white;padding:48px 24px;text-align:center}.header h1{font-size:2rem;margin-bottom:8px}.content{max-width:1200px;margin:0 auto;padding:32px 24px}.section{background:white;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.section h2{font-size:1.25rem;margin-bottom:16px;color:#7c3aed}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px}.stat{background:#f5f3ff;border-radius:8px;padding:16px;text-align:center}.stat-value{font-size:1.5rem;font-weight:700;color:#7c3aed}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #e2e8f0}th{background:#f1f5f9;font-weight:600}.footer{text-align:center;padding:24px;color:#94a3b8;font-size:0.875rem}</style></head><body>
<div class="header"><h1>Customer Support Quality Report</h1><p>June 2026 | CSAT: 4.6/5.0</p></div>
<div class="content">
<div class="section"><h2>Key Metrics</h2><div class="grid"><div class="stat"><div class="stat-value">2,511</div><div>Tickets Resolved</div></div><div class="stat"><div class="stat-value">4.2 min</div><div>Avg First Response</div></div><div class="stat"><div class="stat-value">94.8%</div><div>SLA Compliance</div></div></div></div>
<div class="section"><h2>Agent Leaderboard</h2><table><thead><tr><th>Agent</th><th>Tickets</th><th>Avg Time</th><th>CSAT</th><th>FCR</th></tr></thead><tbody><tr><td>Maria Garcia</td><td>168</td><td>1.5 hrs</td><td>4.91</td><td>92%</td></tr><tr><td>Sarah Johnson</td><td>186</td><td>1.8 hrs</td><td>4.82</td><td>89%</td></tr><tr><td>Ahmed Khan</td><td>172</td><td>2.1 hrs</td><td>4.75</td><td>85%</td></tr><tr><td>Lisa Chen</td><td>149</td><td>1.9 hrs</td><td>4.79</td><td>87%</td></tr><tr><td>James Wilson</td><td>155</td><td>2.4 hrs</td><td>4.68</td><td>82%</td></tr></tbody></table></div>
<div class="section"><h2>Recommendations</h2><ul style="padding-left:20px;line-height:1.8"><li>Implement chatbot for Password Reset tickets (342/month, 0.5hr avg) to free agent capacity</li><li>Add size guide improvement for Fashion returns (19.8% return rate)</li><li>Hire 2 additional agents for Shipping Problems category (12.1hr avg resolution)</li><li>Create knowledge base articles for top 20 recurring questions</li></ul></div>
</div><div class="footer">Generated by DB-GPT on 2026-06-20</div></body></html>""",
    },
    {
        "title": "Marketing ROI Analysis - Q2 2026",
        "description": "Marketing channel performance, campaign ROI breakdown, and budget optimization recommendations",
        "html_content": """<!DOCTYPE html><html><head><title>Marketing ROI Analysis - Q2 2026</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b}.header{background:linear-gradient(135deg,#ea580c,#f97316);color:white;padding:48px 24px;text-align:center}.header h1{font-size:2rem;margin-bottom:8px}.content{max-width:1200px;margin:0 auto;padding:32px 24px}.section{background:white;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.section h2{font-size:1.25rem;margin-bottom:16px;color:#ea580c}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #e2e8f0}th{background:#f1f5f9;font-weight:600}.footer{text-align:center;padding:24px;color:#94a3b8;font-size:0.875rem}.insight{background:#fff7ed;border-left:4px solid #f97316;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0}</style></head><body>
<div class="header"><h1>Marketing ROI Analysis</h1><p>Q2 2026 | Total Spend: $124,500 | Revenue Attributed: $932,500</p></div>
<div class="content">
<div class="section"><h2>Channel Performance</h2><table><thead><tr><th>Channel</th><th>Spend</th><th>Revenue</th><th>ROI</th><th>CPA</th></tr></thead><tbody><tr><td>Email Marketing</td><td>$2,500</td><td>$89,000</td><td>3,460%</td><td>$2.81</td></tr><tr><td>Referral Program</td><td>$8,000</td><td>$156,000</td><td>1,850%</td><td>$15.38</td></tr><tr><td>Influencer</td><td>$15,000</td><td>$178,000</td><td>1,087%</td><td>$33.71</td></tr><tr><td>Google Ads</td><td>$25,000</td><td>$185,000</td><td>640%</td><td>$20.33</td></tr><tr><td>Meta Ads</td><td>$28,000</td><td>$133,000</td><td>375%</td><td>$27.89</td></tr></tbody></table></div>
<div class="section"><h2>Budget Recommendations</h2><div class="insight"><strong>Key Insight:</strong> Email marketing delivers 3,460% ROI at only $2.81 CPA. Recommend increasing email budget by 200% and reallocating 15% of Meta Ads budget to Referral Program.</div><table><thead><tr><th>Channel</th><th>Current</th><th>Recommended</th><th>Change</th></tr></thead><tbody><tr><td>Email</td><td>$2,500</td><td>$7,500</td><td>+200%</td></tr><tr><td>Referral</td><td>$8,000</td><td>$12,200</td><td>+52%</td></tr><tr><td>Meta Ads</td><td>$28,000</td><td>$23,800</td><td>-15%</td></tr><tr><td>Google Ads</td><td>$25,000</td><td>$25,000</td><td>0%</td></tr></tbody></table></div>
</div><div class="footer">Generated by DB-GPT on 2026-06-20</div></body></html>""",
    },
    {
        "title": "Inventory Health Report",
        "description": "Stock level analysis, reorder alerts, dead stock identification, and warehouse utilization",
        "html_content": """<!DOCTYPE html><html><head><title>Inventory Health Report</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8fafc;color:#1e293b}.header{background:linear-gradient(135deg,#0891b2,#06b6d4);color:white;padding:48px 24px;text-align:center}.header h1{font-size:2rem;margin-bottom:8px}.content{max-width:1200px;margin:0 auto;padding:32px 24px}.section{background:white;border-radius:12px;padding:24px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.section h2{font-size:1.25rem;margin-bottom:16px;color:#0891b2}.alert{background:#fef2f2;border-left:4px solid #ef4444;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #e2e8f0}th{background:#f1f5f9;font-weight:600}.footer{text-align:center;padding:24px;color:#94a3b8;font-size:0.875rem}</style></head><body>
<div class="header"><h1>Inventory Health Report</h1><p>As of June 20, 2026 | 8 Critical Alerts</p></div>
<div class="content">
<div class="section"><h2>Critical Stock Alerts</h2><div class="alert"><strong>Action Required:</strong> 8 products are below reorder point. Estimated reorder cost: ~$52K. Wireless Earbuds Pro critically low at 12 units (reorder point: 200).</div><table><thead><tr><th>SKU</th><th>Product</th><th>Stock</th><th>Reorder Point</th><th>Deficit</th></tr></thead><tbody><tr><td>SKU-1042</td><td>Wireless Earbuds Pro</td><td>12</td><td>200</td><td style="color:#ef4444;font-weight:700">-188</td></tr><tr><td>SKU-1589</td><td>Phone Case Premium</td><td>45</td><td>500</td><td style="color:#ef4444;font-weight:700">-455</td></tr><tr><td>SKU-4201</td><td>Mechanical Keyboard RGB</td><td>5</td><td>80</td><td style="color:#ef4444;font-weight:700">-75</td></tr><tr><td>SKU-2087</td><td>USB-C Hub 7-in-1</td><td>34</td><td>150</td><td style="color:#ef4444;font-weight:700">-116</td></tr></tbody></table></div>
<div class="section"><h2>Warehouse Utilization</h2><table><thead><tr><th>Warehouse</th><th>Capacity</th><th>Used</th><th>Utilization</th></tr></thead><tbody><tr><td>East Coast Warehouse</td><td>50,000 units</td><td>38,500</td><td>77%</td></tr><tr><td>Central Distribution</td><td>75,000 units</td><td>52,125</td><td>69.5%</td></tr><tr><td>West Coast Warehouse</td><td>40,000 units</td><td>34,800</td><td>87%</td></tr></tbody></table></div>
</div><div class="footer">Generated by DB-GPT on 2026-06-20</div></body></html>""",
    },
]


async def seed():
    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == "mzoraofficial@gmail.com"))
        user = result.scalar_one_or_none()
        if not user:
            print("ERROR: Default user not found! Run the app first to create it.")
            return

        user_id = user.id
        print(f"Found user: {user.email} (id: {user_id})")

        # Update user settings for Ollama
        user.ollama_base_url = "http://localhost:11434"
        user.ollama_model = "mistral"
        await db.commit()
        print("Updated user Ollama settings: mistral @ localhost:11434")

        # Clear existing dummy data
        await db.execute(text("DELETE FROM dashboard_widgets"))
        await db.execute(text("DELETE FROM dashboards WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM reports WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM queries WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM skills WHERE user_id = :uid"), {"uid": user_id})
        await db.execute(text("DELETE FROM datasources WHERE user_id = :uid"), {"uid": user_id})
        await db.commit()
        print("Cleared existing data")

        # Create Datasources
        ds_ids = []
        for ds in DATASOURCES:
            d = Datasource(id=uid(), user_id=user_id, **ds)
            db.add(d)
            ds_ids.append(d.id)
        await db.commit()
        print(f"Created {len(DATASOURCES)} datasources")

        # Create Queries
        query_ids = []
        for i, q_data in enumerate(QUERIES_DATA):
            ds_idx = q_data.pop("ds_idx")
            q = Query(
                id=uid(),
                user_id=user_id,
                datasource_id=ds_ids[ds_idx],
                created_at=past_date(random.randint(0, 30)),
                **q_data,
            )
            db.add(q)
            query_ids.append(q.id)
        await db.commit()
        print(f"Created {len(QUERIES_DATA)} queries with results")

        # Create Skills
        for s_data in SKILLS_DATA:
            s = Skill(
                id=uid(),
                user_id=user_id,
                is_public=random.choice([True, False]),
                created_at=past_date(random.randint(0, 60)),
                **s_data,
            )
            db.add(s)
        await db.commit()
        print(f"Created {len(SKILLS_DATA)} skills")

        # Create Dashboards with Widgets
        for d_data in DASHBOARDS_DATA:
            widgets_data = d_data.pop("widgets")
            dash = Dashboard(
                id=uid(),
                user_id=user_id,
                name=d_data["name"],
                description=d_data["description"],
                layout=json.dumps([{"i": str(i), "x": w["position_x"], "y": w["position_y"], "w": w["width"], "h": w["height"]} for i, w in enumerate(widgets_data)]),
                created_at=past_date(random.randint(0, 45)),
            )
            db.add(dash)
            await db.flush()

            for w_data in widgets_data:
                widget = DashboardWidget(
                    id=uid(),
                    dashboard_id=dash.id,
                    **w_data,
                )
                db.add(widget)
            d_data["widgets"] = widgets_data
        await db.commit()
        print(f"Created {len(DASHBOARDS_DATA)} dashboards with widgets")

        # Create Reports
        for r_data in REPORTS_DATA:
            report = Report(
                id=uid(),
                user_id=user_id,
                title=r_data["title"],
                description=r_data["description"],
                html_content=r_data["html_content"],
                query_ids=json.dumps(random.sample(query_ids, min(3, len(query_ids)))),
                share_token=uuid.uuid4().hex[:16],
                created_at=past_date(random.randint(0, 30)),
            )
            db.add(report)
        await db.commit()
        print(f"Created {len(REPORTS_DATA)} reports")

        print("\n=== SEED COMPLETE ===")
        print(f"  Datasources: {len(DATASOURCES)}")
        print(f"  Queries:     {len(QUERIES_DATA)}")
        print(f"  Skills:      {len(SKILLS_DATA)}")
        print(f"  Dashboards:  {len(DASHBOARDS_DATA)}")
        print(f"  Reports:     {len(REPORTS_DATA)}")
        print(f"  Total items: {len(DATASOURCES) + len(QUERIES_DATA) + len(SKILLS_DATA) + len(DASHBOARDS_DATA) + len(REPORTS_DATA)}")


if __name__ == "__main__":
    asyncio.run(seed())
