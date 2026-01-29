import requests
import datetime

# 1. API URLs
G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def get_api_data(url):
    try:
        # Cache-busting: adds current time to URL to force fresh data
        ts = int(datetime.datetime.now().timestamp())
        res = requests.get(f"{url}&t={ts}", timeout=15)
        res.raise_for_status()
        return res.json().get('data', {})
    except:
        return None

def main():
    gold = get_api_data(G_URL)
    silver = get_api_data(S_URL)

    # SAFETY: Stop if API is down to avoid breaking the site
    if not gold or not silver:
        print("API Error: Fetch failed. Keeping previous version.")
        return

    # 2. Extract Values
    g_buy = f"{float(gold.get('aura_buy_price', 0)):,.2f}"
    g_sell = f"{float(gold.get('aura_sell_price', 0)):,.2f}"
    s_buy = f"{float(silver.get('aura_buy_price', 0)):,.2f}"
    s_sell = f"{float(silver.get('aura_sell_price', 0)):,.2f}"
    
    # Get exact API time
    api_time = gold.get('created_at', "Live Update")

    # 3. HTML Template (Plain String - NO CSS Conflicts)
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>FDJ Live Rates</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
        body { background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: #1e293b; padding: 25px; border-radius: 20px; width: 350px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { text-align: center; color: #fbbf24; font-size: 22px; margin-bottom: 20px; }
        .metal { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 10px; }
        .row { display: flex; justify-content: space-between; margin: 5px 0; font-size: 18px; }
        .val { font-weight: bold; color: #fbbf24; }
        .label { color: #94a3b8; font-size: 13px; }
        .footer { text-align: center; font-size: 11px; color: #64748b; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>FDJ Live Rates</h1>
        <div class="metal">
            <div class="label">GOLD 24K (1g)</div>
            <div class="row"><span>Buy</span><span class="val">₹[G_BUY]</span></div>
            <div class="row"><span>Sell</span><span class="val">₹[G_SELL]</span></div>
        </div>
        <div class="metal">
            <div class="label">SILVER (1kg)</div>
            <div class="row"><span>Buy</span><span class="val">₹[S_BUY]</span></div>
            <div class="row"><span>Sell</span><span class="val">₹[S_SELL]</span></div>
        </div>
        <div class="footer">API Last Updated: [TIME]<br>Auto-Refresh in 30s</div>
    </div>
</body>
</html>
"""
    # 4. Fill Placeholders
    final_html = html_template.replace("[G_BUY]", g_buy)\
                               .replace("[G_SELL]", g_sell)\
                               .replace("[S_BUY]", s_buy)\
                               .replace("[S_SELL]", s_sell)\
                               .replace("[TIME]", api_time)

    # 5. Write to File
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("Dashboard Updated Successfully.")

if __name__ == "__main__":
    main()
