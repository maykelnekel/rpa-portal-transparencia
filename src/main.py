from playwright.sync_api import sync_playwright
import base64
import json
import os
from datetime import datetime
from time import sleep, gmtime
import asyncio


def coletar_dados(inputData):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        page.goto(
            f"https://portaldatransparencia.gov.br/pessoa-fisica/busca/lista?termo={inputData}&pagina=1&tamanhoPagina=10"
        )
        # page.wait_for_load_state("load")

        # cookie_btn = page.locator("#accept-all-btn")
        # if cookie_btn.is_visible():
        #     cookie_btn.click()

        # cpf_consult_btn = page.locator("#button-consulta-pessoa-fisica")
        # if cpf_consult_btn.is_visible():
        #     cpf_consult_btn.click()

        # page.wait_for_load_state("load")
        # if cookie_btn.is_visible():
        #     cookie_btn.click()

        # refined_search_btn = page.locator('//*[@aria-controls="box-busca-refinada"]')
        # if refined_search_btn.is_visible():
        #     refined_search_btn.click()

        # social_program_checkbox = page.locator('//*[@for="beneficiarioProgramaSocial"]')
        # if social_program_checkbox.is_visible():
        #     social_program_checkbox.click()

        # termo_input = page.locator("input#termo")
        # if termo_input.is_visible():
        #     termo_input.fill(nome)
        #     page.evaluate('document.querySelector("input#termo").value = ""')
        #     termo_input.fill(nome)
        #     sleep(0.3)
        #     termo_input.press("Enter")
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
        # se o botão button.header__button estiver visível, clique nele
        # incomes_button = page.locator(
        #     '//*[@aria-controls="accordion-recebimentos-recursos"]'
        # )
        incomes_button = page.locator("button.header")
        sleep(0.3)
        # print(incomes_button)
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

        screenshot_path = f"page_{datetime.now().isoformat()}.png"

        page.screenshot(path=screenshot_path, full_page=True)

        with open(screenshot_path, "rb") as img_file:
            imagem_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        resultado = {
            "termo_da_busca": inputData,
            "data_consulta": datetime.now().isoformat(),
            "beneficio": benefict_name,
            "valor": recieved_value,
            "imagem_base64": imagem_base64,
            "beneficios": [],
        }

        browser.close()
        # os.remove(screenshot_path)

        return resultado


def main():
    dados = coletar_dados("maykel felipe")
    with open("resultado.json", "w") as f:
        json.dump(dados, f, indent=2)


# Teste simples
if __name__ == "__main__":
    main()
