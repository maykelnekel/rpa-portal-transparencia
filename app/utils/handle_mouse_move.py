from playwright.async_api import Page
import random


async def handle_mouse_move(page: Page):
    await page.mouse.move(random.random() * 800, random.random() * 800)
