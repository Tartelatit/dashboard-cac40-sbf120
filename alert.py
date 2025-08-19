import yfinance as yf
import pandas as pd
import smtplib
from email.message import EmailMessage

# --- Configuration ---
PERIOD = "6mo"
INTERVAL = "1d"
TICKERS = [
    # CAC 40 (les 40 plus grandes capitalisations)
    'AC.PA',      # Accor
    'ACA.PA',     # Crédit Agricole
    'AI.PA',      # Air Liquide
    'AIR.PA',     # Airbus
    'AKE.PA',     # Arkema
    'BN.PA',      # Danone
    'BNP.PA',     # BNP Paribas
    'CA.PA',      # Carrefour
    'CAP.PA',     # Capgemini
    'CS.PA',      # AXA
    'DG.PA',      # Vinci
    'DSY.PA',     # Dassault Systemes
    'ENGI.PA',    # Engie
    'EL.PA',      # EssilorLuxottica
    'FP.PA',      # TotalEnergies
    'GLE.PA',     # Société Générale
    'HO.PA',      # Thales
    'KER.PA',     # Kering
    'LHN.PA',     # LafargeHolcim
    'LR.PA',      # Legrand
    'MC.PA',      # LVMH
    'ML.PA',      # Michelin
    'OR.PA',      # L'Oréal
    'ORA.PA',     # Orange
    'PUB.PA',     # Publicis
    'RI.PA',      # Pernod Ricard
    'RMS.PA',     # Hermès
    'RNO.PA',     # Renault
    'SAF.PA',     # Safran
    'SAN.PA',     # Sanofi
    'SGO.PA',     # Saint-Gobain
    'SU.PA',      # Schneider Electric
    'STM.PA',     # STMicroelectronics
    'TEP.PA',     # Teleperformance
    'STLAM.PA',   # Stellantis (ex Peugeot)
    'URW.PA',     # Unibail-Rodamco-Westfield
    'VIE.PA',     # Veolia
    'VIV.PA',     # Vivendi
    'WLN.PA',     # Worldline

    # CAC Next 20 et valeurs moyennes importantes
    'ADP.PA',     # Aéroports de Paris
    'AF.PA',      # Air France-KLM
    'ALO.PA',     # Alstom
    'BIG.PA',     # Nacon (ex-BigBen)
    'EN.PA',      # Bouygues
    'COV.PA',     # Covivio
    'ELIS.PA',    # Elis
    'ERF.PA',     # Eurofins Scientific
    'FNAC.PA',    # Fnac Darty
    'GET.PA',     # Getlink
    'GTT.PA',     # GTT
    'IPN.PA',     # Ipsen
    'JCQ.PA',     # Jacquet Metals
    'KN.PA',      # Kone (France)
    'MMB.PA',     # Maisons du Monde
    'NEX.PA',     # Nexity
    # Autres valeurs importantes du SBF 120
    'BIM.PA',     # Biomerieux
    'BVI.PA',     # Bureau Veritas
    'CNP.PA',     # CNP Assurances
    'EDF.PA',     # EDF
    'FDJ.PA',     # FDJ
    'FFP.PA',     # FFP
    'ING.PA',     # Ingenico (si encore coté)
    'JCD.PA',     # JCDecaux
    'LG.PA',      # Lagardère
    'NANO.PA',    # Nanobiotix
    'OVH.PA',     # OVHcloud
    'SCR.PA',     # Scor
    'SESG.PA',    # Séché Environnement
    'SPIE.PA',    # Spie
    'UBI.PA',     # Ubisoft
    'VAL.PA',     # Vallourec
    'VIRP.PA',    # Virbac
    'NEX.PA',     # Nexans
    'TFI.PA',     # TF1
    'AKW.PA',     # Akwel
    'AM.PA',      # Dassault Aviation
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




