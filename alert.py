import os
import yfinance as yf
import pandas as pd
import ta
import smtplib
from email.mime.text import MIMEText

# ------------------------
# Paramètres
# ------------------------
SBF120_TICKERS = [
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


PERIOD = "6mo"   # période de données
INTERVAL = "1d"  # données journalières

# ------------------------
# Fonctions
# ------------------------
def check_conditions(ticker):
    data = yf.download(ticker, period=PERIOD, interval=INTERVAL)
    if data.empty:
        return False

    df = data.copy()
    df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()
    df["mm50"] = df["Close"].rolling(window=50).mean()
    df["mm200"] = df["Close"].rolling(window=200).mean()

    last = df.iloc[-1]

    cond_rsi = last["rsi"] > 30
    cond_macd = last["macd"] > last["signal"]
    cond_mm = last["mm50"] > last["mm200"]

    return cond_rsi and cond_macd and cond_mm

def send_email(subject, body):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

# ------------------------
# Script principal
# ------------------------
if __name__ == "__main__":
    matches = []

    for ticker in SBF120_TICKERS:
        try:
            if check_conditions(ticker):
                matches.append(ticker)
        except Exception as e:
            print(f"Erreur {ticker}: {e}")

    if matches:
        body = "Les entreprises suivantes remplissent les critères :\n\n"
        body += "\n".join(matches)
        send_email("Alerte SBF120", body)
        print("Email envoyé !")
    else:
        print("Aucune entreprise ne remplit les critères.")


