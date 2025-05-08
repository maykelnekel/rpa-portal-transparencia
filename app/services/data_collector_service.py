import os
import base64
import random
import asyncio
from datetime import datetime
from patchright.async_api import async_playwright

from app.models.person import SearchResults
from app.config import settings


async def collect_data_async(input_data: str, filter: bool = False) -> SearchResults:
    try:
        results = {
            "termo_da_busca": input_data,
            "data_consulta": datetime.now().isoformat(),
        }

        playwright = await async_playwright().start()

        browser = await playwright.chromium.launch(headless=True)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        options = await browser.new_context(user_agent=user_agent)

        page = await options.new_page()

        await page.goto(settings.PORTAL_URL)

        await page.wait_for_load_state("load")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        cookie_btn = page.locator("#accept-all-btn")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        if await cookie_btn.is_visible():
            await cookie_btn.click()

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.locator("a#link-consulta-pessoa-fisica").click()

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.wait_for_load_state("load")

        if await cookie_btn.is_visible():
            await cookie_btn.click()

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.mouse.move(random.random() * 800, random.random() * 800)

        if filter is True:
            await page.locator("button.header").click()

            await page.locator("div.br-checkbox").filter(
                has_text="Beneficiário de Programa Social"
            ).click()

        await page.mouse.move(random.random() * 800, random.random() * 800)

        input_field = page.locator("#termo")
        if await input_field.is_visible() and await input_field.is_enabled():
            await input_field.fill(input_data)

            await input_field.press("Enter")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.wait_for_selector("span#resultados")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        search_name_link = page.locator("a.link-busca-nome").nth(0)
        if await search_name_link.is_visible():
            await page.mouse.move(random.random() * 800, random.random() * 800)
            await search_name_link.click()
        else:
            print(f"no data was found for {input_data}")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.wait_for_load_state("load")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        if await cookie_btn.is_visible():
            await cookie_btn.click()

        incomes_button = page.locator("button.header")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await asyncio.sleep(0.3)

        if await incomes_button.is_visible() and await incomes_button.is_enabled():
            await incomes_button.click()
        else:
            print("button incomes not found")

        await page.mouse.move(random.random() * 800, random.random() * 800)

        await page.wait_for_load_state()

        beneficts = []
        benefict_deatils = []

        await page.mouse.move(random.random() * 800, random.random() * 800)

        screenshot_path = "page.png"
        await page.screenshot(path=screenshot_path, full_page=True)

        person_data_row = await page.locator(
            "section.dados-tabelados > div.row > div"
        ).all()

        await page.mouse.move(random.random() * 800, random.random() * 800)

        for person_data_index, person_data in enumerate(person_data_row):

            await page.mouse.move(random.random() * 800, random.random() * 800)
            if person_data_index == len(person_data_row) - 1:
                break

            await page.mouse.move(random.random() * 800, random.random() * 800)
            key = await person_data.locator("strong").inner_text()
            value = await person_data.locator("span").inner_text()
            results[key.strip().lower()] = value.strip()

        all_beneficts = await page.locator(
            "div.responsive > table > tbody > tr"
        ).count()

        for benefict_index in range(all_beneficts):
            await page.mouse.move(random.random() * 800, random.random() * 800)
            benefict_name = (
                await page.locator("div.responsive > strong")
                .nth(benefict_index)
                .inner_text()
            )
            response = page.locator("div.responsive > table > tbody > tr").nth(
                benefict_index
            )

            recieved_value = await response.locator("td").nth(-1).inner_text()
            await response.locator("td > a").nth(0).click()

            actual_benefict = {}
            actual_benefict["nome_do_beneficio"] = benefict_name
            actual_benefict["valor"] = recieved_value.strip()

            await page.mouse.move(random.random() * 800, random.random() * 800)

            await page.wait_for_load_state("load")

            await page.mouse.move(random.random() * 800, random.random() * 800)

            if await cookie_btn.is_visible():
                await cookie_btn.click()

            recieved_incomes_thead = await page.locator("th").all()

            await page.mouse.move(random.random() * 800, random.random() * 800)

            recieved_incomes_keys = []

            for th in recieved_incomes_thead:
                text = await th.inner_text()
                recieved_incomes_keys.append(text.strip())

            await page.mouse.move(random.random() * 800, random.random() * 800)

            recieved_incomes_values = await page.locator("tr").all()

            for tr in recieved_incomes_values:
                await page.mouse.move(random.random() * 800, random.random() * 800)

                item = await tr.locator("td").all()
                data = {}
                for i, td in enumerate(item):
                    await page.mouse.move(random.random() * 800, random.random() * 800)
                    income_value = await td.inner_text()
                    data[recieved_incomes_keys[i]] = income_value.strip()
                    benefict_deatils.append(data)

            actual_benefict["detalhes"] = benefict_deatils
            beneficts.append(actual_benefict)
            results["beneficios"] = beneficts

            await page.mouse.move(random.random() * 800, random.random() * 800)

            await page.go_back()
            await page.wait_for_load_state("load")

            if await cookie_btn.is_visible():
                await cookie_btn.click()

            await page.mouse.move(random.random() * 800, random.random() * 800)

            await page.locator("button.header").nth(0).click()

        await browser.close()
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
                "mensagem": str(e),
                "termo_da_busca": input_data,
                "data_consulta": datetime.now().isoformat(),
            }
        )
