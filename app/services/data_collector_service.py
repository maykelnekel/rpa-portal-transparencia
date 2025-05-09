import os
import base64
import asyncio
from datetime import datetime
from patchright.async_api import async_playwright, Page, Locator
from typing import List

from app.models.person import SearchResults
from app.config import settings
from app.models.person import PersonBenefict, PersonDetails

from app.utils.wait_for_page_loading import wait_for_page_loading
from app.utils.handle_mouse_move import handle_mouse_move
from app.utils.errors.CustomError import CustomError
from app.utils.validate_if_is_name_cpf_or_nis import validate_if_is_name_cpf_or_nis

screenshot_path = "page.png"


async def goto_gov_page(page: Page, cookie_btn: Locator):
    # acessa o portal do governo
    await page.goto(settings.PORTAL_URL)

    # aguarda o carregamento da pagina
    await wait_for_page_loading(page)

    # move o mouse aleatoriamente para ajudar a evitar a detecção de bot
    await handle_mouse_move(page)

    # clica no botão de aceitar cookies se existir
    if await cookie_btn.is_visible():
        await cookie_btn.click()

    # move o mouse aleatoriamente para ajudar a evitar a detecção de bot
    await handle_mouse_move(page)


async def access_person_consult_page(page: Page, cookie_btn: Locator):
    # encontra e clica no botão de consultar pessoa física
    await page.locator("a#link-consulta-pessoa-fisica").click()

    # move o mouse aleatoriamente para ajudar a evitar a detecção de bot
    await wait_for_page_loading(page)

    # move o mouse aleatoriamente para ajudar a evitar a detecção de bot
    await handle_mouse_move(page)

    if await cookie_btn.is_visible():
        await cookie_btn.click()

    await handle_mouse_move(page)


async def search_person_and_access_data(
    page: Page, cookie_btn: Locator, input_data: str, filter: bool = False
):
    if filter is True:
        await page.locator("button.header").click()

        await page.locator("div.br-checkbox").filter(
            has_text="Beneficiário de Programa Social"
        ).click()

    await handle_mouse_move(page)

    input_field = page.locator("#termo")
    if await input_field.is_visible() and await input_field.is_enabled():
        await input_field.fill(input_data)

        await input_field.press("Enter")

    await handle_mouse_move(page)

    await handle_mouse_move(page)

    search_name_link = page.locator("a.link-busca-nome").nth(0)
    if await search_name_link.is_visible():
        await handle_mouse_move(page)
        await search_name_link.click()
    else:
        validation = validate_if_is_name_cpf_or_nis(input_data)
        if validation == "name":
            raise CustomError(
                "Foram encontrados 0 resultados para o termo…",
                404,
            )
        else:
            raise CustomError(
                "Não foi possível retornar os dados no tempo de resposta solicitado",
                404,
            )

    await wait_for_page_loading(page)

    await handle_mouse_move(page)

    if await cookie_btn.is_visible():
        await cookie_btn.click()


async def get_general_data(page: Page, person_data_row: List[Locator]) -> dict:
    results = {}
    for person_data_index, person_data in enumerate(person_data_row):

        await handle_mouse_move(page)
        if person_data_index == len(person_data_row) - 1:
            break

        await handle_mouse_move(page)
        key = await person_data.locator("strong").inner_text()
        value = await person_data.locator("span").inner_text()
        results[key.strip().lower()] = value.strip()

    return results


async def get_detailed_values(
    page: Page,
    recieved_incomes_thead: List[Locator],
    recieved_incomes_values: List[Locator],
) -> List[PersonDetails]:

    recieved_incomes_keys: List[str] = []
    details: List[PersonDetails] = []

    for th in recieved_incomes_thead:
        text = await th.inner_text()
        recieved_incomes_keys.append(text.strip())

    for tr in recieved_incomes_values:
        await handle_mouse_move(page)

        item = await tr.locator("td").all()
        personal_details: PersonDetails = {}
        for i, td in enumerate(item):
            await handle_mouse_move(page)
            income_value = await td.inner_text()
            personal_details[recieved_incomes_keys[i]] = income_value.strip()
            details.append(personal_details)

    return details


