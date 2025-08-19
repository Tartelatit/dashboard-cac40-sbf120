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
    "ACCOR.PA", "ADP.PA", "AIR.FRANCE-KLM.PA", "AIR.LIQUIDE.PA", "AIRBUS.PA",
    "ALSTOM.PA", "ALTEN.PA", "AMUNDI.PA", "APERAM.PA", "ARCELORMITTAL.PA",
    "ARGAN.PA", "ARKEMA.PA", "ATOS.PA", "AXA.PA", "AYVENS.PA", "BENETEAU.PA",
    "BIC.PA", "BIOMERIEUX.PA", "BNP.PARIBAS.PA", "BOLLORE.PA", "BOUYGUES.PA",
    "BUREAU.VERITAS.PA", "CAPGEMINI.PA", "CARMILA.PA", "CARREFOUR.PA",
    "CLARIANE.PA", "COFACE.PA", "COVIVIO.PA", "CREDIT.AGRICOLE.PA", "DANONE.PA",
    "DASSAULT.AVIATION.PA", "DASSAULT.SYSTEMES.PA", "DERICHEBOURG.PA",
    "EDENRED.PA", "EIFFAGE.PA", "ELIOR.PA", "ELIS.PA", "ENGIE.PA", "ERAMET.PA",
    "ESSILORLUXOTTICA.PA", "ESSO.PA", "EURAZEO.PA", "EUROFINS.SCIENT.PA",
    "EURONEXT.PA", "FDJ.PA", "FORVIA.PA", "GTT.PA", "GECINA.PA", "GETLINK.PA",
    "HERMES.INTL.PA", "ICADE.PA", "ID.LOGISTICS.GROUP.PA", "IMERYS.PA",
    "INTERPARFUMS.PA", "IPSEN.PA", "IPSOS.PA", "JCDECAUX.PA", "KERING.PA",
    "KLEPIERRE.PA", "L.OREAL.PA", "LEGRAND.PA", "LVMH.PA", "MAUREL.ET.PROM.PA",
    "MEDINCELL.PA", "MERCIALYS.PA", "MERSEN.PA", "METROPOLE.TV.PA",
    "MICHELIN.PA", "NEOEN.PA", "NEXANS.PA", "NEXITY.PA", "OPMOBILITY.PA",
    "ORANGE.PA", "PERNOD.RICARD.PA", "PLANISWARE.PA", "PLUXEE.PA",
    "PUBLICIS.GROUPE.PA", "REMY.COINTREAU.PA", "RENAULT.PA", "REXEL.PA",
    "ROBERTET.PA", "RUBIS.PA", "SEB.PA", "SAFRAN.PA", "SAINT.GOBAIN.PA",
    "SANOFI.PA", "SARTORIUS.STED.BIO.PA", "SCHNEIDER.ELECTRIC.PA",
    "SCOR.PA", "SES.PA", "SOCIETE.GENERALE.PA", "SODEXO.PA", "SOITEC.PA",
    "SOLVAY.PA", "SOPRA.STERIA.PA", "SPIE.PA", "STELLANTIS.PA",
    "STMICROELECTRONICS.PA", "TECHNIP.ENERGIES.PA", "TELEPERFORMANCE.PA",
    "TF1.PA", "THALES.PA", "TOTALENERGIES.PA", "TRIGANO.PA",
    "UBISOFT.PA", "UNIBAIL-RODAMCO.PA", "VALEO.PA", "VALLOUREC.PA",
    "VALNEVA.PA", "VEOLIA.ENVIRON.PA", "VERALLIA.PA", "VICAT.PA",
    "VINCI.PA", "VIRBAC.PA", "VIVENDI.PA", "WENDEL.PA", "WORLDLINE.PA"
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

