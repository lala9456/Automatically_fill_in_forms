import asyncio
from playwright.async_api import async_playwright
import pandas as pd

team_name = "我想爬玉山拜託抽到排雲天氣晴"
stay_days = 2
start_date = "2025-03-12"
end_date = "2025-03-13"


# 讀取 CSV，強制 '手機' 和 '電話' 欄位為字串
df = pd.read_csv("namelist.csv", dtype={"手機號碼": str, "電話": str,"緊急聯絡電話":str})

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://hike.taiwan.gov.tw/apply_1_2.aspx?unit=c951cdcd-b75a-46b9-8002-8ef952ec95fd&cid=2&fid=1&camp_id=0")
        await asyncio.sleep(1)
        await page.locator("input[name='chk[]']").nth(0).check()  # 勾選第一個
        await page.locator("input[name='chk[]']").nth(1).check()  # 勾選第二個
        await page.locator("input[name='chk[]']").nth(2).check()  #
        await page.locator("input[name='chk[]']").nth(16).check()  # 
        await page.locator("input[name='chk[]']").nth(17).check()
        await page.locator("input[name='chk[]']").nth(18).check()
        await asyncio.sleep(1)
        await page.click("#con_btnagree")  # 點擊「同意」按鈕(id定位)
        await asyncio.sleep(1)
        await page.fill("#con_teams_name", team_name)  # 填入隊名
        # 讓程式等待使用者手動關閉
        await page.select_option("#con_sumday", str(stay_days))  # 選擇「共2天」
        await page.select_option("#con_applystart", start_date)  # 選擇 2025-03-12

        #
        await page.locator("label:has-text('排雲登山服務中心')").click()
        await asyncio.sleep(1)
        await page.locator("label:has-text('塔塔加登山口')").click()
        await asyncio.sleep(1)
        await page.locator("label:has-text('排雲山莊')").click()
        await asyncio.sleep(1)
        await page.locator("a:has-text('完成路線')").click()   # a標籤
        await asyncio.sleep(1)
        await page.locator("label:has-text('玉山主峰')").click()
        await asyncio.sleep(1)
        await page.locator("label:has-text('塔塔加登山口')").click()
        await asyncio.sleep(1)
        await page.locator("label:has-text('排雲登山服務中心')").click()
        await asyncio.sleep(1)
        await page.locator("a:has-text('完成路線')").click()   # a標籤
        await asyncio.sleep(1)

        await page.locator("#con_snowtbChk1").click()   
        await page.locator("#con_snowtbChk2").click() 

        await page.locator("a:has-text('下一步')").click()   # a標籤
        await asyncio.sleep(1)
        


        await page.locator("#con_applycheck").click()   
        await asyncio.sleep(1)
        #領隊
        await page.fill("#con_apply_name", df.iloc[0]["姓名"])
        await page.fill("#con_apply_tel", df.iloc[0]["電話"])
        await page.select_option("#con_ddlapply_country", df.iloc[0]["聯絡地址_縣市"])
        await asyncio.sleep(1)
        await page.select_option("#con_ddlapply_city", df.iloc[0]["聯絡地址_區"])
        await page.fill("#con_apply_addr", df.iloc[0]["聯絡地址_街道"])


        await page.fill("#con_apply_mobile", df.iloc[0]["手機號碼"])
        await page.fill("#con_apply_email", df.iloc[0]["Email"])
        await asyncio.sleep(1)
        await page.locator("#con_apply_nation").scroll_into_view_if_needed()
        await page.select_option("#con_apply_nation", "中華民國")
        page.locator("#con_apply_sid").scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await page.fill("#con_apply_sid", df.iloc[0]["身分證號"])
        await asyncio.sleep(1)
        page.locator("#con_apply_sex").scroll_into_view_if_needed()
        await page.select_option("#con_apply_sex", df.iloc[0]["性別"])
 
  

        await page.locator("#con_apply_birthday").scroll_into_view_if_needed()
        await page.evaluate("document.getElementById('con_apply_birthday').removeAttribute('readonly')")
        await page.fill("#con_apply_birthday", df.iloc[0]["生日"])
        await page.locator("#con_apply_birthday").press("Enter")  # 按下 Enter

        await page.locator("#con_apply_contactname").click()
        await asyncio.sleep(1)
        await page.fill("#con_apply_contactname", df.iloc[0]["緊急聯絡人"])
        await page.fill("#con_apply_contacttel", df.iloc[0]["緊急聯絡電話"])
        await asyncio.sleep(1)

        await page.locator("button:has-text('領隊資料(請展開填寫資料)')").click()
        await asyncio.sleep(1)
        await page.locator("#con_copyapply").click() 
        # await page.check("#con_rblNode_0")  # 選擇該單選按鈕
        # await asyncio.sleep(1)
        # await page.check("#con_rblNode_0")  # 選擇該單選按鈕
        # await asyncio.sleep(1)

        input("瀏覽器已開啟，請手動關閉後按 Enter 繼續...")

        await browser.close()

asyncio.run(main())
