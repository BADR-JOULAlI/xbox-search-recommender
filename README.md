# Xbox Search Recommender

Système local de recherche et de recommandation de jeux Xbox construit pour le challenge Kaggle
**ACM SF Chapter Hackathon (small)**. Une requête produit cinq SKU distincts, classés par pertinence.

Le dépôt est **notebook-first** : 13 notebooks couvrent l'environnement, les données, les baselines,
TF-IDF, les embeddings, FAISS, le ranking hybride, l'évaluation, Gradio, Kaggle et Hugging Face.

## État actuel

- RTX 5070 Laptop détectée : 7,96 Go de VRAM.
- PyTorch 2.11.0 avec CUDA 12.8 validé par un calcul réel.
- 13 notebooks créés sans outputs volumineux dans Git.
- 11 tests unitaires passent localement.
- Interface Gradio validée avec cinq SKU uniques.
- Dépôt GitHub alimenté par commits progressifs.
- Publication Hugging Face désactivée en attendant la source réelle et la validation des droits.

Le téléchargement Kaggle renvoie actuellement `403 Forbidden` tant que les règles du challenge ne
sont pas acceptées avec le compte authentifié. Le pipeline utilise temporairement un corpus
synthétique afin de rester entièrement testable. Les métriques correspondantes sont provisoires.

## Architecture

```text
requête
  ├─ historique requête → clics
  ├─ TF-IDF mots
  ├─ TF-IDF caractères
  ├─ embeddings Sentence Transformers → FAISS
  └─ popularité
             ↓
       fusion pondérée
             ↓
       cinq SKU distincts
```

Le modèle sémantique par défaut est `sentence-transformers/all-MiniLM-L6-v2`. Son encodage utilise
CUDA ; l'index FAISS reste sur CPU pour conserver une installation Windows simple.

## Installation sous Windows

Installer [uv](https://docs.astral.sh/uv/), puis exécuter dans PowerShell :

```powershell
uv python install 3.11
uv venv --python 3.11 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-cuda.txt
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Le fichier CUDA utilise les wheels PyTorch CUDA 12.8 nécessaires à l'architecture Blackwell des RTX
50. Pour une machine CPU, omettre `requirements-cuda.txt` et installer PyTorch CPU séparément.

## Télécharger les données Kaggle

1. Ouvrir la [page du challenge](https://www.kaggle.com/c/acm-sf-chapter-hackathon-small/data).
2. Cliquer sur **Join Competition** et accepter les règles.
3. Authentifier le CLI :

```powershell
.\.venv\Scripts\kaggle.exe auth login
```

4. Télécharger les fichiers :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\download_data.ps1
```

Les données restent dans `data/raw` et ne sont jamais suivies par Git.

## Notebooks

| Notebook | Rôle |
|---|---|
| `00_environment_and_gpu.ipynb` | Python, pilote, CUDA et smoke test GPU |
| `01_download_and_inspect_data.ipynb` | inventaire Kaggle et fallback synthétique |
| `02_data_cleaning_and_eda.ipynb` | nettoyage, XML, statistiques et figures |
| `03_popularity_baseline.ipynb` | split sans fuite et popularité globale |
| `04_query_click_baseline.ipynb` | historique requête normalisée → SKU |
| `05_tfidf_search.ipynb` | recherche lexicale mots et caractères |
| `06_semantic_search_faiss.ipynb` | embeddings CUDA et index FAISS |
| `07_hybrid_ranking.ipynb` | fusion des cinq signaux |
| `08_evaluation_and_comparison.ipynb` | comparaison MAP@5, recall, MRR et hit rate |
| `09_build_production_artifacts.ipynb` | bundle local et manifeste SHA-256 |
| `10_gradio_demo.ipynb` | validation de l'interface locale |
| `11_generate_kaggle_submission.ipynb` | fichier `sku` au format Kaggle |
| `12_huggingface_publication.ipynb` | audit de licence et décision de publication |

Exécuter toute la chaîne :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_all_notebooks.ps1
```

Le bypass s'applique uniquement à ce nouveau processus PowerShell et ne modifie pas durablement la
stratégie de sécurité de Windows.

Les copies exécutées sont écrites dans `reports/executed-notebooks` et ignorées par Git.

## Résultats de smoke test

Ces scores utilisent exclusivement le corpus synthétique et ne représentent pas le leaderboard :

| Modèle | MAP@5 | Recall@5 | MRR@5 |
|---|---:|---:|---:|
| Popularité | 0,04 | 0,20 | 0,04 |
| Historique + fallback | 0,04 | 0,20 | 0,04 |
| TF-IDF mots + caractères | 1,00 | 1,00 | 1,00 |
| Sentence Transformers | 1,00 | 1,00 | 1,00 |
| Hybride pondéré | 0,90 | 1,00 | 0,90 |

Après disponibilité des données Kaggle, réexécuter les notebooks 01 à 12. Les rapports indiqueront
alors `source: kaggle` au lieu de `source: synthetic-demo`.

## Application Gradio

Après les notebooks 01 à 09 :

```powershell
.\.venv\Scripts\python.exe -m src.app
```

Ouvrir <http://127.0.0.1:7860>. L'application utilise `share=False` et ne crée pas de tunnel public.

## Soumission Kaggle

Le notebook 11 crée `submissions/predictions.csv` avec une unique colonne `sku`. Chaque cellule
contient cinq SKU distincts séparés par des espaces. Le fichier est ignoré par Git.

## GitHub et Hugging Face

GitHub contient le code, les notebooks sans outputs, les configurations, les tests et les rapports
non sensibles. Il exclut les données, tokens, caches, embeddings, index et modèles.

Hugging Face n'est actuellement pas nécessaire. Le notebook 12 retourne :

> Aucun artefact ne nécessite actuellement une publication sur Hugging Face.

Une publication future restera privée par défaut et exigera simultanément `--confirm-license` et
`--push`. Le dataset Kaggle et le modèle tiers original ne seront jamais republiés.

## Qualité

```powershell
.\.venv\Scripts\ruff.exe check src tests
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\nbstripout.exe --dry-run notebooks\*.ipynb
```

GitHub Actions valide les tests, le format JSON des 13 notebooks et un notebook de smoke test sans
avoir besoin du dataset privé ni d'un GPU.

## Licence

Le code du dépôt est sous licence MIT. Cette licence ne s'applique pas automatiquement aux données
Kaggle, aux descriptions Best Buy ou aux artefacts dérivés : leurs conditions doivent être vérifiées
séparément avant redistribution.
