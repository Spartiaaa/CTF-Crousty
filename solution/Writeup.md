# Write-up : Tasty Secrets

**Catégorie :** Stéganographie / Forensics  
**Difficulté :** Facile / Moyen  

---

## 📝 Description du Challenge
Le Chef Anthinio Parmegano est devenu paranoïaque. Il a dissimulé sa recette secrète au cœur d'un fichier image de son plat phare, le "Tasty Crousty", mais il a pris soin d'effacer toute trace visible.  
Saurez-vous restaurer la structure du secret ?

**Fichier fourni :** `crousty_chall.jpg`

---

## 🔍 Phase 1 : Analyse Initiale
Une inspection rapide du fichier confirme qu'il s'agit d'une image JPEG valide. Cependant, les outils de forensic standards échouent à extraire des données cachées :
* `binwalk` / `foremost` : Aucune archive détectée.
* `strings` : On remarque plusieurs occurrences suspectes de la chaîne `CHEF` dans le binaire.

En ouvrant le fichier dans un **éditeur hexadécimal** (comme HxD ou `xxd`), on observe une structure personnalisée :
1. Le fichier débute par le header JPEG `FF D8`.
2. Un segment de commentaire `FF FE` commence à l'offset `0x02`.
3. À partir de l'offset `0x06`, la signature `CHEF` (`43 48 45 46` en hexadécimal) remplace ce qui ressemble normalement à une structure d'archive.

---

## 💡 Phase 2 : Identification du Sabotage
Le challenge repose sur un **polyglotte JPEG/ZIP**. L'archive ZIP est présente dans le segment de commentaire du JPEG, mais ses signatures ont été intentionnellement corrompues par la constante `CHEF` :

| Structure | Signature Originale | Signature Corrompue |
| :--- | :--- | :--- |
| **Local File Header** | `50 4B 03 04` | `CHEF` |
| **Central Directory** | `50 4B 01 02` | `CHEF` |
| **End of Central Directory** | `50 4B 05 06` | `CHEF` |

---

## 🛠️ Phase 3 : Résolution
La résolution nécessite de restaurer les signatures ZIP. La méthode la plus fiable consiste à localiser l'**EOCD (End of Central Directory)** à la fin du fichier pour valider la structure.

### Script de Restauration (Python)

```python
import struct

def restore_zip(input_file, output_file):
    with open(input_file, "rb") as f:
        data = bytearray(f.read())

    tag = b"CHEF"
    offsets = [i for i in range(len(data)) if data.startswith(tag, i)]

    if not offsets:
        print("[-] Aucune signature 'CHEF' trouvée.")
        return

    # 1. Restaurer l'EOCD (le dernier tag)
    eocd_off = offsets[-1]
    data[eocd_off:eocd_off+4] = b"\x50\x4b\x05\x06"

    # 2. Restaurer les headers précédents (Local Headers)
    for off in offsets[:-1]:
        data[off:off+4] = b"\x50\x4b\x03\x04" 

    with open(output_file, "wb") as f:
        f.write(data)
    print(f"[+] Archive restaurée : {output_file}")

restore_zip("crousty_chall.jpg", "recipe_restored.zip")
```
**Flag : CTF{P4rm3g4n0_S3cr3t_R3c1p3_2026}**
