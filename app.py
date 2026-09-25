import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import io

# ---------------------------------------------------------
# 1. CONFIGURARE PAGINĂ & DESIGN ENTERPRISE
# ---------------------------------------------------------
st.set_page_config(
    page_title="GlucoFit Clinical AI Pro - Tîrnăveanu Ionuț Alexandru",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg, #0f766e, #0284c7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { font-size: 1.1rem; color: #475569; font-weight: 500; }
    .card-box { background: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .metric-box { background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%); color: white; padding: 20px; border-radius: 14px; text-align: center; box-shadow: 0 4px 12px rgba(15,118,110,0.2); }
    .badge-pill { background-color: #f1f5f9; color: #0f766e; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; display: inline-block; margin: 2px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BAZA DE DATE CLINICE: PACIENT & SCHEMA DE TRATAMENT
# ---------------------------------------------------------
PATIENT_PROFILE = {
    "nume": "Tîrnăveanu Ionuț Alexandru",[span_4](start_span)[span_4](end_span)[span_5](start_span)[span_5](end_span)
    "varsta": 38,[span_6](start_span)[span_6](end_span)[span_7](start_span)[span_7](end_span)
    "cnp": "1871225160028",[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span)
    "data_nasterii": "25.12.1987",[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span)
    "telefon": "0730291021",[span_12](start_span)[span_12](end_span)[span_13](start_span)[span_13](end_span)
    "adresa": "București",[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span)
    "medic_curant": "Dr. Ciobanu Anda / Dr. Parasca Diana Maria",[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)
    "data_reteta": "11.09.2026",[span_18](start_span)[span_18](end_span)[span_19](start_span)[span_19](end_span)
    "greutate_curenta": 78.5,
    "inaltime": 178,
    "obiectiv_greutate": 74.0,
    "tratament_farmacologic": [
        {"id": 1, "medicament": "Lagosa 150 mg", "doza": "1 - 0 - 1", "orar": "Dimineața și Seara, după masă", "rol": "Protecție și regenerare hepatică"},[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)
        {"id": 2, "medicament": "Lipantil Nano 145 mg", "doza": "- 1 -", "orar": "La Prânz, după masă", "rol": "Scădere trigliceride / dislipidemie mixtă"},[span_22](start_span)[span_22](end_span)[span_23](start_span)[span_23](end_span)
        {"id": 3, "medicament": "Sortis 20 mg", "doza": "- - 1", "orar": "Seara, după masă", "rol": "Control colesterolemie LDL / stabiliere placă ateromatosă"},[span_24](start_span)[span_24](end_span)[span_25](start_span)[span_25](end_span)
        {"id": 4, "medicament": "Omacor 1000 mg", "doza": "1 1 1", "orar": "Dimineața, Prânz, Seara, după masă", "rol": "Acizi grași polinesaturați Omega-3 / cardioprotecție"},[span_26](start_span)[span_26](end_span)[span_27](start_span)[span_27](end_span)
        {"id": 5, "medicament": "Siofor 1000 mg (Metformină)", "doza": "1 - 1", "orar": "Dimineața și Seara, după masă", "rol": "Sensibilitate la insulină / reducerea gluconeogenezei hepatice"},[span_28](start_span)[span_28](end_span)[span_29](start_span)[span_29](end_span)
        {"id": 6, "medicament": "Diaprel MR 60 mg", "doza": "1 - -", "orar": "Dimineața, înainte de masă", "rol": "Secretogog de insulină cu acțiune prelungită (control glicemie à jeun)"},[span_30](start_span)[span_30](end_span)[span_31](start_span)[span_31](end_span)
        {"id": 7, "medicament": "Larginina 1000 mg", "doza": "- 1 -", "orar": "La Prânz, 10 zile / lună", "rol": "Oxid nitric / vasodilatație și suport vascular"},[span_32](start_span)[span_32](end_span)[span_33](start_span)[span_33](end_span)
        {"id": 8, "medicament": "Atacand 8 mg", "doza": "- - 1", "orar": "Seara, după masă", "rol": "Blocant al receptorilor de angiotensină II / protecție renală și TA"},[span_34](start_span)[span_34](end_span)[span_35](start_span)[span_35](end_span)
        {"id": 9, "medicament": "Nebilet 5 mg", "doza": "1/2 - -", "orar": "Dimineața, după masă", "rol": "Beta-blocant cardioselectiv / ritm cardiac și TA"},[span_36](start_span)[span_36](end_span)[span_37](start_span)[span_37](end_span)
        {"id": 10, "medicament": "Aspenter 75 mg", "doza": "- 1 -", "orar": "La Prânz, după masă", "rol": "Antiagregant plachetar / profilaxie cardiovasculară"}[span_38](start_span)[span_38](end_span)[span_39](start_span)[span_39](end_span)
    ]
}

# ---------------------------------------------------------
# 3. BAZA EXTINSĂ DE REȚETE CLINICE & ÎNLOCUITORI INTELIGENȚI
# ---------------------------------------------------------
CLINICAL_RECIPES_DATABASE = [
    {
        "id": 1,
        "titlu": "Somon la cuptor cu crustă de migdale și sparanghel verde",
        "categorie": "Prânz / Cină",
        "calorii": 420,
        "carbi_net": 4.2,
        "indice_glicemic": 15,
        "satietate": 9.8,
        "ingrediente": [
            {"nume": "File de somon proaspăt (200g)", "inlocuitor": "Păstrăv eviscerat, file de doradă sau file de cod alb."},
            {"nume": "Sparanghel verde (150g)", "inlocuitor": "Broccoli aburit, dovlecei la grătar sau fasole verde subțire."},
            {"nume": "Făină de migdale (30g)", "inlocuitor": "Făină de in măcinată sau nuci românești măcinate fin."},
            {"nume": "Ulei de măsline extra virgin (15ml)", "inlocuitor": "Ulei de avocado presat la rece sau unt clarificat (ghee)."}
        ],
        "beneficiu_diabet": "Omega-3 pur scade inflamația sistemică; proteinele curate nu declanșează nicio eliberare de insulină.",
        "instructiuni": "Se marinează somonul în ulei de măsline, se acoperă cu crusta din făină de migdale și se dă la cuptor la 180°C timp de 18 minute alături de sparanghel."
    },
    {
        "id": 2,
        "titlu": "Salată Mediteraneană cu Pui Crocant și Avocado",
        "categorie": "Prânz Principal",
        "calorii": 350,
        "carbi_net": 5.5,
        "indice_glicemic": 10,
        "satietate": 9.2,
        "ingrediente": [
            {"nume": "Piept de pui gril (150g)", "inlocuitor": "File de curcan, tofu ferm sau creveți trași la tigaie."},
            {"nume": "Avocado Hass copt (100g)", "inlocuitor": "Măsline kalamata fără sâmburi sau nuci pecan."},
            {"nume": "Mix salată verde / rucola (100g)", "inlocuitor": "Spanac baby sau varză fin tăiată."},
            {"nume": "Oțet de mere organic cu mamă (15ml)", "inlocuitor": "Suc proaspăt de lămâie sau oțet balsamic vechi (fără zahăr adăugat)."}
        ],
        "beneficiu_diabet": "Oțetul de mere reduce semnificativ indicele glicemic al întregii mese prin întârzierea golirii gastrice.",
        "instructiuni": "Se taie puiul fâșii, se combină cu salata verde și feliile de avocado. Se asezonează cu ulei de măsline și oțet de mere."
    },
    {
        "id": 3,
        "titlu": "Budincă de Chia cu Scorțișoară Ceylon și Fructe de Pădure",
        "categorie": "Gustare / Poftă de Dulce",
        "calorii": 220,
        "carbi_net": 6.0,
        "indice_glicemic": 20,
        "satietate": 9.5,
        "ingrediente": [
            {"nume": "Semințe de chia (30g)", "inlocuitor": "Semințe de in măcinate sau semințe de psyllium husk."},
            {"nume": "Lapte de migdale neîndulcit (200ml)", "inlocuitor": "Lapte de cocos light din cutie sau lapte de nuci pecan."},
            {"nume": "Fructe de pădure congelate/proaspete (50g)", "inlocuitor": "Zmeură, mure sau afine sălbatice."},
            {"nume": "Eritritol pur sau Stevia (1 linguriță)", "inlocuitor": "Extract pur de călugăr (Monk Fruit) sau Xilitol."}
        ],
        "beneficiu_diabet": "Fibrele solubile din chia formează un gel care blochează absorbția bruscă a carbohidraților, potolind pofta de dulce.",
        "instructiuni": "Se amestecă semințele de chia cu laptele de migdale și eritritolul. Se lasă la frigider cel puțin 3 ore, apoi se adaugă fructele de pădure deasupra."
    },
    {
        "id": 4,
        "titlu": "Tocăniță Fragedă de Vită cu Piure de Conopidă și Unt",
        "categorie": "Prânz / Cină",
        "calorii": 480,
        "carbi_net": 8.1,
        "indice_glicemic": 22,
        "satietate": 9.9,
        "ingrediente": [
            {"nume": "Carne de vită slabă (mușchi/pulpă) (200g)", "inlocuitor": "Carne slabă de curcan sau pulpă de porc degresată."},
            {"nume": "Conopidă proaspătă (250g)", "inlocuitor": "Napi fierți sau țelină bulb fiartă în cantitate moderată."},
            {"nume": "Unt 82% grăsimi (20g)", "inlocuitor": "Ulei de cocos virgin sau ghee."},
            {"nume": "Ceapă și usturoi pentru aromă", "inlocuitor": "Praz tocat mărunt sau praf de usturoi organic."}
        ],
        "beneficiu_diabet": "Înlocuirea cartofului clasic cu conopida elimină complet carbohidrații rafinați, oferind textura cremoasă dorită.",
        "instructiuni": "Carnea se înăbușă lent. Conopida fiartă se pasează cu untul și mirodenii până devine piure fin."
    }
]

# ---------------------------------------------------------
# 4. SIDEBAR & NAVIGARE PRINCIPALĂ
# ---------------------------------------------------------
st.sidebar.markdown(f"### 🛡️ Panel de Control")
st.sidebar.info(f"**Pacient:** {PATIENT_PROFILE['nume']}\n\n**Vârsta:** {PATIENT_PROFILE['varsta']} ani[span_40](start_span)[span_40](end_span)[span_41](start_span)[span_41](end_span)\n\n**CNP:** {PATIENT_PROFILE['cnp']}")

rol_utilizator = st.sidebar.radio("Selectează Rolul:", ["Alex (Admin & Pacient)", "Utilizator Standard"])

meniu_principal = st.sidebar.selectbox("Navigare Modul:", [
    "🩺 Schema de Tratament & Alerte Farmacologice",
    "🍳 Rețete Clinice Avanasate & Înlocuitori",
    "📈 Simulator Glicemie Postprandială & Slăbit",
    "🏆 Gamification, XP & Realizări",
    "📄 Jurnal Medical & Export Raport PDF"
])

# ---------------------------------------------------------
# MODULUL 1: SCHEMA DE TRATAMENT & ALERTE
# ---------------------------------------------------------
if meniu_principal == "🩺 Schema de Tratament & Alerte Farmacologice":
    st.markdown('<p class="main-title">🩺 Schema de Tratament Medical Activă</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Prescripție medicală oficială emisă la data de {PATIENT_PROFILE["data_reteta"]} de către {PATIENT_PROFILE["medic_curant"]}.</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="metric-box"><h3>78.5 kg</h3><p>Greutate Curentă</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-box"><h3>-4.5 kg</h3><p>Obiectiv Lunar</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-box"><h3>118 mg/dL</h3><p>Glicemie Medie Țintă</p></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric-box"><h3>10</h3><p>Medicamente Active</p></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Tabelul Oficial al Medicamentelor Prescrise")
    df_meds = pd.DataFrame(PATIENT_PROFILE["tratament_farmacologic"])
    st.dataframe(df_meds, use_container_width=True)

    st.markdown("### ⚡ Alerte Clinice & Reguli de Asociere Cronologică")
    st.warning("""
    - **Diaprel MR 60 mg:** Se administrează **în mod obligatoriu înainte de masă** (dimineața) pentru a stimula secreția de insulină în momentul sosirii glucozei[span_42](start_span)[span_42](end_span)[span_43](start_span)[span_43](end_span).
    - **Siofor 1000 mg (Metformină):** Se ia **după masă** (dimineața și seara) pentru a reduce intoleranța gastrică[span_44](start_span)[span_44](end_span)[span_45](start_span)[span_45](end_span).
    - **Larginina 1000 mg:** Are caracter ciclic — se ia **10 zile pe lună**, la prânz, după masă[span_46](start_span)[span_46](end_span)[span_47](start_span)[span_47](end_span).
    - **Protecție Hepatică & Cardiovasculară:** Lagosa, Lipantil Nano, Sortis, Omacor, Atacand, Nebilet și Aspenter sunt sincronizate corect pentru a susține profilul lipidic, tensiunea arterială și endoteliul vascular[span_48](start_span)[span_48](end_span)[span_49](start_span)[span_49](end_span).
    """)

# ---------------------------------------------------------
# MODULUL 2: REȚETE CLINICE & ÎNLOCUITORI
# ---------------------------------------------------------
elif meniu_principal == "🍳 Rețete Clinice Avanasate & Înlocuitori":
    st.markdown('<p class="main-title">🍳 Rețete Clinice Optimizate Anti-Spike</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Bază de date inteligentă cu alternative automate pentru fiecare ingredient în parte.</p>', unsafe_allow_html=True)

    search_term = st.text_input("🔍 Caută rețetă, ingredient sau mod de preparare...", "")

    for r in CLINICAL_RECIPES_DATABASE:
        if search_term.lower() in r["titlu"].lower() or any(search_term.lower() in ing["nume"].lower() for ing in r["ingrediente"]):
            st.markdown(f"""
            <div class="card-box">
                <h3>{r['titlu']}</h3>
                <p><b>Categorie:</b> {r['categorie']} | <span style="color:#059669; font-weight:bold;">Indice Glicemic: {r['indice_glicemic']}</span> | <b>Sațietate:</b> {r['satietate']}/10</p>
                <p>🔥 <b>Calorii:</b> {r['calorii']} kcal | 🌾 <b>Carbohidrați Neciți:</b> {r['carbi_net']}g</p>
                <p>💡 <b>Beneficiu Metabolic:</b> {r['beneficiu_diabet']}</p>
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 12px 0;">
                <h4>🛒 Ingrediente & Sugestii de Înlocuire:</h4>
            """, unsafe_allow_html=True)
            
            for ing in r["ingrediente"]:
                st.markdown(f"- **{ing['nume']}** ➔ *Înlocuitor recomandat:* {ing['inlocuitor']}")
                
            st.markdown(f"""
                <p style="margin-top: 12px;"><b>Mod de preparare:</b> {r['instructiuni']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULUL 3: SIMULATOR GLICEMIE & PREDICȚIE SLĂBIT
# ---------------------------------------------------------
elif meniu_principal == "📈 Simulator Glicemie Postprandială & Slăbit":
    st.markdown('<p class="main-title">📈 Simulator Farmacocinetic & Predicție Metabolică</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Estimează curba glicemică postprandială pe 2 ore în funcție de masă, medicația luată (Siofor/Diaprel) și mișcare.</p>', unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        m_ales = st.selectbox("Selectează Masa Consumată:", [r["titlu"] for r in CLINICAL_RECIPES_DATABASE])
        glic_start = st.number_input("Glicemia la momentul 0 (înainte de masă) [mg/dL]:", value=112, min_value=70, max_value=250)
        miscare = st.selectbox("Activitate fizică postprandială:", [
            "Fără efort suplimentar", 
            "Plimbare lejeră 15 min (-15 mg/dL spike)", 
            "Mers rapid 30 min (-28 mg/dL spike)"
        ])
        ruleaza_sim = st.button("Generează Predicția AI")

    with col_s2:
        if ruleaza_sim:
            # Calcul estimativ avansat
            bonus_scadere = 15 if "15 min" in miscare else (28 if "30 min" in miscare else 0)
            pic_glicemic = glic_start + 16 - bonus_scadere
            if pic_glicemic < 100: pic_glicemic = 100
            
            st.success("Simularea metabolică a fost calculată cu succes!")
            st.metric("Vârf Glicemic Estimat (la 60 min)", f"{pic_glicemic} mg/dL", "Interval sigur (<140 mg/dL)")
            st.metric("Rată Estimată Slăbit (Lunar)", "-4.2 kg", "Menținere masă musculară")

            # Grafic Plotly interactiv
            timp_ax = ['0m (Înainte)', '30m', '60m (Vârf)', '90m', '120m (Stabilizare)']
            valori_glic = [glic_start, glic_start + 8, pic_glicemic, pic_glicemic - 5, glic_start - 2]
            
            fig_g = px.line(x=timp_ax, y=valori_glic, markers=True, title="Dinamica Glicemiei Postprandiale sub Tratament")
            fig_g.update_layout(yaxis_title="Glicemie (mg/dL)", xaxis_title="Timp postprandial", template="plotly_white")
            st.plotly_chart(fig_g, use_container_width=True)

# ---------------------------------------------------------
# MODULUL 4: GAMIFICATION & XP
# ---------------------------------------------------------
elif meniu_principal == "🏆 Gamification, XP & Realizări":
    st.markdown('<p class="main-title">🏆 Gamification & Performanță Clinică</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle>Transformă disciplina terapeutică într-o experiență interactivă cu puncte XP și badge-uri.</p>', unsafe_allow_html=True)

    col_g1, col_g2, col_g3 = st.columns(3)
    col_g1.markdown('<div class="metric-box"><h3>🔥 14 Zile</h3><p>Streak Terapeutic</p></div>', unsafe_allow_html=True)
    col_g2.markdown('<div class="metric-box"><h3>⭐ Nivel 5</h3><p>Maestru Anti-Spike</p></div>', unsafe_allow_html=True)
    col_g3.markdown('<div class="metric-box"><h3>750 / 1000 XP</h3><p>Progres spre Nivelul 6</p></div>', unsafe_allow_html=True)

    st.markdown("### 🏅 Badge-uri și Realizări Deblocate")
    st.markdown("""
    - 🔥 **Streak de 14 Zile:** Logare constantă a meselor și respectarea orarului medicamentelor.
    - 🛡️ **Zero Spike Master:** 10 mese consecutive fără salt glicemic peste pragul de siguranță.
    - 🥗 **Chef Anti-Zahăr:** 15 rețete testate cu Indice Glicemic sub 25.
    - ⚖️ **Primul Kilogram Topit:** Obiectivul de slăbit lunar atins anticipat.
    """)

# ---------------------------------------------------------
# MODULUL 5: JURNAL & EXPORT RAPORT PDF
# ---------------------------------------------------------
elif meniu_principal == "📄 Jurnal Medical & Export Raport PDF":
    st.markdown('<p class="main-title">📄 Jurnal Medical & Raport pentru Medicul Curant</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Centralizează datele pentru consultația următoare.</p>', unsafe_allow_html=True)

    jurnal_sample = pd.DataFrame([
        {"Data/Ora": "26.09.2026 13:30", "Masă Consumată": "Somon cu crustă de migdale", "Calorii": 420, "Carbi Net": "4.2g", "Glicemie Postprandială": "132 mg/dL", "Status": "Optim"},
        {"Data/Ora": "25.09.2026 19:45", "Masă Consumată": "Salată cu avocado și pui", "Calorii": 350, "Carbi Net": "5.5g", "Glicemie Postprandială": "126 mg/dL", "Status": "Optim"}
    ])
    
    st.dataframe(jurnal_sample, use_container_width=True)

    csv_data = jurnal_sample.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descarcă Raportul Medical (Format CSV / Excel)",
        data=csv_data,
        file_name=f"Raport_Medical_{PATIENT_PROFILE['nume'].replace(' ', '_')}.csv",
        mime='text/csv'
    )

# Panou Admin Exclusiv pentru Alex
if rol_utilizator == "Alex (Admin & Pacient)":
    st.sidebar.markdown("---")
    st.sidebar.success("👑 **Admin Privileges Active**\n\nAlex poate adăuga rețete noi, calibra parametrii glicemici și gestiona utilizatorii.")
