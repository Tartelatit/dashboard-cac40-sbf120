import yfinance as yf
import pandas as pd
import smtplib
from email.message import EmailMessage

# --- Configuration ---
PERIOD = "6mo"
INTERVAL = "1d"
TICKERS = [
    "AC.PA",    # Accor
    "ADP.PA",   # Aéroports de Paris
    "AF.PA",    # Air France-KLM
    "AI.PA",    # Air Liquide
    "AIR.PA",   # Airbus
    "ALO.PA",   # Alstom
    "ATE.PA",   # Alten
    "AMUN.PA",  # Amundi
    "APAM.AS",  # Aperam (coté à Amsterdam)
    "MT.AS",    # ArcelorMittal (coté à Amsterdam)
    "ARG.PA",   # Argan
    "AKE.PA",   # Arkema
    "ATO.PA",   # Atos
    "CS.PA",    # AXA
    "BVI.PA",   # Bureau Veritas
    "CAP.PA",   # Capgemini
    "CA.PA",    # Crédit Agricole
    "BN.PA",    # Danone
    "DSY.PA",   # Dassault Systèmes
    "EN.PA",    # Bouygues
    "ENGI.PA",  # Engie
    "EL.PA",    # EssilorLuxottica
    "HO.PA",    # Thales
    "KER.PA",   # Kering
    "OR.PA",    # L'Oréal
    "MC.PA",    # LVMH
    "PUB.PA",   # Publicis
    "RI.PA",    # Pernod Ricard
    "RNO.PA",   # Renault
    "SAN.PA",   # Sanofi
    "SGO.PA",   # Saint-Gobain
    "SU.PA",    # Schneider Electric
    "GLE.PA",   # Société Générale
    "BNP.PA",   # BNP Paribas
    "ACA.PA",   # Crédit Agricole
    "VIV.PA",   # Vivendi
    "WLN.PA",   # Worldline
    "DG.PA",    # Vinci
    "ML.PA",    # Michelin
    "STLA.MI",  # Stellantis (coté à Milan)
    "STM.PA",   # STMicroelectronics
    "TTE.PA",   # TotalEnergies
    "ORP.PA",   # Orpea
    "UBI.PA",   # Ubisoft
    "PLW.PA",   # Planisware
    "RBT.PA",   # Robertet
    "MED.PA",   # MedinCell
    "VCT.PA",   # Vicat
    "MP.PA",    # Maurel & Prom
    "ES.PA",    # Esso
    "CAS.PA",   # Casino
    "S30.PA",   # Solutions 30
    "X-FAB.PA", # X-Fab
    "CLAI.PA",  # Clariane
    "FNAC.PA",  # Fnac Darty
    "VLT.PA",   # Voltalia
    "RCO.PA",   # Rothschild & Co
    "EDF.PA",   # EDF
    "KOR.PA",   # Korian
    "OVH.PA",   # OVH Groupe
    "BEN.PA",   # Bénéteau
    "MERS.PA",  # Mersen
    "MC.PA",    # McPhy Energy
    "SES.PA",   # SES-imagotag
    "ANT.PA",   # Antin Infrastructure Partners
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "QUA.PA",   # Quadient
    "ANT.PA",   # Antin Infrastructure Partners
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagotag
    "ALB.PA",   # Albioma
    "TEC.PA",   # Technicolor
    "EUC.PA",   # Europcar Mobility Group
    "GMB.PA",   # Green Mobility Holding
    "SOM.PA",   # Somfy
    "SES.PA",   # SES-imagot
]
EMAIL_SENDER = "leplus.jeremy@gmail.com"
EMAIL_PASSWORD = "prlg vowq fcew vmtr"  # mot de passe d’application si Gmail
EMAIL_RECEIVER = "leplus.jeremy@gmail.com"

# --- Fonctions ---
def get_close_series(ticker):
    try:
        data = yf.download(ticker, period=PERIOD, interval=INTERVAL, auto_adjust=True, progress=False)
        if data.empty:
            print(f"Erreur {ticker}: pas de données disponibles")
            return None
        close = data['Close']
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:,0]  # sécurité 1D
        return close
    except Exception as e:
        print(f"Erreur {ticker}: {e}")
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_moving_averages(series, windows=[50,200]):
    ma = {}
    for w in windows:
        ma[w] = series.rolling(w).mean()
    return ma

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Email envoyé !")

# --- Exécution ---
for ticker in TICKERS:
    close_prices = get_close_series(ticker)
    if close_prices is None:
        continue

    rsi_series = calculate_rsi(close_prices)
    macd_series, signal_series = calculate_macd(close_prices)
    ma_dict = calculate_moving_averages(close_prices)

    latest_rsi = rsi_series.iloc[-1]
    latest_macd = macd_series.iloc[-1]
    latest_signal = signal_series.iloc[-1]
    latest_ma50 = ma_dict[50].iloc[-1]
    latest_ma200 = ma_dict[200].iloc[-1]

    if latest_rsi < 30 and latest_macd > latest_signal > latest_ma50 > latest_ma200:
        print(f"Alerte {ticker}: conditions remplies !")
        send_email(
            subject=f"Alerte Bourse {ticker}",
            body=f"{ticker} a rempli les conditions : RSI={latest_rsi:.2f}, MACD={latest_macd:.2f}, MA50={latest_ma50:.2f}, MA200={latest_ma200:.2f}"
        )
