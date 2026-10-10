import os
import glob
import shutil

BASE = "/content/donnees"

# classe : [(code locuteur CMU Arctic, nb fichiers train, nb fichiers test)]
VOIX = {
    "Moi":    [("jmk", 100, 20)],
    "User1":  [("bdl", 100, 20)],
    "User2":  [("slt", 100, 20)],
    "Autres": [("clb", 40, 10), ("awb", 40, 10), ("rms", 40, 10)],
}

for classe, locuteurs in VOIX.items():
    for dossier in ["entrainements", "tests"]:
        os.makedirs(f"{BASE}/{dossier}/{classe}", exist_ok=True)
    for code, n_train, n_test in locuteurs:
        url = f"http://festvox.org/cmu_arctic/packed/cmu_us_{code}_arctic.tar.bz2"
        os.system(f"wget -q {url} -O /content/{code}.tar.bz2 && tar -xjf /content/{code}.tar.bz2 -C /content")
        fichiers = sorted(glob.glob(f"/content/cmu_us_{code}_arctic/wav/*.wav"))
        for f in fichiers[:n_train]:
            shutil.copy(f, f"{BASE}/entrainements/{classe}/{code}_{os.path.basename(f)}")
        for f in fichiers[-n_test:]:
            shutil.copy(f, f"{BASE}/tests/{classe}/{code}_{os.path.basename(f)}")
        print(classe, "<-", code, ":", len(fichiers), "fichiers trouvés")
