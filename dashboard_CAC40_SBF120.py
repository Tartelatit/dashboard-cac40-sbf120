import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import ta
from datetime import datetime
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Dashboard Actions Françaises", layout="wide")

# --- TITRE ---
# Le titre sera mis à jour dynamiquement plus tard si le SBF120 est filtré
#st.title("📊 Dashboard technique – Actions françaises")

# --- SÉLECTION DE L'ACTION ---
st.sidebar.header("⚙️ Paramètres")


# Liste des actions du CAC40 et du SBF120
cac40_actions = {
    "Air Liquide": "AI.PA",
    "Airbus": "AIR.PA",
    "Alstom": "ALO.PA",
    "ArcelorMittal": "MT.PA",
    "AXA": "CS.PA",
    "BNP Paribas": "BNP.PA",
    "Bouygues": "EN.PA",
    "Capgemini": "CAP.PA",
    "Carrefour": "CA.PA",
    "Crédit Agricole": "ACA.PA",
    "Danone": "BN.PA",
    "Dassault Systèmes": "DSY.PA",
    "Engie": "ENGI.PA",
    "EssilorLuxottica": "EL.PA",
    "Eurofins Scientific": "ERF.PA",
    "Hermès": "RMS.PA",
    "Kering": "KER.PA",
    "Legrand": "LR.PA",
    "L'Oréal": "OR.PA",
    "LVMH": "MC.PA",
    "Michelin": "ML.PA",
    "Orange": "ORA.PA",
    "Pernod Ricard": "RI.PA",
    "Publicis Groupe": "PUB.PA",
    "Renault": "RNO.PA",
    "Safran": "SAF.PA",
    "Saint-Gobain": "SGO.PA",
    "Sanofi": "SAN.PA",
    "Schneider Electric": "SU.PA",
    "Société Générale": "GLE.PA",
    "Stellantis": "STLA.PA",
    "STMicroelectronics": "STM.PA",
    "Teleperformance": "TEP.PA",
    "Thales": "HO.PA",
    "TotalEnergies": "TTE.PA",
    "Unibail-Rodamco-Westfield": "URW.PA",
    "Veolia": "VIE.PA",
    "Vinci": "DG.PA",
    "Vivendi": "VIV.PA",
    "Worldline": "WLN.PA"
}

# --- LISTE ACTIONS RECOMMANDÉES POUR AOÛT 2025 (PEA) ---
top_actions_pea_2025 = {
    "Air Liquide": "AI.PA",
    "AXA": "CS.PA",
    "BNP Paribas": "BNP.PA",
    "Bouygues": "EN.PA",
    "Crédit Agricole": "ACA.PA",
    "Engie": "ENGI.PA",
    "LVMH": "MC.PA",
    "Orange": "ORA.PA",
    "Stellantis": "STLA.PA",
    "Veolia": "VIE.PA",
    # Ajout des 5 de Café de la Bourse
    "M6 Métropole Télévision": "MMT.PA",
    "Vallourec": "VK.PA",
    "Électricité de Strasbourg": "ELEC.PA",  # Vérifie ce ticker
    "Neurones": "NRO.PA",
    "Trigano": "TRI.PA"
}

