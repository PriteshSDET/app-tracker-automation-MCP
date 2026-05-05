# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: regression\app_tracker_regression.spec.ts >> app tracker regression flow
- Location: tests\regression\app_tracker_regression.spec.ts:16:5

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - alert [ref=e4]:
    - img [ref=e6]
    - generic [ref=e8]: UAT
  - generic [ref=e9]:
    - banner [ref=e11]:
      - generic [ref=e12]:
        - img "Leap Logo" [ref=e14]
        - button "menu" [active] [ref=e16] [cursor=pointer]:
          - generic [ref=e18]:
            - text: MENU
            - generic [ref=e19]: ▼
    - generic [ref=e20]:
      - generic [ref=e21]:
        - generic [ref=e22]:
          - button "menu" [ref=e23] [cursor=pointer]:
            - img [ref=e25]
          - generic [ref=e27]: Application List
        - button "Submit" [ref=e29] [cursor=pointer]
      - generic [ref=e31]:
        - button "Filter + 2" [ref=e32] [cursor=pointer]:
          - generic [ref=e33]:
            - img [ref=e35]
            - generic [ref=e37]:
              - text: Filter
              - generic [ref=e40]: + 2
        - generic [ref=e41]:
          - generic [ref=e42]: "Sort :"
          - generic [ref=e46] [cursor=pointer]:
            - button "Modified - New to Old" [ref=e47]:
              - generic [ref=e49]: Modified - New to Old
            - textbox: Modified - New to Old
            - img
      - generic [ref=e50]:
        - generic [ref=e51]:
          - generic [ref=e53] [cursor=pointer]:
            - generic [ref=e54]:
              - generic [ref=e55]: LA53541792 | messer tgxzb
              - generic [ref=e56]:
                - generic [ref=e57]: ABSLI Digishield Plan | INDIAN BANK LIMITED (IB)
                - generic [ref=e59]:
                  - generic [ref=e60]: Documents
                  - generic [ref=e61]: "|"
                  - generic [ref=e62]: Pending
                  - img [ref=e63]
                  - button "refresh" [ref=e64]:
                    - img [ref=e66]
            - generic [ref=e68]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e70] [cursor=pointer]:
            - generic [ref=e71]:
              - generic [ref=e72]: LA53544113 | mr. utpal mal utpal
              - generic [ref=e73]:
                - generic [ref=e74]: ABSLI Digishield Plan | DCB BANK LTD
                - generic [ref=e76]:
                  - generic [ref=e77]: Select Plan
                  - generic [ref=e78]: "|"
                  - generic [ref=e79]: Pending
                  - img [ref=e80]
                  - button "refresh" [ref=e81]:
                    - img [ref=e83]
            - generic [ref=e85]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e87] [cursor=pointer]:
            - generic [ref=e88]:
              - generic [ref=e89]: LA53543543 | mr. utpal mal utpal
              - generic [ref=e90]:
                - generic [ref=e91]: ABSLI Super Term Plan | DEUTSCHE BANK AG (DB)
                - generic [ref=e92]:
                  - generic [ref=e93]:
                    - generic [ref=e94]: Application Status
                    - generic [ref=e95]: "|"
                    - generic [ref=e96]: Completed
                    - img [ref=e97]
                    - button "refresh" [ref=e98]:
                      - img [ref=e100]
                  - generic [ref=e102]:
                    - text: Track
                    - button "refresh" [ref=e103]:
                      - img [ref=e105]
            - button "refresh" [ref=e108]:
              - img [ref=e110]
          - generic [ref=e113] [cursor=pointer]:
            - generic [ref=e114]:
              - generic [ref=e115]: LA53543575 | messer jkfgkfk
              - generic [ref=e116]:
                - generic [ref=e117]: ABSLI Super Term Plan | EQUITAS SMALL FINANCE BANK
                - generic [ref=e119]:
                  - generic [ref=e120]: Payment
                  - generic [ref=e121]: "|"
                  - generic [ref=e122]: Completed
                  - img [ref=e123]
                  - button "refresh" [ref=e124]:
                    - img [ref=e126]
            - generic [ref=e128]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e130] [cursor=pointer]:
            - generic [ref=e131]:
              - generic [ref=e132]: LA53543931 | master app tracker testing
              - generic [ref=e133]:
                - generic [ref=e134]: ABSLI Index Guaranteed Annuity Plus | THE KARUR VYSYA BANK LIMITED (KVB)
                - generic [ref=e136]:
                  - generic [ref=e137]: Select Plan
                  - generic [ref=e138]: "|"
                  - generic [ref=e139]: Pending
                  - img [ref=e140]
                  - button "refresh" [ref=e141]:
                    - img [ref=e143]
            - generic [ref=e145]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e147] [cursor=pointer]:
            - generic [ref=e148]:
              - generic [ref=e149]: LA53543887 | ms. harshada
              - generic [ref=e152]:
                - generic [ref=e153]: Select Plan
                - generic [ref=e154]: "|"
                - generic [ref=e155]: Pending
                - img [ref=e156]
                - button "refresh" [ref=e157]:
                  - img [ref=e159]
            - generic [ref=e161]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e163] [cursor=pointer]:
            - generic [ref=e164]:
              - generic [ref=e165]: LA53543835 | ms. harsha s j
              - generic [ref=e166]:
                - generic [ref=e167]: BSLI Wealth Secure Plan | UJJIVAN SMALL FINANCE BANK LIMITED (USFB)
                - generic [ref=e168]:
                  - generic [ref=e169]:
                    - generic [ref=e170]: Policy Status
                    - generic [ref=e171]: "|"
                    - generic [ref=e172]: Pending
                    - img [ref=e173]
                    - button "refresh" [ref=e174]:
                      - img [ref=e176]
                  - generic [ref=e178]:
                    - text: Track
                    - button "refresh" [ref=e179]:
                      - img [ref=e181]
            - button "refresh" [ref=e184]:
              - img [ref=e186]
          - generic [ref=e189] [cursor=pointer]:
            - generic [ref=e190]:
              - generic [ref=e191]: LA53543537 | mrs. samm jamm
              - generic [ref=e192]:
                - generic [ref=e193]: ABSLI Assured Savings Plan | EQUITAS SMALL FINANCE BANK
                - generic [ref=e194]:
                  - generic [ref=e195]:
                    - generic [ref=e196]: Policy Status
                    - generic [ref=e197]: "|"
                    - generic [ref=e198]: Pending
                    - img [ref=e199]
                    - button "refresh" [ref=e200]:
                      - img [ref=e202]
                  - generic [ref=e204]:
                    - text: Track
                    - button "refresh" [ref=e205]:
                      - img [ref=e207]
            - button "refresh" [ref=e210]:
              - img [ref=e212]
          - generic [ref=e215] [cursor=pointer]:
            - generic [ref=e216]:
              - generic [ref=e217]: LA53543818 | ms. harsha j
              - generic [ref=e218]:
                - generic [ref=e219]: BSLI Wealth Max Plan | THE KARUR VYSYA BANK LIMITED (KVB)
                - generic [ref=e220]:
                  - generic [ref=e221]:
                    - generic [ref=e222]: Policy Status
                    - generic [ref=e223]: "|"
                    - generic [ref=e224]: Pending
                    - img [ref=e225]
                    - button "refresh" [ref=e226]:
                      - img [ref=e228]
                  - generic [ref=e230]:
                    - text: Track
                    - button "refresh" [ref=e231]:
                      - img [ref=e233]
            - button "refresh" [ref=e236]:
              - img [ref=e238]
          - generic [ref=e241] [cursor=pointer]:
            - generic [ref=e242]:
              - generic [ref=e243]: LA53542654 | mr. sachin test
              - generic [ref=e244]:
                - generic [ref=e245]: ABSLI Assured Savings Plan | UJJIVAN SMALL FINANCE BANK LIMITED (USFB)
                - generic [ref=e246]:
                  - generic [ref=e247]:
                    - generic [ref=e248]: Application Status
                    - generic [ref=e249]: "|"
                    - generic [ref=e250]: Completed
                    - img [ref=e251]
                    - button "refresh" [ref=e252]:
                      - img [ref=e254]
                  - generic [ref=e256]:
                    - text: Track
                    - button "refresh" [ref=e257]:
                      - img [ref=e259]
            - button "refresh" [ref=e262]:
              - img [ref=e264]
          - generic [ref=e267] [cursor=pointer]:
            - generic [ref=e268]:
              - generic [ref=e269]: LA53544026 | ms. xdrgxdg xdrgxg
              - generic [ref=e272]:
                - generic [ref=e273]: Select Plan
                - generic [ref=e274]: "|"
                - generic [ref=e275]: Pending
                - img [ref=e276]
                - button "refresh" [ref=e277]:
                  - img [ref=e279]
            - generic [ref=e281]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e283] [cursor=pointer]:
            - generic [ref=e284]:
              - generic [ref=e285]: LA53543930 | mrs. apoorv gaurav
              - generic [ref=e288]:
                - generic [ref=e289]: Select Plan
                - generic [ref=e290]: "|"
                - generic [ref=e291]: Pending
                - img [ref=e292]
                - button "refresh" [ref=e293]:
                  - img [ref=e295]
            - generic [ref=e297]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e299] [cursor=pointer]:
            - generic [ref=e300]:
              - generic [ref=e301]: LA53543832 | ms. harshada suhas jadhav
              - generic [ref=e304]:
                - generic [ref=e305]: Select Plan
                - generic [ref=e306]: "|"
                - generic [ref=e307]: Pending
                - img [ref=e308]
                - button "refresh" [ref=e309]:
                  - img [ref=e311]
            - generic [ref=e313]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e315] [cursor=pointer]:
            - generic [ref=e316]:
              - generic [ref=e317]: LA53543787 | messer knjjkhjkhkjhk
              - generic [ref=e320]:
                - generic [ref=e321]: Select Plan
                - generic [ref=e322]: "|"
                - generic [ref=e323]: Pending
                - img [ref=e324]
                - button "refresh" [ref=e325]:
                  - img [ref=e327]
            - generic [ref=e329]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e331] [cursor=pointer]:
            - generic [ref=e332]:
              - generic [ref=e333]: LA53543741 | dr. priyanka j
              - generic [ref=e336]:
                - generic [ref=e337]: Select Plan
                - generic [ref=e338]: "|"
                - generic [ref=e339]: Pending
                - img [ref=e340]
                - button "refresh" [ref=e341]:
                  - img [ref=e343]
            - generic [ref=e345]:
              - button "refresh" [disabled]:
                - generic:
                  - img
        - button "add" [ref=e347] [cursor=pointer]:
          - generic [ref=e349]:
            - img [ref=e350]
            - generic [ref=e352]: NEW APPLICATION
