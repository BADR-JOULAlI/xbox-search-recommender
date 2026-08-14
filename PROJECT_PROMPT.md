# Prompt d'exécution du projet

Construis réellement un système local de recherche et recommandation de jeux Xbox à partir du dataset Kaggle `acm-sf-chapter-hackathon-small`.

Travaille en boucle jusqu'à obtenir un projet reproductible :

1. implémenter une étape ;
2. exécuter le notebook correspondant ;
3. mesurer et vérifier le résultat ;
4. corriger les erreurs ;
5. exécuter les tests ;
6. committer et pousser l'étape sur GitHub ;
7. passer à l'étape suivante.

Contraintes principales :

- Windows, Python 3.11 et exécution locale ;
- NVIDIA RTX 5070, CUDA et FP16 lorsque possible, fallback CPU ;
- aucun service ML payant et aucun LLM distant ;
- 75 à 85 % du code métier dans des notebooks Jupyter ;
- cinq SKU distincts classés pour chaque requête ;
- évaluation MAP@5, Recall@5, MRR@5 et Hit Rate@5 ;
- baselines popularité et historique requête/SKU ;
- recherche lexicale TF-IDF mots et caractères ;
- recherche sémantique avec Sentence Transformers et FAISS ;
- fusion hybride, puis LGBMRanker seulement si les données le justifient ;
- interface Gradio locale sur `127.0.0.1` ;
- génération d'une soumission Kaggle valide ;
- tests unitaires et smoke tests sans dataset privé dans GitHub Actions.

Notebooks attendus :

- `00_environment_and_gpu.ipynb`
- `01_download_and_inspect_data.ipynb`
- `02_data_cleaning_and_eda.ipynb`
- `03_popularity_baseline.ipynb`
- `04_query_click_baseline.ipynb`
- `05_tfidf_search.ipynb`
- `06_semantic_search_faiss.ipynb`
- `07_hybrid_ranking.ipynb`
- `08_evaluation_and_comparison.ipynb`
- `09_build_production_artifacts.ipynb`
- `10_gradio_demo.ipynb`
- `11_generate_kaggle_submission.ipynb`
- `12_huggingface_publication.ipynb`

GitHub doit recevoir un premier push avant le développement, puis un push après chaque phase validée. Ne jamais pousser le dataset Kaggle, des secrets, les caches, les modèles tiers téléchargés ou les gros artefacts.

Hugging Face ne doit pas être créé au début. Après entraînement, vérifier les licences et expliquer si un dépôt privé d'artefacts est utile. Ne jamais republier le dataset Kaggle ni le modèle tiers d'origine.

