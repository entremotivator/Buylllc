import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Micro Business ROI Calculator", layout="wide")

# Title Section
st.title("Micro Business ROI Forecast App")
st.markdown("""
Welcome to the **Micro Business ROI Forecast Tool**. Use this app to model long-term returns 
from buying low-cost businesses, holding them, and selling them after a set number of years.

**Example Strategy:**
- Buy businesses for $99–$199 each
- Spend $50/year to maintain
- Sell for $10,000+ in 10 years

""")

# Sidebar Inputs
st.sidebar.header("Investment Setup")

num_businesses = st.sidebar.selectbox("How many businesses will you buy?", [10, 20, 50, 100, 200])
purchase_price = st.sidebar.selectbox("Purchase Price per Business ($)", [99, 149, 199])
annual_cost = st.sidebar.slider("Annual Cost per Business ($)", 10, 100, 50)
resale_value = st.sidebar.number_input("Expected Resale Value per Business", min_value=1000, max_value=100000, value=10000, step=500)
resale_year = st.sidebar.slider("Year to Sell Each Business", 3, 20, 10)

# Derived Values
total_years = resale_year
initial_investment = num_businesses * purchase_price
total_annual_cost = annual_cost * total_years * num_businesses
total_cost = initial_investment + total_annual_cost
total_revenue = resale_value * num_businesses
net_profit = total_revenue - total_cost
roi = (net_profit / total_cost) * 100
roi_per_business = ((resale_value - (purchase_price + annual_cost * resale_year)) / (purchase_price + annual_cost * resale_year)) * 100

# Layout
st.header("Investment Summary")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Initial Investment", f"${initial_investment:,}")
    st.metric("Annual Maintenance", f"${annual_cost * num_businesses:,}")
with col2:
    st.metric("Total Cost Over Time", f"${total_cost:,}")
    st.metric("Projected Revenue", f"${total_revenue:,}")
with col3:
    st.metric("Net Profit", f"${net_profit:,}")
    st.metric("Total ROI", f"{roi:.2f}%")

st.markdown("---")

# Yearly DataFrame Simulation
years = list(range(1, resale_year + 1))
cumulative_costs = [initial_investment + (i * annual_cost * num_businesses) for i in years]
revenue = [0 if i < resale_year else total_revenue for i in years]
profit = [revenue[i] - cumulative_costs[i] for i in range(len(years))]
roi_over_time = [(profit[i] / cumulative_costs[i]) * 100 for i in range(len(years))]

df = pd.DataFrame({
    "Year": years,
    "Cumulative Cost": cumulative_costs,
    "Projected Revenue": revenue,
    "Net Profit": profit,
    "ROI (%)": roi_over_time
})

# Graphs
st.subheader("Financial Projections Over Time")

tab1, tab2, tab3 = st.tabs(["📈 Revenue vs Cost", "💸 Net Profit Growth", "📊 ROI Over Time"])

with tab1:
    fig, ax = plt.subplots()
    ax.plot(df["Year"], df["Cumulative Cost"], label="Cumulative Cost", color="red", linewidth=2)
    ax.plot(df["Year"], df["Projected Revenue"], label="Revenue", color="green", linestyle="--", linewidth=2)
    ax.set_title("Cost vs Revenue")
    ax.set_xlabel("Year")
    ax.set_ylabel("USD")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Year"], df["Net Profit"], label="Net Profit", color="blue", linewidth=2)
    ax2.set_title("Net Profit Over Time")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("USD")
    ax2.axhline(0, color="gray", linestyle="--")
    ax2.grid(True)
    st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots()
    ax3.plot(df["Year"], df["ROI (%)"], label="ROI %", color="purple", linewidth=2)
    ax3.set_title("ROI Growth")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("ROI %")
    ax3.axhline(100, color="gray", linestyle="--", label="100% ROI")
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)

# ROI per business
st.markdown("### ROI Per Business Breakdown")
st.write(f"If each business is sold for **${resale_value:,}** in year {resale_year},")
st.write(f"and each one costs **${purchase_price:,}** + **${annual_cost * resale_year:,}** in maintenance:")
st.success(f"**ROI per Business = {roi_per_business:.2f}%**")

# Business strategy advice
st.markdown("---")
st.markdown("### Business Strategy Summary")
st.markdown("""
This strategy focuses on acquiring **micro businesses** or **digital assets** that require minimal upkeep but have future potential value.

**Business Types to Consider:**
- Newsletter/email list-based businesses
- Niche content websites or blogs
- Template stores (Gumroad, Etsy, Shopify)
- Micro SaaS apps or tools
- Educational courses or micro-consulting offers
- Print-on-demand brand stores

**Why This Works:**
- **Low acquisition costs** mean low risk per asset.
- **Minimal annual upkeep** allows holding multiple without active management.
- **High upside exit** provides great ROI if you build equity or sell to strategic buyers.

**Tips for Maximizing ROI:**
- Choose niches with recurring traffic or engagement.
- Create SOPs and automate business operations.
- Track performance using dashboards or VA support.
- Consider flipping early if value spikes before Year 10.
""")

# Download CSV
st.markdown("---")
st.download_button("Download Projection Data (CSV)", df.to_csv(index=False), "micro_business_projection.csv")

# Optional Markdown Report
st.markdown("### Markdown Summary Report")
st.code(f"""
Micro Business Investment Plan
------------------------------
Businesses Purchased: {num_businesses}
Purchase Price: ${purchase_price}
Annual Maintenance: ${annual_cost}
Years Held: {resale_year}
Expected Sale Price per Business: ${resale_value}

Initial Investment: ${initial_investment}
Total Cost (over {resale_year} years): ${total_cost}
Projected Revenue: ${total_revenue}
Net Profit: ${net_profit}
Overall ROI: {roi:.2f}%
ROI per Business: {roi_per_business:.2f}%
""", language="markdown")

