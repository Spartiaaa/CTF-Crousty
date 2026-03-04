# 🚩 Mission : Tasty Secrets - Blackout

Vous êtes un agent ayant réussi à intercepter une image provenant du serveur privé d'un célèbre chef cuisinier soupçonné d'espionnage industriel sur la recette originale du Tasty Crousty.

---

### 🔍 Hints (Indices)

#### 🟢 Niveau 1 : Le Double Tablier
La cible utilise une technique de **"Polyglotte"**. Un fichier JPEG peut légalement contenir d'autres données à l'intérieur d'un segment de commentaire (`FF FE`) sans altérer l'affichage de l'image. Vous devez explorer les premiers octets avec un éditeur hexadécimal pour repérer où les données cachées commencent.

#### 🟡 Niveau 2 : L'Ingrédient Signature
Les outils automatiques comme `binwalk` ou `unzip` sont inefficaces ici car les signatures standards du format ZIP (`50 4B ...`) ont été remplacées par le marquage : **`CHEF`** (`43 48 45 46` en hexadécimal). Pour ouvrir l'archive, vous devez restaurer ces signatures manuellement ou via un script.

#### 🔴 Niveau 3 : Le Fil d'Ariane (EOCD)
Une archive ZIP se décode plus facilement par la fin. Localisez le dernier tag **`CHEF`** du fichier ; il correspond à l'**EOCD** (End of Central Directory). En restaurant cette signature précise (`50 4B 05 06`), vous pourrez identifier les pointeurs nécessaires pour reconstruire toute la structure sabotée.

---
*Bonne chance, Agent. La survie du Tasty Crousty est entre vos mains.*
