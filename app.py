from flask import Flask, render_template, request, Response
import pandas as pd
import numpy as np
import io

app = Flask(__name__)

# --- DONNÉES DE DÉMONSTRATION (12 Fiches) ---
data_demo = [
    {"espece": "Bovin", "poids": 450, "production": 22, "sante": "Bon", "cout": 120, "effectif": 1},
    {"espece": "Caprin", "poids": 45, "production": 3, "sante": "Excellent", "cout": 15, "effectif": 5},
    {"espece": "Volailles", "poids": 2.1, "production": 0, "sante": "Moyen", "cout": 2, "effectif": 100},
    {"espece": "Bovin", "poids": 480, "production": 25, "sante": "Excellent", "cout": 130, "effectif": 1},
    {"espece": "Porcin", "poids": 90, "production": 0, "sante": "Bon", "cout": 45, "effectif": 10},
    {"espece": "Bovin", "poids": 420, "production": 18, "sante": "Critique", "cout": 140, "effectif": 1},
    {"espece": "Volailles", "poids": 1.9, "production": 0, "sante": "Bon", "cout": 1.8, "effectif": 150},
    {"espece": "Caprin", "poids": 50, "production": 4, "sante": "Bon", "cout": 18, "effectif": 4},
    {"espece": "Porcin", "poids": 95, "production": 0, "sante": "Excellent", "cout": 40, "effectif": 12},
    {"espece": "Bovin", "poids": 460, "production": 20, "sante": "Bon", "cout": 115, "effectif": 1},
    {"espece": "Volailles", "poids": 2.3, "production": 0, "sante": "Moyen", "cout": 2.2, "effectif": 80},
    {"espece": "Caprin", "poids": 42, "production": 2.5, "sante": "Moyen", "cout": 14, "effectif": 6},
]
df = pd.DataFrame(data_demo)

@app.route('/')
def dashboard():
    # --- 6 KPI ---
    kpi = {
        "total_animaux": int(df['effectif'].sum()),
        "poids_moyen": round(df['poids'].mean(), 2),
        "prod_totale": round(df['production'].sum(), 2),
        "cout_moyen": round(df['cout'].mean(), 2),
        "taux_excellent": round((df[df['sante'] == 'Excellent'].shape[0] / len(df)) * 100, 1),
        "espece_majoritaire": df['espece'].mode()[0]
    }

    # --- ANALYSE DESCRIPTIVE ---
    stats = df[['poids', 'production', 'cout']].describe().to_dict()
    # Ajout Médiane et Étendue manuellement
    for col in ['poids', 'production', 'cout']:
        stats[col]['median'] = df[col].median()
        stats[col]['range'] = df[col].max() - df[col].min()

    # --- TABLEAU CROISÉ (Espèce x Santé) ---
    cross_tab = pd.crosstab(df['espece'], df['sante']).to_dict()

    return render_template('dashboard.html', kpi=kpi, stats=stats, cross_tab=cross_tab)

@app.route('/export')
def export():
    proxy = io.StringIO()
    df.to_csv(proxy, index=False, sep=';')
    return Response(proxy.getvalue(), mimetype="text/csv", 
                    headers={"Content-disposition": "attachment; filename=rapport_elevage.csv"})

if __name__ == '__main__':
    app.run(debug=True)
