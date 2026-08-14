---
library_name: sentence-transformers
pipeline_tag: sentence-similarity
license: other
---

# Xbox Search Recommender

Bundle expérimental de recherche et recommandation pour les requêtes Xbox du challenge Kaggle
`acm-sf-chapter-hackathon-small`.

## Statut de publication

La publication des artefacts est actuellement **désactivée**. Le dépôt GitHub contient le code et les
notebooks, mais pas les données Kaggle ni les fichiers dérivés du catalogue.

## Architecture

- historique normalisé requête → SKU ;
- TF-IDF mots et caractères ;
- embeddings `sentence-transformers/all-MiniLM-L6-v2` ;
- index FAISS ;
- popularité ;
- fusion pondérée.

Le modèle Sentence Transformers d'origine n'est pas republié. Il est téléchargé depuis son dépôt
officiel lors de la préparation locale.

## Limites

Les métriques produites avec le corpus synthétique sont uniquement des smoke tests. Elles ne doivent
pas être interprétées comme des performances Kaggle. Toute publication future exige la vérification
des règles du challenge et des droits sur les artefacts dérivés.

