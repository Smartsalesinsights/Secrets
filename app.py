
from openai import OpenAI
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import datetime

# ✅ Initialize OpenAI client using new SDK syntax
client = OpenAI("sk-xxxxxxxxxxxxxxxxxxxxxxx")

st.set_page_config(page_title="SmartSales Insight", layout="centered")
st.title("📊 SmartSales Insight")
st.markdown("Upload your sales Excel/CSV file and get AI-powered insights + charts + PDF report")

uploaded_file = st.file_uploader("Upload Sales File (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")
    st.dataframe(df.head())

    if 'Date' in df.columns and 'Sales' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        monthly = df.groupby(df['Date'].dt.to_period("M")).sum(numeric_only=True).reset_index()
        monthly['Date'] = monthly['Date'].astype(str)
        st.subheader("📅 Monthly Sales Trend")
        fig = px.line(monthly, x='Date', y='Sales', title="Sales Over Time")
        st.plotly_chart(fig)

    if 'Product' in df.columns and 'Sales' in df.columns:
        product_sales = df.groupby('Product')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
        st.subheader("🏆 Top 10 Products")
        fig2 = px.bar(product_sales, x='Product', y='Sales', title="Top Products")
        st.plotly_chart(fig2)

    if st.button("🔍 Generate AI Insights"):
        summary = df.describe(include='all').to_string()
        prompt = f"""
        Analyze the following sales data summary and provide:
        1. Key sales trends and insights
        2. Top-performing and underperforming products or regions
        3. Business recommendations to improve sales

       Data Summary:
        {summary}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            insight = response.choices[0].message.content
            st.subheader("🤖 AI-Powered Insights")
            st.text_area("Insights", insight, height=300)
            def export_to_pdf(insight_text):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="SmartSales Insight Report", ln=True, align='C')
                pdf.cell(200, 10, txt=str(datetime.datetime.now().date()), ln=True, align='C')
                pdf.ln(10)
                for line in insight_text.split('\n'):
                    pdf.multi_cell(0, 10, line)
                pdf_path = "sales_insights.pdf"
                pdf.output(pdf_path)
                return pdf_path

            if st.button("📥 Download PDF Report"):
                path = export_to_pdf(insight)
                with open(path, "rb") as f:
                    st.download_button("Download PDF", f, file_name="sales_insights.pdf")

        except Exception as e:
            st.error(f"OpenAI API Error: {e}")
else:
    st.info("Please upload an Excel or CSV file to get started.")
