import pytest
from playwright.sync_api import Page, sync_playwright, expect

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.amonamarth.com/")
        yield page
        context.close()
        browser.close()

def test_zobrazeni_homepage_loga(page: Page):
    """Otestuje zda se zobrazuje logo kapely na hlavní stránce"""
    homepage_logo = page.locator("img[src*='Logo2018+white.png']")
    assert homepage_logo.is_visible(), f"Logo kapely na úvodní stránce není viditelné. Aktuální URL: {page.url}"

def test_pridani_2ks_zbozi_do_kosiku(page: Page):
    """Přechod z homepage do obchodu, vložení 2ks zboží do košíku a kontrola košíku, zda obsahuje 2ks zboží"""

    # Přechod do obchodu z menu
    odkaz_shop = page.get_by_role("link", name="SHOP")
    odkaz_shop.hover()
    odkaz_international = page.get_by_role("link", name="INTERNATIONAL")
    odkaz_international.click()

    # kontrola otevření stránky shop pomocí URL
    assert "https://eu.amonamarth.shop/en/" in page.url, f"Není otevřená správná URL obchodu. Aktuální URL: {page.url}"

    # otevření konkrétního produktu
    zbozi_k_nakupu = page.get_by_role("link", name="zipper--we-rule-the-waves")
    zbozi_k_nakupu.scroll_into_view_if_needed()
    zbozi_k_nakupu.click()

    # Kontrola názvu produktu
    nazev_zbozi = page.get_by_role("heading", name="Zipper - We Rule The Waves")
    try:
        expect(nazev_zbozi).to_be_visible(timeout=3000)
    except Exception:
        raise AssertionError("Nadpis produktu 'Zipper - We Rule The Waves' není vidět.")

    # krátký wait před klikem na velikost XL
    page.wait_for_timeout(500)
    velikost_L = page.get_by_text("XL", exact=True)
    velikost_L.scroll_into_view_if_needed()
    velikost_L.click(force=True)
    page.wait_for_timeout(500)  # čekáme na update třídy
    assert "active" in velikost_L.get_attribute("class"), "Velikost XL produktu se neaktivovala po kliknutí."

    # krátký wait před klikem na +
    page.wait_for_timeout(500)
    pridani_mnozstvi = page.locator("input[value='+']")
    pridani_mnozstvi.scroll_into_view_if_needed()
    pridani_mnozstvi.click()
    page.wait_for_timeout(500)  # čekáme na update množství

    # Kontrola množství
    assert int(page.locator("input[name='quantity']").input_value()) == 2, "Nepasuje množství zboží."

    # Přidání do košíku
    page.get_by_role("button", name="Add to cart").click()

    # kontrola popup košíku
    modal = page.get_by_text("Products in your cart")
    try:
        expect(modal).to_be_visible(timeout=5000)
    except Exception:
        raise AssertionError("Není zobrazen popup košík po kliknutí na Add to cart.")

    # otevření stránky košíku
    page.get_by_role("button", name="Shopping cart").click()
    assert page.get_by_role("heading", name="your cart").is_visible(), "Nezobrazuje se stránka košíku"

    # kontrola množství v košíku
    assert int(page.locator("input[name='quantity']").input_value()) == 2, "Nepasuje množství zboží v košíku."

def test_prihlaseni_neregistrovaneho_uzivatele(page: Page):
    """Test přihlášení neregistrovaného uživatele s prázdným košíkem a ověření popupu 'Please add an item first'"""

    # Přechod do obchodu
    odkaz_shop = page.get_by_role("link", name="SHOP")
    odkaz_shop.hover()
    odkaz_international = page.get_by_role("link", name="INTERNATIONAL")
    odkaz_international.click()

    # Přechod na Login stránku
    page.get_by_role("link", name="Login").click()

    # Ověření, že jsme na správné stránce
    expected_url = "https://eu.amonamarth.shop/en/user/login.html"
    assert page.url == expected_url, f"Není otevřená stránka přihlášení. Aktuální URL: {page.url}"


    # Vyplnění přihlašovacích polí
    email_input = page.locator("#loginUserEmailForm")
    email_input.fill("aaa@bbb.cz")
    page.wait_for_timeout(500)  # malá pauza, aby stránka stihla reagovat
    password_input = page.locator("#loginUserPassForm")
    password_input.fill("123456789")
    page.wait_for_timeout(500)  # malá pauza, aby stránka stihla reagovat

    # Reálný klik myší na tlačítko odeslání
    login_button = page.locator("#sentLoginForm")
    login_button.scroll_into_view_if_needed()
    login_button.hover()
    page.wait_for_timeout(500)  # malá pauza, aby stránka stihla reagovat
    box = login_button.bounding_box()
    page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)

    # Čekání na popup
    popup = page.locator("#swal2-content")
    popup.wait_for(state="visible", timeout=10000)
    assert popup.is_visible(), "Popup hláška se nezobrazila"
    assert "Please add an item first" in popup.inner_text(), f"Neočekávaný popup: {popup.inner_text()}"