```

# Test source

```ts
  1   | import { test, expect, Page } from '@playwright/test';
  2   | import * as dotenv from 'dotenv';
  3   | import * as path from 'path';
  4   | import * as fs from 'fs';
  5   | import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
  6   | import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
  7   | import { AdityaBirlaLocators } from '../../locators/aditya_birla_locators';
  8   | import { FilterSearchBar } from '../../components/filter_search_bar';
  9   | import { PolicyListTable } from '../../components/policy_list_table';
  10  | import { PaginationFooter } from '../../components/pagination_footer';
  11  | import { DetailDrawer } from '../../components/detail_drawer';
  12  | import { TopNavigationControls } from '../../components/top_navigation_controls';
  13  | 
  14  | defaultPaths();
  15  | 
  16  | test('app tracker regression flow', async ({ page }) => {
  17  |   const username = process.env.ADITYA_BIRLA_USER || '';
  18  |   const password = process.env.ADITYA_BIRLA_PASS || '';
  19  | 
  20  |   expect(username, 'ADITYA_BIRLA_USER must be provided').not.toBe('');
  21  |   expect(password, 'ADITYA_BIRLA_PASS must be provided').not.toBe('');
  22  | 
  23  |   const loginPage = new AdityaBirlaLoginPage(page);
  24  |   const trackerPage = new AdityaBirlaTrackerPage(page);
  25  |   const locators = new AdityaBirlaLocators(page);
  26  | 
  27  |   // Initialize Components
  28  |   const searchBar = new FilterSearchBar(page);
  29  |   const policyTable = new PolicyListTable(page);
  30  |   const pagination = new PaginationFooter(page);
  31  |   const details = new DetailDrawer(page);
  32  |   const topNav = new TopNavigationControls(page);
  33  | 
  34  |   await loginPage.load();
  35  |   await loginPage.enterCredentials(username, password);
  36  |   await loginPage.clickLoginButton();
  37  | 
  38  |   await page.waitForURL('**/dashboard', { timeout: 15000 });
  39  |   expect(page.url()).toContain('/dashboard');
  40  | 
  41  |   const menuBtn = locators.menuButton.first();
  42  |   await menuBtn.scrollIntoViewIfNeeded();
  43  |   await menuBtn.waitFor({ state: 'visible', timeout: 5000 });
  44  |   await menuBtn.click();
  45  | 
  46  |   await page.waitForTimeout(500);
  47  | 
  48  |   const trackerMenuItem = locators.applicationTrackerItem.first();
  49  |   await trackerMenuItem.waitFor({ state: 'visible', timeout: 5000 });
  50  |   await trackerMenuItem.click({ force: true });
  51  | 
  52  |   await page.waitForTimeout(2000);
  53  |   const pages = page.context().pages();
  54  |   const trackerPageObj = pages.find((p) => p.url().includes('app-tracker')) || page;
  55  |   
  56  |   // Update components to use the new page object if a new tab was opened
  57  |   const effectiveSearchBar = trackerPageObj !== page ? new FilterSearchBar(trackerPageObj) : searchBar;
  58  |   const effectiveTable = trackerPageObj !== page ? new PolicyListTable(trackerPageObj) : policyTable;
  59  |   const effectivePagination = trackerPageObj !== page ? new PaginationFooter(trackerPageObj) : pagination;
  60  | 
  61  |   await trackerPageObj.waitForLoadState('networkidle', { timeout: 10000 });
  62  |   
  63  |   // Component Validations
  64  |   console.log('Validating Search Bar...');
  65  |   const searchBarStatus = await effectiveSearchBar.validateAll();
  66  |   expect(searchBarStatus.searchBarVisible).toBeTruthy();
  67  | 
  68  |   console.log('Validating Policy Table...');
  69  |   const tableStatus = await effectiveTable.validateAll();
  70  |   expect(tableStatus.visible).toBeTruthy();
  71  |   expect(tableStatus.rowCount).toBeGreaterThan(0);
  72  | 
  73  |   console.log('Validating Pagination...');
  74  |   const paginationStatus = await effectivePagination.validateAll();
> 75  |   expect(paginationStatus.visible).toBeTruthy();
      |                                    ^ Error: expect(received).toBeTruthy()
  76  | 
  77  |   // Perform a search interaction
  78  |   if (tableStatus.rowCount > 0) {
  79  |     const firstAppNo = tableStatus.firstRow.app_no;
  80  |     console.log(`Searching for Application No: ${firstAppNo}`);
  81  |     await effectiveSearchBar.search(firstAppNo);
  82  |     await trackerPageObj.waitForTimeout(2000); // Wait for results to filter
  83  |     
  84  |     const filteredCount = await effectiveTable.getRowCount();
  85  |     console.log(`Filtered row count: ${filteredCount}`);
  86  |     expect(filteredCount).toBeGreaterThan(0);
  87  |   }
  88  | 
  89  |   const pageUrl = trackerPageObj.url();
  90  |   expect(pageUrl).toContain('app-tracker');
  91  | });
  92  | 
  93  | function defaultPaths() {
  94  |   const envPaths = [
  95  |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', '.env'),
  96  |     path.resolve(__dirname, '..', '..', '..', '.env'),
  97  |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', 'tests', '.env')
  98  |   ];
  99  | 
  100 |   for (const envPath of envPaths) {
  101 |     if (fs.existsSync(envPath)) {
  102 |       dotenv.config({ path: envPath });
  103 |       break;
  104 |     }
  105 |   }
  106 | }
  107 | 
```