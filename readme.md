# Automatizované testy e-shopu Amon Amarth

Tento repozitář obsahuje **automatizované testy webu e-shopu kapely Amon Amarth** pomocí **Python + Playwright**. Testy jsou určeny pro kurz testování.

---

## Struktura testů

### 1. `test_zobrazeni_homepage_loga`
- **Účel:** Ověřit, zda se na hlavní stránce zobrazuje logo kapely.  
- **Co testuje:** Viditelnost obrázku loga.

### 2. `test_pridani_2ks_zbozi_do_kosiku`
- **Účel:** Přidat konkrétní produkt do košíku a ověřit jeho množství.  
- **Kroky:**
  1. Přechod z homepage do obchodu (SHOP → INTERNATIONAL).
  2. Otevření konkrétního produktu „Zipper - We Rule The Waves“.
  3. Výběr velikosti L.
  4. Zvýšení množství na 2 ks.
  5. Přidání do košíku.
  6. Kontrola, že se zobrazil popup „Products in your cart“.
  7. Ověření množství v košíku na stránce košíku.

### 3. `test_prihlaseni_neregistrovaneho_uzivatele`
- **Účel:** Ověřit chování při přihlášení neregistrovaného uživatele bez zboží v košíku.  
- **Kroky:**
  1. Přechod do obchodu a na stránku Login.
  2. Vyplnění neplatného emailu a hesla.
  3. Reálný klik myší na tlačítko „Login“ (kvůli JavaScriptu, popup se objevuje pouze při skutečném kliknutí).
  4. Ověření, že se zobrazil popup hlášky **„Please add an item first“**.

**Poznámka:** Popup se zobrazuje jen na pár sekund, proto je nutné ověřit ho ihned po kliknutí.

---

## Požadavky
- Python 3.13+
- Playwright (`pip install playwright`)
- Pytest (`pip install pytest`)

Po instalaci Playwrightu spusť:
```bash
playwright install


## Spuštění testů

```bash
# Spuštění všech testů
pytest

# Spuštění konkrétního testu (např. test přihlášení neregistrovaného uživatele)
pytest python.py::test_prihlaseni_neregistrovaneho_uzivatele

# Spuštění testů s podrobným výstupem
pytest -v
