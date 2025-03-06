import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import ddddocr
from PIL import Image
from datetime import datetime

team_name = "我想爬玉山拜託抽到排雲天氣晴"
stay_days = 2
start_date = "2025-05-01"




start_date_obj = datetime.strptime("2025-05-01", "%Y-%m-%d")


# 讀取 CSV，強制 '手機' 和 '電話' 欄位為字串
df = pd.read_csv("namelist.csv", dtype={"手機號碼": str, "電話": str,"緊急聯絡電話":str})
df_stay = pd.read_csv("stay_info.csv",dtype={"手機號碼": str})
stay_people_name = df_stay.iloc[0]["姓名"]
stay_people_number = df_stay.iloc[0]["手機號碼"]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto("https://hike.taiwan.gov.tw/apply_1_2.aspx?unit=c951cdcd-b75a-46b9-8002-8ef952ec95fd&cid=2&fid=1&camp_id=0")
            await asyncio.sleep(10)
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
            if start_date_obj.month in [12,1,2,3]:
                try:
                    await page.locator("#con_snowtbChk1").click()   
                    await page.locator("#con_snowtbChk2").click() 
                except:
                    print("沒有雪季按鈕")
            await page.locator("a:has-text('下一步')").scroll_into_view_if_needed()
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
            await page.locator("#con_apply_sid").scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await page.fill("#con_apply_sid", df.iloc[0]["身分證號"])
            await asyncio.sleep(1)
            await page.locator("#con_apply_sex").scroll_into_view_if_needed()
            await page.select_option("#con_apply_sex", df.iloc[0]["性別"])
    
    

            await page.locator("#con_apply_birthday").scroll_into_view_if_needed()
            birthday_value = df.iloc[0]["生日"]
            await page.evaluate("""
                (birthday) => {
                    let input = document.getElementById('con_apply_birthday');
                    input.removeAttribute('readonly');  // 確保移除 readonly
                    input.value = birthday;  // 直接設定值
                    input.dispatchEvent(new Event('change', { bubbles: true }));  // 觸發 change 事件
                }
            """, birthday_value)

            # await page.evaluate("document.getElementById('con_apply_birthday').removeAttribute('readonly')")
            # await page.locator("#con_apply_birthday").click()
            # await page.fill("#con_apply_birthday", df.iloc[0]["生日"])
            # await page.locator("#con_apply_birthday").press("Enter")  # 按下 Enter

            await page.locator("#con_apply_contactname").click()
            await asyncio.sleep(1)
            await page.fill("#con_apply_contactname", df.iloc[0]["緊急聯絡人"])
            await page.fill("#con_apply_contacttel", df.iloc[0]["緊急聯絡電話"])
            await asyncio.sleep(1)

            await page.locator("button:has-text('領隊資料(請展開填寫資料)')").click()
            await asyncio.sleep(1)
            await page.locator("#con_copyapply").click() 

            await page.locator("button:has-text('隊員資料(請展開填寫資料)')").click()
            for _ in range(len(df)-1):
                await page.locator("#con_lbInsMember").click()
                await asyncio.sleep(1)
            await page.locator("button:has-text('展開全部隊員')").click()

            ########隊員
            table_idx = 0
            for i in range(1,len(df)):
                await page.fill(f"#con_lisMem_member_name_{table_idx}", df.iloc[i]["姓名"])
                await page.fill(f"#con_lisMem_member_tel_{table_idx}", df.iloc[i]["電話"])
                await page.select_option(f"#con_lisMem_ddlmember_country_{table_idx}", df.iloc[i]["聯絡地址_縣市"])
                await asyncio.sleep(1)
                await page.select_option(f"#con_lisMem_ddlmember_city_{table_idx}", df.iloc[i]["聯絡地址_區"])
                await page.fill(f"#con_lisMem_member_addr_{table_idx}", df.iloc[i]["聯絡地址_街道"])


                await page.fill(f"#con_lisMem_member_mobile_{table_idx}", df.iloc[i]["手機號碼"])
                await page.fill(f"#con_lisMem_member_email_{table_idx}", df.iloc[i]["Email"])
                await asyncio.sleep(1)
                await page.locator(f"#con_lisMem_member_nation_{table_idx}").scroll_into_view_if_needed()
                await page.select_option(f"#con_lisMem_member_nation_{table_idx}", "中華民國")
                await page.locator(f"#con_lisMem_member_sid_{table_idx}").scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await page.fill(f"#con_lisMem_member_sid_{table_idx}", df.iloc[i]["身分證號"])
                await asyncio.sleep(1)
                await page.locator(f"#con_lisMem_member_sex_{table_idx}").scroll_into_view_if_needed()
                await page.select_option(f"#con_lisMem_member_sex_{table_idx}", df.iloc[i]["性別"])
        
        

                await page.locator(f"#con_lisMem_member_birthday_{table_idx}").scroll_into_view_if_needed()
                birthday_input_id = f"con_lisMem_member_birthday_{table_idx}"
                birthday_value = df.iloc[i]["生日"]

                await page.evaluate("""
                    ({ inputId, birthday }) => {
                        let input = document.getElementById(inputId);
                        input.removeAttribute('readonly');  // 確保移除 readonly
                        input.value = birthday;  // 直接設定值
                        input.dispatchEvent(new Event('change', { bubbles: true }));  // 觸發 change 事件
                    }
                """, {"inputId": birthday_input_id, "birthday": birthday_value})


                # await page.evaluate("document.getElementById('con_apply_birthday').removeAttribute('readonly')")
                # await page.locator("#con_apply_birthday").click()
                # await page.fill("#con_apply_birthday", df.iloc[i]["生日"])
                # await page.locator("#con_apply_birthday").press("Enter")  # 按下 Enter

                await page.locator(f"#con_lisMem_member_contactname_{table_idx}").click()
                await asyncio.sleep(1)
                await page.fill(f"#con_lisMem_member_contactname_{table_idx}", df.iloc[i]["緊急聯絡人"])
                await page.fill(f"#con_lisMem_member_contacttel_{table_idx}", df.iloc[i]["緊急聯絡電話"])
                await asyncio.sleep(1)
                table_idx = table_idx + 1

            ####留守人
            await page.locator("button:has-text('留守人資料(請展開填寫資料)')").click()
            await page.fill(f"#con_stay_name", stay_people_name)
            await page.fill(f"#con_stay_mobile", stay_people_number)

            ### 驗證碼截圖
            await page.locator("#con_imgcode").screenshot(path="captcha.png")

            ## 辨識驗證碼
            ocr = ddddocr.DdddOcr()
            with open("captcha.png", "rb") as f:
                captcha_text = ocr.classification(f.read())
            print(f"辨識出的驗證碼: {captcha_text}")

            await page.fill(f"#con_vcode", captcha_text)  ##送驗證碼
            await page.locator("a:has-text('下一步')").click()


            
            input("瀏覽器已開啟，請手動關閉後按 Enter 繼續...")
        except Exception as e:
            print(f"⚠️ 發生錯誤: {e}")
            input("❗ 瀏覽器保持開啟，請手動檢查錯誤後按 Enter 繼續...")  # 等待手動關閉

        finally:
            input("✅ 填寫完成，請手動確認後按 Enter 關閉瀏覽器...")
            await browser.close()  # **手動確認後才關閉瀏覽器**


        # await browser.close()

asyncio.run(main())
