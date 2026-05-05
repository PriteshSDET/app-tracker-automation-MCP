# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: regression\app_tracker_regression.spec.ts >> app tracker regression flow
- Location: tests\regression\app_tracker_regression.spec.ts:19:5

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.waitForTimeout: Test timeout of 30000ms exceeded.
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
              - generic [ref=e55]: LA53543887 | ms. harshada
              - generic [ref=e58]:
                - generic [ref=e59]: Select Plan
                - generic [ref=e60]: "|"
                - generic [ref=e61]: Pending
                - img [ref=e62]
                - button "refresh" [ref=e63]:
                  - img [ref=e65]
            - generic [ref=e67]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e69] [cursor=pointer]:
            - generic [ref=e70]:
              - generic [ref=e71]: LA53541792 | messer tgxzb
              - generic [ref=e72]:
                - generic [ref=e73]: ABSLI Digishield Plan | INDIAN BANK LIMITED (IB)
                - generic [ref=e75]:
                  - generic [ref=e76]: Documents
                  - generic [ref=e77]: "|"
                  - generic [ref=e78]: Pending
                  - img [ref=e79]
                  - button "refresh" [ref=e80]:
                    - img [ref=e82]
            - generic [ref=e84]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e86] [cursor=pointer]:
            - generic [ref=e87]:
              - generic [ref=e88]: LA53543931 | master app tracker testing
              - generic [ref=e89]:
                - generic [ref=e90]: ABSLI Index Guaranteed Annuity Plus | THE KARUR VYSYA BANK LIMITED (KVB)
                - generic [ref=e92]:
                  - generic [ref=e93]: Customer Profile
                  - generic [ref=e94]: "|"
                  - generic [ref=e95]: Pending
                  - img [ref=e96]
                  - button "refresh" [ref=e97]:
                    - img [ref=e99]
            - generic [ref=e101]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e103] [cursor=pointer]:
            - generic [ref=e104]:
              - generic [ref=e105]: LA53543575 | messer jkfgkfk
              - generic [ref=e106]:
                - generic [ref=e107]: ABSLI Super Term Plan | EQUITAS SMALL FINANCE BANK
                - generic [ref=e109]:
                  - generic [ref=e110]: Documents
                  - generic [ref=e111]: "|"
                  - generic [ref=e112]: Pending
                  - img [ref=e113]
                  - button "refresh" [ref=e114]:
                    - img [ref=e116]
            - generic [ref=e118]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e120] [cursor=pointer]:
            - generic [ref=e121]:
              - generic [ref=e122]: LA53544113 | mr. utpal mal utpal
              - generic [ref=e123]:
                - generic [ref=e124]: ABSLI Digishield Plan | DCB BANK LTD
                - generic [ref=e126]:
                  - generic [ref=e127]: Select Plan
                  - generic [ref=e128]: "|"
                  - generic [ref=e129]: Pending
                  - img [ref=e130]
                  - button "refresh" [ref=e131]:
                    - img [ref=e133]
            - generic [ref=e135]:
              - button "refresh" [disabled]:
                - generic:
                  - img
          - generic [ref=e137] [cursor=pointer]:
            - generic [ref=e138]:
              - generic [ref=e139]: LA53543543 | mr. utpal mal utpal
              - generic [ref=e140]:
                - generic [ref=e141]: ABSLI Super Term Plan | DEUTSCHE BANK AG (DB)
                - generic [ref=e142]:
                  - generic [ref=e143]:
                    - generic [ref=e144]: Application Status
                    - generic [ref=e145]: "|"
                    - generic [ref=e146]: Completed
                    - img [ref=e147]
                    - button "refresh" [ref=e148]:
                      - img [ref=e150]
                  - generic [ref=e152]:
                    - text: Track
                    - button "refresh" [ref=e153]:
                      - img [ref=e155]
            - button "refresh" [ref=e158]:
              - img [ref=e160]
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
  33  |   await page.waitForURL('**/dashboard', { timeout: 15000 });
  34  |   expect(page.url()).toContain('/dashboard');
  35  | 
  36  |   const menuBtn = locators.menuButton.first();
  37  |   await menuBtn.scrollIntoViewIfNeeded();
  38  |   await menuBtn.waitFor({ state: 'visible', timeout: 10000 });
  39  |   await menuBtn.click();
  40  | 
  41  |   await page.waitForTimeout(2000);
  42  | 
  43  |   const trackerMenuItem = locators.applicationTrackerItem.first();
  44  |   await trackerMenuItem.waitFor({ state: 'visible', timeout: 10000 });
  45  |   
  46  |   console.log('Clicking Tracker menu item...');
  47  |   const newPagePromise = page.context().waitForEvent('page', { timeout: 15000 }).catch(() => null);
  48  |   await trackerMenuItem.click({ force: true });
  49  |   const trackerPageObj = (await newPagePromise) || page;
  50  | 
  51  |   await trackerPageObj.waitForLoadState('networkidle', { timeout: 20000 });
  52  |   console.log(`Current Tracker URL: ${trackerPageObj.url()}`);
  53  |   
  54  |   const effectiveTopNav = new TopNavigationControls(trackerPageObj);
  55  |   const effectiveFilterChips = new ActiveFilterChips(trackerPageObj);
  56  |   const effectiveSearchBar = new FilterSearchBar(trackerPageObj);
  57  |   const effectivePagination = new PaginationFooter(trackerPageObj);
  58  |   const effectiveTable = new PolicyListTable(trackerPageObj);
  59  |   const effectiveDetails = new DetailDrawer(trackerPageObj);
  60  | 
  61  |   // 1. Top Navigation Interactions
  62  |   console.log('--- Top Navigation Interactions ---');
  63  |   await effectiveTopNav.toggleTheme();
  64  |   await trackerPageObj.waitForTimeout(1000);
  65  |   
  66  |   await effectiveTopNav.openAccountMenu();
  67  |   const initials = await effectiveTopNav.getUserInitials();
  68  |   console.log(`User initials found: ${initials}`);
  69  |   await effectiveTopNav.closeAccountMenu();
  70  | 
  71  |   // 2. Filter Chips Interactions
  72  |   console.log('--- Filter Chips Interactions ---');
  73  |   await effectiveFilterChips.validateChipsVisible();
  74  |   
  75  |   console.log('Opening filter dropdown...');
  76  |   const opened = await effectiveFilterChips.openDropdown();
  77  |   if (opened) {
  78  |     await trackerPageObj.waitForTimeout(2000);
  79  |     const availableStatuses = await effectiveFilterChips.getAvailableStatuses();
  80  |     console.log(`Available statuses: ${availableStatuses}`);
  81  |     
  82  |     if (availableStatuses.length > 0) {
  83  |       const statusToSelect = availableStatuses.find(s => s !== 'All' && s !== 'Others') || availableStatuses[0];
  84  |       
  85  |       console.log('Clearing all filters...');
  86  |       await effectiveFilterChips.clearAll();
  87  |       await trackerPageObj.waitForTimeout(2000);
  88  |       
  89  |       console.log(`Selecting "${statusToSelect}" status...`);
  90  |       await effectiveFilterChips.selectStatus(statusToSelect);
  91  |       await trackerPageObj.waitForTimeout(4000);
  92  |       
  93  |       const currentChips = await effectiveFilterChips.getActiveChipNames();
  94  |       console.log(`Active chips after selection: ${currentChips}`);
  95  |       
  96  |       const isMatched = currentChips.some(c => 
  97  |         c.toLowerCase().includes(statusToSelect.toLowerCase()) || 
  98  |         statusToSelect.toLowerCase().includes(c.toLowerCase())
  99  |       );
  100 |       if (!isMatched) console.warn(`Selected status "${statusToSelect}" not found in active chips.`);
  101 |       
  102 |       console.log(`Verifying table status for row 0...`);
  103 |       const rowCount = await effectiveTable.getRowCount();
  104 |       if (rowCount > 0) {
  105 |         const firstRowStatus = await effectiveTable.getPolicyStatusBadge(0);
  106 |         console.log(`First row status: ${firstRowStatus}`);
  107 |       }
  108 |       
  109 |       console.log('Cleaning up filters...');
  110 |       await effectiveFilterChips.clearAll();
  111 |       await trackerPageObj.waitForTimeout(2000);
  112 |     }
  113 |   }
  114 | 
  115 |   // 3. Search Bar Validation
  116 |   console.log('--- Search Bar Validation ---');
  117 |   await effectiveSearchBar.validateAll();
  118 | 
  119 |   // 4. Pagination Validation
  120 |   console.log('--- Pagination Validation ---');
  121 |   await effectivePagination.validateAll();
  122 | 
  123 |   // 5. Policy Table Validation
  124 |   console.log('--- Policy Table Validation ---');
  125 |   const tableStatus = await effectiveTable.validateAll();
  126 |   expect(tableStatus.visible).toBeTruthy();
  127 | 
  128 |   // 6. Search Interaction Validation
  129 |   if (tableStatus.rowCount > 0) {
  130 |     const firstAppNo = tableStatus.firstRow.app_no;
  131 |     console.log(`Searching for App No: ${firstAppNo}`);
  132 |     await effectiveSearchBar.search(firstAppNo);
> 133 |     await trackerPageObj.waitForTimeout(3000);
      |                          ^ Error: page.waitForTimeout: Test timeout of 30000ms exceeded.
  134 |     const filteredCount = await effectiveTable.getRowCount();
  135 |     console.log(`Filtered count: ${filteredCount}`);
  136 |   }
  137 | 
  138 |   // 7. Detail Drawer Validation
  139 |   if (tableStatus.rowCount > 0) {
  140 |     console.log('--- Detail Drawer Validation ---');
  141 |     await effectiveTable.clickRow(0);
  142 |     await effectiveDetails.waitUntilOpen();
  143 |     const drawerStatus = await effectiveDetails.validateAll();
  144 |     console.log(`Drawer header: ${drawerStatus.headerName}`);
  145 |     await effectiveDetails.close();
  146 |   }
  147 | 
  148 |   expect(trackerPageObj.url()).toContain('app-tracker');
  149 | });
  150 | 
  151 | function defaultPaths() {
  152 |   const envPaths = [
  153 |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', '.env'),
  154 |     path.resolve(__dirname, '..', '..', '..', '.env'),
  155 |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', 'tests', '.env')
  156 |   ];
  157 | 
  158 |   for (const envPath of envPaths) {
  159 |     if (fs.existsSync(envPath)) {
  160 |       dotenv.config({ path: envPath });
  161 |       break;
  162 |     }
  163 |   }
  164 | }
  165 | 
```