# Liste plus exhaustive du SBF120, incluant M6 Métropole Télévision
raw_sbf120_actions = {
    "Accor": "AC.PA", "ADP": "ADP.PA", "Air France-KLM": "AF.PA", "Albioma": "ABIO.PA",
    "Amundi": "AMUN.PA", "Arkema": "AKE.PA", "Atos": "ATO.PA", "BIC": "BB.PA",
    "BioMérieux": "BIM.PA", "Bolloré": "BOL.PA", "Bonduelle": "BON.PA", "Bureau Veritas": "BVI.PA",
    "Cie Plastic Omnium": "POM.PA", # Ticker mis à jour
    "Cie des Alpes": "CDA.PA", "Coface": "COFA.PA",
    "Credit Agricole": "ACA.PA",
    "Dassault Aviation": "AM.PA", "Elis": "ELIS.PA", "Eiffage": "FGR.PA",
    "Eramet": "ERA.PA", "Euronext": "ENX.PA", "Eutelsat Communications": "ETL.PA",
    "Faurecia": "EO.PA", "FDJ": "FDJ.PA", "Gecina": "GFC.PA", "Getlink": "GET.PA",
    "Icade": "ICAD.PA", "Imerys": "NK.PA", "IPSEN": "IPN.PA", "JCDecaux": "DEC.PA",
    "Klepierre": "LI.PA", "Maisons du Monde": "MDM.PA", "Mersen": "MRN.PA",
    "M6 Métropole Télévision": "MMT.PA", # Ajout de M6
    "Neoen": "NEOEN.PA", "Nexans": "NEX.PA", "Orpea": "ORP.PA",
    "Remy Cointreau": "RCO.PA", "Rexel": "RXL.PA", "Rubis": "RUI.PA",
    "Safran": "SAF.PA",
    "Saint-Gobain": "SGO.PA",
    "SEB": "SK.PA", "SES": "SES.PA", "Sodexo": "SW.PA", "Sopra Steria": "SOP.PA",
    "Spie": "SPIE.PA", "TF1": "TFI.PA", "Valeo": "FR.PA", "Verallia": "VRLA.PA",
    "Vilmorin & Cie": "RIN.PA", "Wendel": "MF.PA", "Worldline": "WLN.PA",
    "Zalando": "ZAL.DE",
    "EDF": "EDF.PA",
    "Sartorius Stedim Biotech": "DIM.PA",
    "Solutions 30": "S30.PA",
    "TechnipFMC": "FTI.PA",
    "Vetoquinol": "VETO.PA",
    "Virbac": "VIRB.PA",
    "Xavier Niel (Iliad)": "ILD.PA" # Ticker Iliad
}


# Fonction pour filtrer les actions SBF120 par dividende
@st.cache_data(ttl=3600) # Cache pendant 1 heure pour éviter des appels API répétés
def filter_sbf120_by_dividend(actions_dict_raw, min_dividend_yield_percent=2.0):
    filtered_actions = {}
    st.sidebar.write(f"Filtrage des actions SBF120 (rendement >= {min_dividend_yield_percent:.1f}%)...")
    progress_bar_filter = st.sidebar.progress(0)
    total_raw_actions = len(actions_dict_raw)
    
    for i, (company, ticker) in enumerate(actions_dict_raw.items()):
        try:
            stock_info = yf.Ticker(ticker).info
            dividend_yield = stock_info.get("dividendYield")
            
            if dividend_yield is not None:
                # Correction du "facteur 100": si le rendement est > 1.0, on le divise par 100
                # pour le normaliser en décimal avant la comparaison.
                if dividend_yield > 1.0:
                    dividend_yield /= 100.0
            
            if dividend_yield is not None and (dividend_yield * 100) >= min_dividend_yield_percent:
                filtered_actions[company] = ticker
        except Exception:
            # Ignorer les erreurs pour les actions individuelles lors du filtrage (ex: ticker non trouvé)
            pass
        progress_bar_filter.progress((i + 1) / total_raw_actions)
    
    progress_bar_filter.empty()
    st.sidebar.write("Filtrage terminé.")
    return filtered_actions

# Menu déroulant pour sélectionner l'index
selected_index = st.sidebar.selectbox(
    "📋 Choisir un index :",
    ["CAC40", "SBF120", "Top PEA Août 2025"],
    index=0  # CAC40 par défaut
)

sbf120_filtered_title_suffix = ""
if selected_index == "CAC40":
    actions_dict = cac40_actions
