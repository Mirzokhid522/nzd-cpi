from playwright.sync_api import sync_playwright
import time
import os

def run_cpi_workflow():
    project_folder = os.path.abspath(os.path.dirname(__file__))
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            print("Navigating to Infoshare Stats NZ...")
            page.goto("https://infoshare.stats.govt.nz/", timeout=60000)
            
            # Navigate tree structure automatically
            page.wait_for_selector("text=Economic indicators", timeout=15000)
            print("Expanding 'Economic indicators'...")
            page.click("text=Economic indicators")
            
            cpi_selector = "text=Consumers Price Index - CPI"
            page.wait_for_selector(cpi_selector, state="visible", timeout=15000)
            print("Clicking 'Consumers Price Index - CPI'...")
            page.click(cpi_selector, force=True)
            
            print("Waiting for CPI sub-options to load...")
            page.wait_for_selector("text=Contributions to all groups", timeout=20000)
            print("Successfully loaded CPI sub-options view!")

            # Target headline table
            target_table = "CPI All Groups for New Zealand, percentage change (Qrtly-Mar/Jun/Sep/Dec)"
            print(f"Selecting table: '{target_table}'...")
            page.click(f"text={target_table}", force=True)
            
            # Wait for variable configuration page to load
            print("Waiting for variable selection screen...")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Automatically click all "Select all" links so everything is pre-selected up to 2026
            print("Automatically selecting all variables and full time history...")
            select_all_links = page.locator("text=Select all").all()
            for link in select_all_links:
                try:
                    link.click()
                    time.sleep(0.3)
                except:
                    pass

            print("\n" + "="*65)
            print(" [READY] Automation complete up to the export screen!")
            print(" 1. Scroll down to the bottom right dropdown in the browser.")
            print(" 2. Change 'Table on screen' to 'Comma delimited (.csv)'.")
            print(" 3. Click 'Go'. Playwright will intercept it automatically!")
            print("="*65 + "\n")

            # Listen for the download event when you click Go manually
            with page.expect_download(timeout=180000) as download_info:
                print("Waiting for you to change format to CSV and click 'Go'...")
            
            download = download_info.value
            
            # Save it explicitly as cpi.csv right in your project folder
            final_file_path = os.path.join(project_folder, "cpi.csv")
            download.save_as(final_file_path)
            
            print(f"\n[SUCCESS] File successfully captured and saved to: {final_file_path}")
            time.sleep(3)

        except Exception as e:
            print(f"\n[ERROR] Step failed: {e}")
        
        finally:
            browser.close()
            print("Browser closed.")

if __name__ == "__main__":
    run_cpi_workflow()