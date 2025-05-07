import os
import base64

from playwright.async_api import async_playwright
from app.models.person import SearchResults
from app.config import settings
from datetime import datetime
from time import sleep


async def collect_data_async(input_data: str, filter: bool = False) -> SearchResults:
    with async_playwright() as p:
        try:
            results = {
                "termo_da_busca": input_data,
                "data_consulta": datetime.now().isoformat(),
            }
            browser = p.firefox.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            await page.goto(settings.PORTAL_URL)

            await page.wait_for_load_state("load")

            cookie_btn = page.locator("#accept-all-btn")

            if cookie_btn.is_visible():
                await cookie_btn.click()

            await page.locator("a#link-consulta-pessoa-fisica").click()

            await page.wait_for_load_state("load")

            if cookie_btn.is_visible():
                await cookie_btn.click()

            sleep(1)

            if filter is True:
                await page.locator("button.header").click()
                sleep(1)
                await page.locator("div.br-checkbox").filter(
                    has_text="Beneficiário de Programa Social"
                ).click()

            input_field = page.locator("#termo")
            if input_field.is_visible() and input_field.is_enabled():
                await input_field.fill(input_data)
                sleep(1)
                await input_field.press("Enter")

            await page.wait_for_selector("span#resultados")

            search_name_link = page.locator("a.link-busca-nome").nth(0)
            if search_name_link.is_visible():
                await search_name_link.click()
            else:
                print(f"no data was found for {input_data}")

            await page.wait_for_load_state("load")

            if cookie_btn.is_visible():
                await cookie_btn.click()

            incomes_button = page.locator("button.header")

            sleep(0.3)

            if incomes_button.is_visible() and incomes_button.is_enabled():
                await incomes_button.click()
            else:
                print("button incomes not found")

            await page.wait_for_load_state()

            beneficts = []
            benefict_deatils = []

            screenshot_path = "page.png"
            await page.screenshot(path=screenshot_path, full_page=True)

            person_data_row = page.locator(
                "section.dados-tabelados > div.row > div"
            ).all()

            for person_data_index, person_data in enumerate(person_data_row):
                if person_data_index == len(person_data_row) - 1:
                    break
                key = person_data.locator("strong").inner_text().strip().lower()
                value = person_data.locator("span").inner_text().strip()
                results[key] = value

            all_beneficts = page.locator("div.responsive > table > tbody > tr").count()

            for benefict_index in range(all_beneficts):
                benefict_name = (
                    page.locator("div.responsive > strong")
                    .nth(benefict_index)
                    .inner_text()
                )
                response = page.locator("div.responsive > table > tbody > tr").nth(
                    benefict_index
                )

                recieved_value = response.locator("td").nth(-1).inner_text().strip()
                await response.locator("td > a").nth(0).click()

                actual_benefict = {}
                actual_benefict["nome_do_beneficio"] = benefict_name
                actual_benefict["valor"] = recieved_value

                await page.wait_for_load_state("load")

                if benefict_index == 0:
                    sleep(13)
                    await page.wait_for_load_state("load")
                else:
                    sleep(1)

                if cookie_btn.is_visible():
                    await cookie_btn.click()

                recieved_incomes_thead = page.locator("th").all()

                sleep(1)

                recieved_incomes_keys = []

                for th in recieved_incomes_thead:
                    recieved_incomes_keys.append(th.inner_text().strip())

                sleep(1)

                recieved_incomes_values = page.locator("tr").all()

                for tr in recieved_incomes_values:
                    item = tr.locator("td").all()
                    data = {}
                    for i, td in enumerate(item):
                        data[recieved_incomes_keys[i]] = td.inner_text().strip()
                        benefict_deatils.append(data)

                actual_benefict["detalhes"] = benefict_deatils
                beneficts.append(actual_benefict)
                results["beneficios"] = beneficts

                await page.go_back()
                await page.wait_for_load_state("load")
                sleep(1)
                if cookie_btn.is_visible():
                    await cookie_btn.click()
                await page.locator("button.header").nth(0).click()

            browser.close()
            with open(screenshot_path, "rb") as img_file:
                results["screenshot_base64"] = base64.b64encode(img_file.read()).decode(
                    "utf-8"
                )
            os.remove(screenshot_path)

            results["data_consulta"] = datetime.now().isoformat()

            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            raise ValueError(
                {
                    "message": str(e),
                    "termo_da_busca": input_data,
                    "data_consulta": datetime.now().isoformat(),
                }
            )