elif selected_index == "SBF120":
    MIN_DIVIDEND_YIELD = 2.0
    actions_dict = filter_sbf120_by_dividend(raw_sbf120_actions, MIN_DIVIDEND_YIELD)
    sbf120_filtered_title_suffix = f" (SBF120 filtré par dividende >= {MIN_DIVIDEND_YIELD:.1f}%)"
    if not actions_dict:
        st.warning(f"Aucune action du SBF120 n'a un rendement de dividende >= {MIN_DIVIDEND_YIELD:.1f}%. Affichage complet du SBF120.")
        actions_dict = raw_sbf120_actions
        sbf120_filtered_title_suffix = f" (SBF120 complet, aucun dividende >= {MIN_DIVIDEND_YIELD:.1f}%)"
elif selected_index == "Top PEA Août 2025":
    actions_dict = top_actions_pea_2025
    sbf120_filtered_title_suffix = " (Top 15 PEA recommandées – Août 2025)"


# Mettre à jour le titre principal du dashboard
st.title(f"📊 Dashboard technique – Actions françaises{sbf120_filtered_title_suffix}")


selected_company = st.sidebar.selectbox(
    "🏢 Choisir une action :",
    list(actions_dict.keys()),
    index=0  # Première action par défaut
)

ticker = actions_dict[selected_company]

# --- INITIALISATION DES VARIABLES AVANT LE BLOC TRY ---
# Ceci garantit que ces variables existent même si la récupération des données échoue
dividend_info = {}
dividend_rate = None
dividend_yield = None
ex_dividend_date = None
# Initialisation de df pour éviter NameError si le try block échoue avant sa définition
df = pd.DataFrame()


# --- RÉCUPÉRATION DES DONNÉES ---
st.write(f"📥 Récupération des données pour {selected_company} ({ticker})...")

# Ajouter un paramètre pour la période d'analyse
period_options = {
    "6 mois": "6mo",
    "1 an": "1y",
    "2 ans": "2y",
    "5 ans": "5y"
}

selected_period = st.sidebar.selectbox(
    "📅 Période d'analyse :",
    list(period_options.keys()),
    index=1  # 1 an par défaut
)

# Paramètres des moyennes mobiles
st.sidebar.subheader("📊 Moyennes mobiles")
ma_short = st.sidebar.slider("MA courte", 10, 100, 50, 5)
ma_long = st.sidebar.slider("MA longue", 100, 300, 200, 10)

display_period = period_options[selected_period]

