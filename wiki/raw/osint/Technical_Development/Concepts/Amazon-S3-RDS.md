---
tags: [technical-development, aws, s3, rds, database, storage]
---
### Amazon S3 (pour les images) + RDS
Si vous avez besoin d'un stockage scalable pour les images et une base de données relationnelle pour les métadonnées :

**Pourquoi choisir cette combinaison**:
- **S3** : Excellente solution pour le stockage de fichiers volumineux.
- **RDS** : Offre une base de données relationnelle gérée (comme PostgreSQL ou MySQL).

**Comment l'utiliser**:
- **Boto3 pour S3** : Utilisez la bibliothèque Boto3 pour interagir avec S3 en Python.
- **Exemple d'upload à S3** :
    ```python
    import boto3
    
    s3 = boto3.client('s3')
    bucket_name = 'your-bucket-name'
    
    s3.upload_file('path/to/local/img1.jpg', bucket_name, 'img1.jpg')
    s3.upload_file('path/to/local/img2.jpg', bucket_name, 'img2.jpg')
    ```

- **Psycopg2 pour RDS** : Connectez-vous à votre instance RDS PostgreSQL de la même manière que pour PostgreSQL local.