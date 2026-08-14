# Xbox Search Recommender

Système local de recherche et de recommandation de jeux Xbox à partir du challenge Kaggle **ACM SF Chapter Hackathon (small)**.

Le projet est conçu en mode **notebook-first** : l'exploration, l'entraînement, l'évaluation et la génération de la soumission sont réalisés principalement dans des notebooks Jupyter. Une petite couche Python assure l'inférence réutilisable, les tests et l'interface Gradio.

## Objectifs

- Retourner cinq SKU distincts pour chaque requête.
- Comparer popularité, historique des clics, TF-IDF et recherche sémantique.
- Construire un ranking hybride évalué avec MAP@5.
- Exploiter localement CUDA sur une RTX 5070 avec fallback CPU.
- Générer une interface Gradio et une soumission Kaggle.
- Versionner le code sur GitHub dès le démarrage.
- Publier sur Hugging Face uniquement les artefacts utiles et redistribuables.

## Statut

Le dépôt est développé par jalons. Chaque notebook est exécuté et validé avant son push.

## Installation rapide sous PowerShell

```powershell
uv python install 3.11
uv venv --python 3.11 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-cuda.txt
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

PyTorch 2.11 avec CUDA 12.8 est utilisé afin de prendre en charge l'architecture Blackwell des RTX 50. Le projet détecte CUDA au runtime et conserve un fallback CPU.

Pour accéder aux données Kaggle :

```powershell
.\.venv\Scripts\kaggle.exe auth login
.\.venv\Scripts\kaggle.exe competitions download -c acm-sf-chapter-hackathon-small -p data/raw
```

L'authentification Kaggle reste locale et ne doit jamais être ajoutée au dépôt.

## Sécurité des données

Le dataset Kaggle, les tokens, les caches, les embeddings et les artefacts volumineux ne sont pas suivis par Git.
