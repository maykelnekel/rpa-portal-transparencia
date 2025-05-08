from playwright.async_api import Page


async def wait_for_page_loading(page: Page):
    await page.wait_for_load_state("load")
