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

Le dépôt vient d'être initialisé. Les notebooks seront ajoutés et poussés progressivement après exécution et validation.

## Sécurité des données

Le dataset Kaggle, les tokens, les caches, les embeddings et les artefacts volumineux ne sont pas suivis par Git.

