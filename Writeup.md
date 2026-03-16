#  Write-up : Tasty Secrets 

**Catégorie :** Steganography / Forensics  
**Difficulté :** Easy  

---

## Description du Challenge

Le Chef Anthinio Parmegano est devenu paranoïaque. Il a dissimulé sa recette secrète au cœur d'un fichier image de son plat phare le "Tasty Crousty", mais il a pris soin d'effacer toute trace visible.

Saurez-vous restaurer la structure du secret ?

**Fichier fourni :** `crousty_chall.jpg`

---

###  Hints

####  Niveau 1 : Le Double Tablier
La cible utilise une technique de **"Polyglotte"**. Un fichier JPEG peut légalement contenir d'autres données à l'intérieur d'un segment de commentaire (`FF FE`) sans altérer l'affichage de l'image. Vous devez explorer les premiers octets avec un éditeur hexadécimal pour repérer où les données cachées commencent.

####  Niveau 2 : L'Ingrédient Signature
Les outils automatiques comme `binwalk` ou `unzip` sont inefficaces ici car les signatures standards du format ZIP (`50 4B ...`) ont été remplacées par le marquage : **`CHEF`** (`43 48 45 46` en hexadécimal). Pour ouvrir l'archive, vous devez restaurer ces signatures manuellement ou via un script.

####  Niveau 3 : Le Fil d'Ariane (EOCD)
Une archive ZIP se décode plus facilement par la fin. Localisez le dernier tag **`CHEF`** du fichier ; il correspond à l'**EOCD** (End of Central Directory). En restaurant cette signature précise (`50 4B 05 06`), vous pourrez identifier les pointeurs nécessaires pour reconstruire toute la structure sabotée.

---

## Phase 1 : Analyse Initiale

Une analyse rapide avec les outils standards ne donne rien de concluant :

* **file** : Confirme qu'il s'agit d'un fichier JPEG valide.
* **binwalk / foremost** : Échec de la détection d'archives cachées car les signatures `PK` sont absentes.
* **strings** : On remarque une répétition inhabituelle du mot `CHEF`.

En ouvrant le fichier dans un **éditeur hexadécimal** (comme `HxD` ou `xxd`), on observe :

1. Le fichier commence bien par le header JPEG `FF D8`.
2. Un segment de commentaire `FF FE` commence dès l'offset **0x02**.
3. À partir de l'offset **0x06**, on trouve la chaîne `CHEF` ($43 48 45 46$ en hexadécimal) là où l'on attendrait normalement une signature de fichier.

---

## Phase 2 : Identification du Sabotage

Le challenge repose sur un **polyglotte JPEG/ZIP** dont les structures de contrôle de l'archive ZIP ont été intentionnellement corrompues. Le script de création a remplacé les signatures standard par la constante `CHEF` :

| Structure ZIP | Signature Originale | Signature Corrompue |
| :--- | :--- | :--- |
| **Local File Header** | `50 4B 03 04` | `CHEF` |
| **Central Directory** | `50 4B 01 02` | `CHEF` |
| **End of Central Directory** | `50 4B 05 06` | `CHEF` |

L'archive est techniquement présente dans le segment de commentaire JPEG, mais elle est invisible pour les logiciels de décompression.

---

## Phase 3 : Résolution

Pour résoudre ce challenge, il faut reconstruire manuellement (ou par script) la table des signatures en respectant la spécification du format ZIP (APPNOTE.TXT). L'astuce consiste à utiliser l'**EOCD** (End of Central Directory) situé à la fin de l'archive pour retrouver les pointeurs vers le **Central Directory**.

### Script de Restauration (Python)


```python

import struct

def restore_zip(input_file, output_file):

    with open(input_file, "rb") as f:

        data = bytearray(f.read())

    # On identifie tous les tags 'CHEF'

    tag = b"CHEF"

    offsets = [i for i in range(len(data)) if data.startswith(tag, i)]

    # 1. Restaurer l'EOCD (le dernier tag)

    eocd_off = offsets[-1]

    data[eocd_off:eocd_off+4] = b"\x50\x4b\x05\x06"

    # 2. Lire l'offset du Central Directory dans l'EOCD (offset +16)

    cd_offset_rel = struct.unpack("<I", data[eocd_off+16:eocd_off+20])[0]

    zip_start = offsets[0]

    cd_abs_off = zip_start + cd_offset_rel

    # 3. Restaurer les headers du Central Directory et les Local Headers associés

    # (Voir script solver.py pour la logique complète de parcours)
```