async def get_beneficts(
    page: Page, cookie_btn: Locator, all_beneficts: int
) -> List[PersonBenefict]:
    beneficts: List[PersonBenefict] = []

    for benefict_index in range(all_beneficts):
        await handle_mouse_move(page)
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

        actual_benefict: PersonBenefict = {}
        actual_benefict["nome_do_beneficio"] = benefict_name
        actual_benefict["valor"] = recieved_value.strip()

        await handle_mouse_move(page)

        await wait_for_page_loading(page)

        await handle_mouse_move(page)

        if await cookie_btn.is_visible():
            await cookie_btn.click()

        asyncio.sleep(1)

        recieved_incomes_thead = await page.locator("th").all()

        recieved_incomes_values = await page.locator("tr").all()

        benefict_deatils = await get_detailed_values(
            page=page,
            recieved_incomes_thead=recieved_incomes_thead,
            recieved_incomes_values=recieved_incomes_values,
        )
        actual_benefict["detalhes"] = benefict_deatils

        beneficts.append(actual_benefict)

        await handle_mouse_move(page)

        await page.go_back()
        await wait_for_page_loading(page)

        if await cookie_btn.is_visible():
            await cookie_btn.click()

        await handle_mouse_move(page)

        await page.locator("button.header").nth(0).click()

        return beneficts


async def collect_data_async_service(
    input_data: str, filter: bool = False
) -> SearchResults:
    try:
        results: SearchResults = {
            "termo_da_busca": input_data,
            "data_consulta": datetime.now().isoformat(),
        }

        playwright = await async_playwright().start()

        browser = await playwright.chromium.launch(headless=True)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        options = await browser.new_context(user_agent=user_agent)

        page = await options.new_page()

        # salva o locator para o botão de aceitar cookies
        cookie_btn = page.locator("#accept-all-btn")
        # acessa o portal do governo
        await goto_gov_page(page, cookie_btn)

        # acessa a pagina de consulta de pessoa física
        await access_person_consult_page(page, cookie_btn)

        # realiza a busca da pessoa física e acessa o primeiro resultado
        await search_person_and_access_data(
            page=page, cookie_btn=cookie_btn, input_data=input_data, filter=filter
        )

        incomes_button = page.locator("button.header")

        await handle_mouse_move(page)

        await asyncio.sleep(0.3)

        if await incomes_button.is_visible() and await incomes_button.is_enabled():
            await incomes_button.click()

        await handle_mouse_move(page)

        await page.wait_for_load_state()

        await handle_mouse_move(page)

        await page.screenshot(path=screenshot_path, full_page=True)

        person_data_row = await page.locator(
            "section.dados-tabelados > div.row > div"
        ).all()

        # pega os dados gerais
        person_data = await get_general_data(page, person_data_row)

        # adiciona os dados gerais ao resultado
        results.update(person_data)

        all_beneficts = await page.locator(
            "div.responsive > table > tbody > tr"
        ).count()

        # coleta todos os beneficios
        beneficts = await get_beneficts(
            page=page, cookie_btn=cookie_btn, all_beneficts=all_beneficts
        )

        # adiciona os beneficios ao resultado
        results["beneficios"] = beneficts

        await browser.close()

        # converte o screenshot para base64 e adiciona ao resultado
        with open(screenshot_path, "rb") as img_file:
            results["screenshot_base64"] = base64.b64encode(img_file.read()).decode(
                "utf-8"
            )
        os.remove(screenshot_path)

        results["data_consulta"] = datetime.now().isoformat()

        return results

    except CustomError as e:
        await browser.close()
        raise CustomError(e.mensagem, e.status_code)
    except Exception as e:
        await browser.close()
        raise e