try:
    # Création de l'objet Ticker pour l'action sélectionnée
    stock = yf.Ticker(ticker)

    # Récupérer plus de données pour avoir assez d'historique pour la MA200
    if display_period == "6mo":
        fetch_period = "2y"
        filter_months = 6
    elif display_period == "1y":
        fetch_period = "3y"
        filter_months = 12
    elif display_period == "2y":
        fetch_period = "5y"
        filter_months = 24
    else:  # 5y
        fetch_period = "10y"
        filter_months = 60
    
    # Utiliser l'objet Ticker pour télécharger l'historique
    df_full = stock.history(period=fetch_period, interval="1d")
    
    # Récupérer les informations sur les dividendes
    dividend_info = stock.info
    dividend_rate = dividend_info.get("dividendRate")
    dividend_yield = dividend_info.get("dividendYield")
    ex_dividend_date = dividend_info.get("exDividendDate")
    
    # Correction du "facteur 100" pour l'affichage principal
    if dividend_yield is not None and dividend_yield > 1.0:
        dividend_yield /= 100.0

    st.write(f"✅ Données complètes récupérées : {len(df_full)} lignes")

    if len(df_full) == 0:
        st.error(f"❌ Aucune donnée récupérée pour {selected_company}. Vérifiez le ticker ou la période.")
        st.info("Cela peut arriver si l'action est très récente ou si yfinance n'a pas de données pour cette période.")
        st.stop()

    df_full.dropna(inplace=True)

    # Si après dropna, le DataFrame est vide, on s'arrête
    if len(df_full) == 0:
        st.error(f"❌ Données insuffisantes après nettoyage pour {selected_company}. Impossible de poursuivre l'analyse.")
        st.stop()

    if isinstance(df_full.columns, pd.MultiIndex):
        df_full.columns = df_full.columns.droplevel(1)

    # Supprimer les informations de fuseau horaire de l'index du DataFrame
    # pour permettre une comparaison avec des timestamps naïfs (sans fuseau horaire).
    if df_full.index.tz is not None:
        df_full.index = df_full.index.tz_localize(None)

    close_series = df_full["Close"].squeeze()

    # Calculer les indicateurs sur TOUTES les données
    # Vérifier que close_series n'est pas vide avant de calculer les indicateurs
    if close_series.empty:
        st.error(f"❌ La série de prix de clôture est vide pour {selected_company}. Impossible de calculer les indicateurs.")
        st.stop()

    # Vérifier qu'il y a suffisamment de données pour les moyennes mobiles
    if len(close_series) < max(ma_short, ma_long):
        st.warning(f"⚠️ Pas assez de données pour calculer les moyennes mobiles MA{ma_short} et MA{ma_long}. Nécessite au moins {max(ma_short, ma_long)} points.")
        df_full[f"MA{ma_short}"] = pd.NA
        df_full[f"MA{ma_long}"] = pd.NA
    else:
        df_full[f"MA{ma_short}"] = close_series.rolling(window=ma_short).mean()
        df_full[f"MA{ma_long}"] = close_series.rolling(window=ma_long).mean()

    # Vérifier qu'il y a suffisamment de données pour le RSI (généralement 14 périodes)
    if len(close_series) < 14:
        st.warning(f"⚠️ Pas assez de données pour calculer le RSI. Nécessite au moins 14 points.")
        df_full["RSI"] = pd.NA
    else:
        df_full["RSI"] = ta.momentum.RSIIndicator(close_series).rsi()
    
    # MACD nécessite aussi une certaine longueur de données
    if len(close_series) < 26: # La plus longue période pour MACD est 26
        st.warning(f"⚠️ Pas assez de données pour calculer le MACD. Nécessite au moins 26 points.")
        df_full["MACD"] = pd.NA
        df_full["Signal"] = pd.NA
    else:
        macd = ta.trend.MACD(close_series)
        df_full["MACD"] = macd.macd()
        df_full["Signal"] = macd.macd_signal()

    # La cutoff_date est maintenant comparée à un index sans fuseau horaire.
    cutoff_date = pd.Timestamp.now() - pd.DateOffset(months=filter_months)
    df = df_full[df_full.index >= cutoff_date].copy()

    # Si le DataFrame filtré est vide, on s'arrête
    if len(df) == 0:
        st.error(f"❌ Aucune donnée disponible pour la période sélectionnée ({selected_period}) pour {selected_company}. Essayez une période plus longue.")
        st.stop()

    st.write(f"📊 Données affichées : {len(df)} lignes ({selected_period})")
    st.write(f"📅 Période d'affichage : {df.index.min().strftime('%Y-%m-%d')} à {df.index.max().strftime('%Y-%m-%d')}")
    st.write(f"📈 Cours actuel : {close_series.iloc[-1]:.2f} €")

    ma_long_available = df[f"MA{ma_long}"].dropna()
    if len(ma_long_available) > 0:
        st.write(f"✅ MA{ma_long} disponible sur {len(ma_long_available)} points pour la période d'affichage.")
    else:
        st.warning(f"⚠️ MA{ma_long} non disponible pour la période d'affichage (pas assez de données historiques ou toutes les valeurs sont NaN).")

except Exception as e:
    st.error(f"❌ Erreur lors de la récupération ou du traitement des données pour {selected_company} : {e}")
    st.info("💡 Cela peut être dû à un problème de connexion, un ticker incorrect, ou des données historiques manquantes/incomplètes.")
    st.stop()

# --- INTERPRÉTATION TECHNIQUE AUTOMATIQUE ---
st.subheader("🧠 Interprétation technique automatique")

