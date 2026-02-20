**Catégorie :** Forensic / Stéganographie **Difficulté :** 🔴 Hard

---

## 1. Analyse Initiale

On commence par inspecter le fichier fourni, `challenge_hard.jpg`, avec les outils de base pour identifier sa nature. 

L'outil `file` nous confirme qu'il s'agit d'un JPEG valide. Cependant, un examen visuel de l'image ne révèle aucun artefact, message caché ou LSB (Least Significant Bit) évident.

## 2. Analyse des Métadonnées

	Utilisons `exiftool` pour voir si des informations ont été laissées dans les headers.

**Observation cruciale :** Le champ `Comment` contient des données binaires. On y distingue les caractères **`PK`**, suivis de ce qui ressemble à un nom de fichier : `flag.txt`. Le marqueur `PK` (en hexadécimal `50 4B 03 04`) est la signature (Magic Bytes) d'une archive **ZIP**.

## 3. Analyse Hexadécimale (Deep Dive)

Ouvrons le fichier avec un éditeur hexadécimal (comme `HxD` ou `hexyl`) pour comprendre comment ce ZIP est imbriqué.

**Décomposition des premiers octets :**

1. `FF D8` : Marqueur JPEG **SOI** (Start of Image).
    
2. `FF FE` : Marqueur JPEG **COM** (Commentaire).
    
3. `02 4B` : Taille du segment de commentaire (en Big Endian). `0x024B` = 587 octets.
    
4. **`50 4B 03 04`** : Début de l'archive ZIP à l'offset **`0x06`**.
    

Le fichier est un **polyglotte**. La structure JPEG englobe l'archive ZIP dans un segment de commentaire que les visionneuses d'images ignorent, tandis que les extracteurs ZIP cherchent la signature `PK` n'importe où dans les premiers octets du fichier.

## 4. Extraction du Secret

Puisque le fichier est une archive ZIP valide avec un "prefix junk" de seulement 6 octets, la plupart des outils de décompression modernes peuvent le traiter directement.

### Méthode A : Extraction directe

On change l'extension ou on force l'extraction :

### Méthode B : Carving manuel (Binwalk)

Si l'extraction directe échoue, on peut utiliser `binwalk` pour extraire les fichiers imbriqués :

## 5. Récupération du Flag

Une fois le fichier `flag.txt` extrait, il ne reste plus qu'à lire son contenu.

---

## 🏁 Conclusion

Ce challenge reposait sur la manipulation des headers JPEG. En utilisant le segment `FF FE` (Comment), l'attaquant a pu insérer une structure de données complète (ZIP) sans corrompre le rendu visuel de l'image. C'est une technique puissante de stéganographie qui trompe les outils d'analyse de fichiers trop simplistes.