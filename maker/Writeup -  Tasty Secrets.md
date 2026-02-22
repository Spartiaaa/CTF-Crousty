# 🚩 Write-Up : Le Secret Corrompu du Chef Enzo

**Catégorie :** Forensic / Stéganographie  
**Difficulté :** 🔴 Insane (Expert)

---

## 1. Analyse Initiale
L'analyse avec l'outil `file` confirme que `challenge_insane.jpg` est un fichier JPEG valide. Toutefois, les outils d'extraction automatisés échouent :
* **Binwalk** : Détecte une signature ZIP à l'offset `0x06` mais l'extraction ne produit aucun fichier.
* **7z / Unzip** : Déclarent que le fichier n'est pas une archive ou que les en-têtes sont corrompus.

---

## 2. Structure du Fichier
L'examen hexadécimal révèle un montage **polyglotte**. Une archive ZIP est encapsulée dans un segment de commentaire JPEG (**COM**).

| Offset | Valeur Hex | Description | Endianness |
| :--- | :--- | :--- | :--- |
| `0x00` | `FF D8` | SOI (Start of Image) | N/A |
| `0x02` | `FF FE` | COM (JPEG Comment Marker) | N/A |
| `0x04` | `XX XX` | Taille du segment (Données ZIP incluses) | **Big Endian** |
| `0x06` | `50 4B 03 04` | Signature Local File Header ZIP | **Little Endian** |

---

## 3. Identification de la Corruption
Le sabotage se situe dans le **Central Directory (CD)**, la structure de contrôle située à la fin des données ZIP :

1. **Signature du CD invalide** : La signature standard `50 4B 01 02` a été modifiée en **`50 4B 00 00`**. Cela empêche les extracteurs de lister les fichiers contenus.
2. **Version d'extraction erronée** : Le champ *Version needed to extract* (offset +6 du CD) contient la valeur **`FF FF`** (65535), ce qui est invalide pour le format ZIP.

---

## 4. Résolution (Réparation Binaire)
La restauration doit respecter la spécification **PKWARE**. Deux méthodes sont possibles :

### Méthode A : Manuelle (Éditeur Hex)
1. **Signature** : Localiser la séquence `50 4B 00 00` et la corriger en **`50 4B 01 02`**.
2. **Version** : Modifier les octets `FF FF` (offset +6) par **`14 00`** (Version 2.0).

### Méthode B : Automatisée (Script Python)
Pour une résolution rapide sur plusieurs fichiers, on peut utiliser le script suivant :

```python
import struct

def solver(input_file, output_file):
    with open(input_file, "rb") as f:
        data = bytearray(f.read())

    # Recherche et correction du Central Directory
    cd_sig = b"\x50\x4b\x00\x00"
    offset = data.find(cd_sig)

    if offset != -1:
        # Correction Signature + Version (2.0)
        data[offset:offset+4] = b"\x50\x4b\x01\x02"
        data[offset+6:offset+8] = struct.pack("<H", 20)
        
        with open(output_file, "wb") as f:
            f.write(data)
        print("[+] Fichier réparé généré.")