def get_scalar_value(series, index=-1):
    """Extrait une valeur scalaire d'une Series pandas, gère les cas None/NaN."""
    try:
        if series.empty:
            return None
        val = series.iloc[index]
        if pd.isna(val):
            return None
        return float(val)
    except IndexError: # Si l'index est hors limites
        return None
    except Exception: # Pour toute autre erreur inattendue
        return None

# Vérifier si df est vide avant d'essayer d'accéder aux colonnes
if not df.empty and "RSI" in df.columns and not df["RSI"].isna().all():
    last_rsi = get_scalar_value(df["RSI"])
    last_macd = get_scalar_value(df["MACD"])
    last_signal = get_scalar_value(df["Signal"])
    ma_short_val = get_scalar_value(df[f"MA{ma_short}"])
    ma_long_val = get_scalar_value(df[f"MA{ma_long}"])
    close = get_scalar_value(df["Close"])

    # Vérifier que toutes les valeurs nécessaires sont disponibles pour l'interprétation
    if all(x is not None for x in [last_rsi, last_macd, last_signal, ma_short_val, ma_long_val, close]):
        if last_rsi is not None and last_macd is not None and last_signal is not None and ma_short_val is not None and ma_long_val is not None:
            if last_rsi < 40 and last_macd > last_signal and ma_short_val > ma_long_val:
                st.success("📈 Signal d'achat technique détecté : Survente (RSI), Croisement MACD haussier, Croisement MA haussier.")
            elif last_rsi > 70 or last_macd < last_signal:
                st.error("📉 Signal de vente ou surachat possible : Surachat (RSI) ou Croisement MACD baissier.")
            else:
                st.info("⏳ Situation neutre / consolidation probable : Pas de signal fort détecté.")
        else:
            st.warning("⚠️ Données d'indicateurs manquantes pour une interprétation technique complète.")
    else:
        st.warning("⚠️ Données insuffisantes pour une interprétation technique complète.")
    
    def format_value(val):
        return f"{val:.2f}" if val is not None else "N/A"

    st.markdown(f"""
    - **Cours actuel :** {format_value(close)} €
    - **RSI :** {format_value(last_rsi)}
    - **MACD :** {format_value(last_macd)}
    - **Signal MACD :** {format_value(last_signal)}
    - **MA{ma_short} :** {format_value(ma_short_val)}
    - **MA{ma_long} :** {format_value(ma_long_val)}
    """)
else:
    st.warning("⚠️ Données insuffisantes pour calculer tous les indicateurs ou pour l'interprétation technique.")

# --- TABLEAU RÉCAPITULATIF ---
st.subheader(f"📖 Tableau Récapitulatif de l'Index {selected_index}")

