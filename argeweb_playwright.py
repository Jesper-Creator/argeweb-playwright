from playwright.sync_api import sync_playwright


def insert_subdomain_dns(fqdn, cname=None, a=None, mx=None, aaaa=None, txt=None, srv=None, prio=None, ttl=600, username='name', password='password'):
    '''
    Install Chromium Web-browser (Most optimized):
    playwright install chromium
    '''
    domain = '.'.join(fqdn.split('.')[-2:])
    subdomain = '.'.join(fqdn.split('.')[:-2])
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Going to website...")
        # Go to https://www.argeweb.nl/argecs/login
        page.goto("https://www.argeweb.nl/argecs/login")
        print("Logging in...")
        # Click text=Accepteren
        page.click("text=Accepteren")
        # Fill input[name="username"]
        page.fill("input[name=\"username\"]", f"{username}")
        # Fill input[name="password"]
        page.fill("input[name=\"password\"]", f"{password}")
        # Click text=Login
        # with page.expect_navigation(url="https://www.argeweb.nl/argecs/"):
        with page.expect_navigation():
            page.click("text=Login")
        print("Navigating to DNS...")
        # Click text=Beheren
        page.click("text=Beheren")
        # Click #item_1830
        page.click("#item_1830")
        assert page.url == "https://www.argeweb.nl/argecs/#hi_domein"
        # Click a:has-text("DNS")
        page.click("a:has-text(\"DNS\")")
        assert page.url == f"https://www.argeweb.nl/argecs/#hi_dns_edit_zone?CS_dienst_id={domain}"

        print("Filling in details...")
        # Fill input[name="subdomain"]
        page.fill("input[name=\"subdomain\"]", f"{subdomain}")
        # Fill input[name="prio"]
        page.fill("input[name=\"prio\"]", f"{prio}")
        # Fill input[name="ttl"]
        page.fill("input[name=\"ttl\"]", f"{ttl}")
        if cname:
            # Select CNAME
            page.select_option("select[name=\"type\"]", "CNAME")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{cname}")
        elif a:
            # Select A
            page.select_option("select[name=\"type\"]", "A")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{a}")
        elif mx:
            # Select MX
            page.select_option("select[name=\"type\"]", "MX")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{mx}")
        elif aaaa:
            # Select AAA
            page.select_option("select[name=\"type\"]", "AAAA")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{aaaa}")
        elif txt:
            # Select TXT
            page.select_option("select[name=\"type\"]", "TXT")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{txt}")
        elif srv:
            # Select SRV
            page.select_option("select[name=\"type\"]", "SRV")
            # Fill input[name="address"]
            page.fill("input[name=\"address\"]", f"{srv}")

        print("Inserting & Checking for errors...")
        # Click text=insert
        page.click("text=insert")

        page.wait_for_load_state("networkidle")
        # Check for insert errors
        if page.query_selector('span[style*="color: red"]'):
            raise ValueError(page.inner_text('span[style*="color: red"]'))
        # Record error span
        elif page.query_selector('#content > div:nth-child(6) > div.overzicht_box_content > form > span:nth-child(4)'):
            raise ValueError(page.inner_text('#content > div:nth-child(6) > div.overzicht_box_content > form > span:nth-child(4)'))
        # Adres error span
        elif page.query_selector('#content > div:nth-child(6) > div.overzicht_box_content > form > table > tbody > tr:nth-child(2) > td:nth-child(5) > span'):
            raise ValueError(page.inner_text('#content > div:nth-child(6) > div.overzicht_box_content > form > table > tbody > tr:nth-child(2) > td:nth-child(5) > span'))
        # TTL error span
        elif page.query_selector('#content > div:nth-child(6) > div.overzicht_box_content > form > table > tbody > tr:nth-child(2) > td:nth-child(4) > span'):
            raise ValueError(page.inner_text('#content > div:nth-child(6) > div.overzicht_box_content > form > table > tbody > tr:nth-child(2) > td:nth-child(4) > span'))

        print("Updating...")
        # Click text=update
        page.click("text=update")

        print("Done!")
        browser.close()


insert_subdomain_dns('full_subdomain', cname='full_address', prio=0, ttl=3600)
