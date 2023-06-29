import asyncio
import csv
import aiohttp
import pandas as pd
from playwright.async_api import async_playwright


async def find_linkedin_urls(csv_file):
    df = pd.read_csv(csv_file)

    async with aiohttp.ClientSession() as session:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()

            for index, row in df.iterrows():
                company_name = row['Company']
                url = f'https://www.google.com/search?q={company_name} LinkedIn'

                await page.goto(url)
                linkedin_url = await page.evaluate('document.querySelector(".yuRUbf a").href')

                df.loc[index, 'LinkedIn URL'] = linkedin_url

            await browser.close()

    return df


async def find_employee_count(csv_file):
    df = pd.read_csv(csv_file)

    async with aiohttp.ClientSession() as session:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()

            for index, row in df.iterrows():
                linkedin_url = row['LinkedIn URL']

                await page.goto(linkedin_url)
                employee_count = await page.evaluate('document.querySelector(".org-top-card-summary-info-list__info-item:nth-child(2)").innerText')

                df.loc[index, 'Employee Count'] = employee_count

            await browser.close()

    return df


async def process_csv(csv_file):
    try:
        linkedin_df = await find_linkedin_urls(csv_file)
        with_employee_count_df = await find_employee_count(linkedin_df)
        with_employee_count_df.to_csv('result_with_employee_count.csv', index=False)
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