@st.cache_data(ttl=600) # Cache les données pendant 10 minutes
def get_full_analysis(actions_dict_for_analysis, ma_short, ma_long):
    analysis_data = []
    progress_bar = st.progress(0)
    total_actions = len(actions_dict_for_analysis)

    for i, (company, ticker) in enumerate(actions_dict_for_analysis.items()):
        try:
            df_temp = yf.download(ticker, period="3y", interval="1d", progress=False)
            if not df_temp.empty:
                # Appliquer la même logique de suppression de fuseau horaire ici
                if df_temp.index.tz is not None:
                    df_temp.index = df_temp.index.tz_localize(None)

                df_temp.dropna(inplace=True) # Nettoyer les NaN
                
                if df_temp.empty: # Si vide après nettoyage
                    analysis_data.append({
                        "Action": company, "Interprétation Technique": "Données insuffisantes", 
                        "RSI": "N/A", "MACD > Signal": "N/A", f"MA{ma_short} > MA{ma_long}": "N/A"
                    })
                    continue # Passer à l'action suivante

                close_series = df_temp["Close"].squeeze()
                
                # Vérifier que la série n'est pas vide avant de calculer les indicateurs
                if close_series.empty:
                    analysis_data.append({
                        "Action": company, "Interprétation Technique": "Série de prix vide", 
                        "RSI": "N/A", "MACD > Signal": "N/A", f"MA{ma_short} > MA{ma_long}": "N/A"
                    })
                    continue

                # Assurer qu'il y a suffisamment de points pour les calculs de MA et RSI
                # MACD nécessite 26 périodes, RSI 14, MA la longueur de la fenêtre
                min_data_points_required = max(ma_short, ma_long, 26) 
                if len(close_series) < min_data_points_required:
                     analysis_data.append({
                        "Action": company, "Interprétation Technique": "Pas assez de données pour indicateurs", 
                        "RSI": "N/A", "MACD > Signal": "N/A", f"MA{ma_short} > MA{ma_long}": "N/A"
                    })
                     continue

                rsi = ta.momentum.RSIIndicator(close_series).rsi().iloc[-1]
                macd = ta.trend.MACD(close_series)
                macd_val = macd.macd().iloc[-1]
                signal_val = macd.macd_signal().iloc[-1]
                ma_short_val = close_series.rolling(window=ma_short).mean().iloc[-1]
                ma_long_val = close_series.rolling(window=ma_long).mean().iloc[-1]

                interpretation = "Neutre"
                # Vérifier que les valeurs ne sont pas NaN avant la comparaison
                if pd.notna(rsi) and pd.notna(macd_val) and pd.notna(signal_val) and pd.notna(ma_short_val) and pd.notna(ma_long_val):
                    if rsi < 40 and macd_val > signal_val and ma_short_val > ma_long_val:
                        interpretation = "Achat"
                    elif rsi > 70 or macd_val < signal_val:
                        interpretation = "Vente / Surachat"
                else:
                    interpretation = "Indicateurs non calculables"
                
                analysis_data.append({
                    "Action": company,
                    "Interprétation Technique": interpretation,
                    "RSI": f"{rsi:.2f}" if pd.notna(rsi) else "N/A",
                    "MACD > Signal": "Oui" if pd.notna(macd_val) and pd.notna(signal_val) and macd_val > signal_val else ("Non" if pd.notna(macd_val) and pd.notna(signal_val) else "N/A"),
                    f"MA{ma_short} > MA{ma_long}": "Oui" if pd.notna(ma_short_val) and pd.notna(ma_long_val) and ma_short_val > ma_long_val else ("Non" if pd.notna(ma_short_val) and pd.notna(ma_long_val) else "N/A")
                })
            else:
                analysis_data.append({
                    "Action": company, "Interprétation Technique": "Données indisponibles", 
                    "RSI": "N/A", "MACD > Signal": "N/A", f"MA{ma_short} > MA{ma_long}": "N/A"
                })
        except Exception as e:
            # Capturer l'erreur spécifique pour un meilleur diagnostic si besoin
            analysis_data.append({
                "Action": company, "Interprétation Technique": f"Erreur ({str(e)[:40]}...)", # Limiter la longueur du message d'erreur
                "RSI": "N/A", "MACD > Signal": "N/A", f"MA{ma_short} > MA{ma_long}": "N/A"
            })
        
        time.sleep(0.1) # Pour éviter de surcharger l'API yfinance
        progress_bar.progress((i + 1) / total_actions)

    progress_bar.empty()
    return pd.DataFrame(analysis_data)

# Fonction de style pour surligner les lignes
def highlight_buy_signals(row):
    style = [''] * len(row)
    if row["Interprétation Technique"] == "Achat":
        style = ['background-color: #e6ffe6'] * len(row) # Vert clair
    return style

if st.button(f"Lancer l'analyse complète de l'index {selected_index}"):
    with st.spinner(f"Analyse en cours pour les {len(actions_dict)} actions..."):
        df_analysis = get_full_analysis(actions_dict, ma_short, ma_long)
        
        # Définir l'ordre des catégories pour le tri
        category_order = pd.CategoricalDtype(
            ["Achat", "Vente / Surachat", "Neutre", "Indicateurs non calculables", 
             "Données insuffisantes", "Série de prix vide", "Pas assez de données pour indicateurs", "Erreur"],
            ordered=True
        )
        df_analysis["Interprétation Technique"] = df_analysis["Interprétation Technique"].astype(category_order)
        
        # Trier le DataFrame
        df_analysis_sorted = df_analysis.sort_values(by="Interprétation Technique").set_index("Action")
        
        # Appliquer le style et afficher
        st.dataframe(df_analysis_sorted.style.apply(highlight_buy_signals, axis=1), use_container_width=True)

