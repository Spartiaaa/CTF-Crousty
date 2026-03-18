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
import os
import struct

def solve_blackout(input_path, restored_zip_path):
    print(f"[*] Début de la restauration chirurgicale : {input_path}")

    with open(input_path, "rb") as f:
        data = bytearray(f.read())

    # 1. Localiser tous les tags 'CHEF' (Signatures sabotées)
    tag = b"CHEF"
    offsets = []
    idx = data.find(tag)
    while idx != -1:
        offsets.append(idx)
        idx = data.find(tag, idx + 1)

    if not offsets:
        print("[!] Erreur : Aucune signature 'CHEF' détectée.")
        return

    print(f"[+] {len(offsets)} signatures corrompues identifiées.")

    # 2. Identifier le début du ZIP et l'EOCD
    # Le premier 'CHEF' est le début du Local File Header de l'archive
    zip_start_offset = offsets[0]
    # Le dernier 'CHEF' est obligatoirement l'EOCD (End of Central Directory)
    eocd_offset = offsets[-1]

    print(f"[*] Restauration de l'EOCD à l'offset : {hex(eocd_offset)}")
    data[eocd_offset : eocd_offset + 4] = b"\x50\x4b\x05\x06"

    # 3. Analyser l'EOCD pour trouver le Central Directory (CD)
    # L'offset du CD est stocké à +16 octets du début de l'EOCD (4 octets, Little Endian)
    # Cet offset est relatif au début du fichier ZIP.
    cd_offset_relative = struct.unpack("<I", data[eocd_offset + 16 : eocd_offset + 20])[
        0
    ]
    cd_start_abs = zip_start_offset + cd_offset_relative

    # On lit aussi le nombre d'entrées (fichiers) dans le ZIP (+10 octets, 2 octets)
    num_entries = struct.unpack("<H", data[eocd_offset + 10 : eocd_offset + 12])[0]
    print(
        f"[*] {num_entries} fichier(s) détecté(s). Central Directory à : {hex(cd_start_abs)}"
    )

    # 4. Parcourir le Central Directory pour restaurer les headers et trouver les Local Headers
    current_cd_pos = cd_start_abs
    for i in range(num_entries):
        # Restauration du Header du Central Directory
        if data[current_cd_pos : current_cd_pos + 4] == b"CHEF":
            data[current_cd_pos : current_cd_pos + 4] = b"\x50\x4b\x01\x02"

            # Récupérer l'offset du Local Header associé à ce fichier (+42 octets du début de l'entrée CD)
            local_header_rel = struct.unpack(
                "<I", data[current_cd_pos + 42 : current_cd_pos + 46]
            )[0]
            local_header_abs = zip_start_offset + local_header_rel

            # Restauration du Local Header
            if data[local_header_abs : local_header_abs + 4] == b"CHEF":
                print(
                    f"    [+] Restauration Local Header #{i} à {hex(local_header_abs)}"
                )
                data[local_header_abs : local_header_abs + 4] = b"\x50\x4b\x03\x04"

            # Avancer vers l'entrée suivante du CD (Taille fixe 46 + longueurs variables n, m, k)
            n = struct.unpack("<H", data[current_cd_pos + 28 : current_cd_pos + 30])[
                0
            ]  # file name length
            m = struct.unpack("<H", data[current_cd_pos + 30 : current_cd_pos + 32])[
                0
            ]  # extra field length
            k = struct.unpack("<H", data[current_cd_pos + 32 : current_cd_pos + 34])[
                0
            ]  # file comment length
            current_cd_pos += 46 + n + m + k

    # 5. Extraction finale du ZIP nettoyé
    # On calcule la fin du ZIP (EOCD (22) + taille du commentaire éventuel)
    zip_comment_len = struct.unpack("<H", data[eocd_offset + 20 : eocd_offset + 22])[0]
    zip_end_abs = eocd_offset + 22 + zip_comment_len

    zip_final = data[zip_start_offset:zip_end_abs]

    with open(restored_zip_path, "wb") as f:
        f.write(zip_final)

    print(f"\n[!] Restauration terminée : {restored_zip_path}")
    print("[*] Le fichier est maintenant prêt à être décompressé.")


if __name__ == "__main__":
    solve_blackout("crousty_chall.jpg", "tasty_recovered.zip")
```
### **Flag : CTF{P4rm3g4n0_S3cr3t_R3c1p3_2026}**
