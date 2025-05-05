from playwright.sync_api import sync_playwright
import base64
import json
import os
from datetime import datetime
from time import sleep


def coletar_dados(inputData):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        page.goto(
            f"https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?termo={inputData}&pagina=1&tamanhoPagina=10"
        )

        page.wait_for_load_state("load")

        cookie_btn = page.locator("#accept-all-btn")
        if cookie_btn.is_visible():
            cookie_btn.click()

        page.wait_for_selector("span#resultados")

        search_name_link = page.locator("a.link-busca-nome").nth(0)
        if search_name_link.is_visible():
            search_name_link.click()
        else:
            print(f"no data was found for {inputData}")

        page.wait_for_load_state("load")

        if cookie_btn.is_visible():
            cookie_btn.click()

        incomes_button = page.locator("button.header")

        sleep(0.3)

        if incomes_button.is_visible() and incomes_button.is_enabled():
            incomes_button.click()
        else:
            print("button incomes not found")

        page.wait_for_load_state()

        benefict_name = page.locator("div.responsive > strong").nth(0).inner_text()
        response = page.locator("div.responsive > table > tbody > tr").nth(0)

        recieved_value = response.locator("td").nth(-1).inner_text().strip()
        response.locator("td > a").nth(0).click()

        page.wait_for_load_state("load")

        sleep(15)

        page.wait_for_load_state("load")

        if cookie_btn.is_visible():
            cookie_btn.click()

        screenshot_path = f"page_{datetime.now().isoformat()}.png"

        recieved_incomes_thead = page.locator("th").all()

        sleep(1)

        recieved_incomes_keys = []

        for th in recieved_incomes_thead:
            recieved_incomes_keys.append(th.inner_text().strip())

        sleep(1)

        recieved_incomes_values = page.locator("tr").all()
        beneficts = []

        for tr in recieved_incomes_values:
            item = tr.locator("td").all()
            data = {}
            for i, td in enumerate(item):
                data[recieved_incomes_keys[i]] = td.inner_text().strip()
                beneficts.append(data)

        page.screenshot(path=screenshot_path, full_page=True)

        with open(screenshot_path, "rb") as img_file:
            imagem_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        results = {
            "termo_da_busca": inputData,
            "data_consulta": datetime.now().isoformat(),
            "beneficio": benefict_name,
            "valor": recieved_value,
            "beneficios": [beneficts],
            "imagem_base64": imagem_base64,
        }

        browser.close()
        os.remove(screenshot_path)
        print(results)
        return results


def main():
    dados = coletar_dados("maykel felipe")
    with open("results.json", "w") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


# Teste simples
if __name__ == "__main__":
    main()