# --- INFORMATIONS SUR LES DIVIDENDES (DONNÉES EN TEMPS RÉEL) ---
st.subheader("💰 Informations sur les dividendes")

# Vérifier si dividend_info est disponible et non vide
if dividend_info and (dividend_rate is not None or dividend_yield is not None):
    if dividend_rate is not None:
        st.markdown(f"- **Taux de dividende (annuel) :** {dividend_rate:.2f} €")
    if dividend_yield is not None:
        # Affichage du rendement du dividende après normalisation
        st.markdown(f"- **Rendement du dividende :** {dividend_yield * 100:.2f} %")
    if ex_dividend_date is not None:
        # yfinance renvoie exDividendDate comme un timestamp Unix, le convertir en datetime
        date_str = datetime.fromtimestamp(ex_dividend_date).strftime('%d-%m-%Y')
        st.markdown(f"- **Dernière date de détachement :** {date_str}")
    else:
        st.markdown("- *Date de détachement non disponible.*")
else:
    st.markdown("Aucune information sur les dividendes n'est disponible pour cette action.")


# --- CHART PRINCIPAL ---
st.header(f"📈 Analyse détaillée de {selected_company}")
fig_price = go.Figure()

# Ajouter le cours de clôture
fig_price.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    mode='lines',
    name='Cours',
    line=dict(color='blue', width=2)
))

# Ajouter MA courte
# Vérifier que la colonne existe et n'est pas entièrement NaN
if f"MA{ma_short}" in df.columns and not df[f"MA{ma_short}"].isna().all():
    fig_price.add_trace(go.Scatter(
        x=df.index,
        y=df[f"MA{ma_short}"],
        mode='lines',
        name=f'MA{ma_short}',
        line=dict(color='orange', width=1)
    ))

# Ajouter MA longue
# Vérifier que la colonne existe et n'est pas entièrement NaN
if f"MA{ma_long}" in df.columns and not df[f"MA{ma_long}"].isna().all():
    fig_price.add_trace(go.Scatter(
        x=df.index,
        y=df[f"MA{ma_long}"],
        mode='lines',
        name=f'MA{ma_long}',
        line=dict(color='red', width=1)
    ))

fig_price.update_layout(
    title=f"Cours de {selected_company} avec moyennes mobiles",
    height=500,
    xaxis_title="Date",
    yaxis_title="Prix (€)"
)

# --- RSI ---
fig_rsi = go.Figure()
if "RSI" in df.columns and not df["RSI"].isna().all():
    fig_rsi.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode='lines', name='RSI'))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=40, line_dash="dash", line_color="green")
    fig_rsi.update_layout(title="RSI (Relative Strength Index)", height=300)
else:
    fig_rsi.add_annotation(text="Données RSI non disponibles", x=0.5, y=0.5, showarrow=False)

# --- MACD ---
fig_macd = go.Figure()
if "MACD" in df.columns and "Signal" in df.columns and not df["MACD"].isna().all() and not df["Signal"].isna().all():
    fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode='lines', name='MACD'))
    fig_macd.add_trace(go.Scatter(x=df.index, y=df["Signal"], mode='lines', name='Signal'))
    fig_macd.update_layout(title="MACD & Signal", height=300)
else:
    fig_macd.add_annotation(text="Données MACD non disponibles", x=0.5, y=0.5, showarrow=False)

# --- AFFICHAGE ---
st.plotly_chart(fig_price, use_container_width=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_rsi, use_container_width=True)
with col2:
    st.plotly_chart(fig_macd, use_container_width=True)
