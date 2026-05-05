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
Error: expect(received).toContain(expected) // indexOf

Expected substring: "app"
Received string:    ""
```

# Test source

```ts
  20  |   const username = process.env.ADITYA_BIRLA_USER || '';
  21  |   const password = process.env.ADITYA_BIRLA_PASS || '';
  22  | 
  23  |   expect(username, 'ADITYA_BIRLA_USER must be provided').not.toBe('');
  24  |   expect(password, 'ADITYA_BIRLA_PASS must be provided').not.toBe('');
  25  | 
  26  |   const loginPage = new AdityaBirlaLoginPage(page);
  27  |   const locators = new AdityaBirlaLocators(page);
  28  | 
  29  |   await loginPage.load();
  30  |   await loginPage.enterCredentials(username, password);
  31  |   await loginPage.clickLoginButton();
  32  | 
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
  47  |   // Handle potential new tab or same page navigation
  48  |   const newPagePromise = page.context().waitForEvent('page', { timeout: 10000 }).catch(() => null);
  49  |   await trackerMenuItem.click({ force: true });
  50  |   
  51  |   const newPage = await newPagePromise;
  52  |   const trackerPageObj = newPage || page;
  53  | 
  54  |   await trackerPageObj.waitForLoadState('networkidle', { timeout: 20000 });
  55  |   console.log(`Current Tracker URL: ${trackerPageObj.url()}`);
  56  |   
  57  |   // Initialize Components
  58  |   const effectiveTopNav = new TopNavigationControls(trackerPageObj);
  59  |   const effectiveFilterChips = new ActiveFilterChips(trackerPageObj);
  60  |   const effectiveSearchBar = new FilterSearchBar(trackerPageObj);
  61  |   const effectivePagination = new PaginationFooter(trackerPageObj);
  62  |   const effectiveTable = new PolicyListTable(trackerPageObj);
  63  |   const effectiveDetails = new DetailDrawer(trackerPageObj);
  64  | 
  65  |   // 1. Top Navigation Interactions
  66  |   console.log('--- Top Navigation Interactions ---');
  67  |   try {
  68  |     console.log('Toggling theme...');
  69  |     await effectiveTopNav.toggleTheme();
  70  |     await trackerPageObj.waitForTimeout(1000);
  71  |     
  72  |     console.log('Opening account menu...');
  73  |     await effectiveTopNav.openAccountMenu();
  74  |     const initials = await effectiveTopNav.getUserInitials();
  75  |     console.log(`User initials found: ${initials}`);
  76  |     expect(initials).toBeTruthy();
  77  |     await effectiveTopNav.closeAccountMenu();
  78  |   } catch (e) {
  79  |     console.warn(`Top Navigation Interaction warning: ${e.message}`);
  80  |   }
  81  | 
  82  |   // 2. Filter Chips Interactions
  83  |   console.log('--- Filter Chips Interactions ---');
  84  |   await effectiveFilterChips.validateChipsVisible();
  85  |   
  86  |   console.log('Opening filter dropdown...');
  87  |   await effectiveFilterChips.openDropdown();
  88  |   await trackerPageObj.waitForTimeout(2000);
  89  |   
  90  |   const availableStatuses = await effectiveFilterChips.getAvailableStatuses();
  91  |   console.log(`Available statuses: ${availableStatuses}`);
  92  |   
  93  |   if (availableStatuses.length > 0) {
  94  |     const statusToSelect = availableStatuses.find(s => s !== 'All' && s !== 'Others') || availableStatuses[0];
  95  |     
  96  |     console.log('Clearing all filters...');
  97  |     await effectiveFilterChips.clearAll();
  98  |     await trackerPageObj.waitForTimeout(3000);
  99  |     
  100 |     console.log(`Selecting "${statusToSelect}" status...`);
  101 |     await effectiveFilterChips.selectStatus(statusToSelect);
  102 |     await trackerPageObj.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
  103 |     await trackerPageObj.waitForTimeout(4000);
  104 |     
  105 |     const currentChips = await effectiveFilterChips.getActiveChipNames();
  106 |     console.log(`Active chips after selection: ${currentChips}`);
  107 |     
  108 |     const isMatched = currentChips.some(c => 
  109 |       c.toLowerCase().includes(statusToSelect.toLowerCase()) || 
  110 |       statusToSelect.toLowerCase().includes(c.toLowerCase())
  111 |     );
  112 |     expect(isMatched, `Selected status "${statusToSelect}" should be active`).toBeTruthy();
  113 |     
  114 |     console.log(`Verifying table reflects "${statusToSelect}" filter...`);
  115 |     const rowCount = await effectiveTable.getRowCount();
  116 |     if (rowCount > 0) {
  117 |       const firstRowStatus = await effectiveTable.getPolicyStatusBadge(0);
  118 |       console.log(`First row status: ${firstRowStatus}`);
  119 |       const statusWord = statusToSelect.split(' ')[0].toLowerCase();
> 120 |       expect(firstRowStatus.toLowerCase()).toContain(statusWord);
      |                                            ^ Error: expect(received).toContain(expected) // indexOf
  121 |     }
  122 |     
  123 |     console.log('Cleaning up filters...');
  124 |     await effectiveFilterChips.clearAll();
  125 |     await trackerPageObj.waitForTimeout(3000);
  126 |   }
  127 | 
  128 |   // 3. Search Bar Validation
  129 |   console.log('--- Search Bar Validation ---');
  130 |   await effectiveSearchBar.validateAll();
  131 | 
  132 |   // 4. Pagination Validation
  133 |   console.log('--- Pagination Validation ---');
  134 |   await effectivePagination.validateAll();
  135 | 
  136 |   // 5. Policy Table Validation
  137 |   console.log('--- Policy Table Validation ---');
  138 |   const tableStatus = await effectiveTable.validateAll();
  139 |   expect(tableStatus.visible).toBeTruthy();
  140 | 
  141 |   // 6. Search Interaction Validation
  142 |   if (tableStatus.rowCount > 0) {
  143 |     const firstAppNo = tableStatus.firstRow.app_no;
  144 |     console.log(`Searching for App No: ${firstAppNo}`);
  145 |     await effectiveSearchBar.search(firstAppNo);
  146 |     await trackerPageObj.waitForTimeout(3000);
  147 |     const filteredCount = await effectiveTable.getRowCount();
  148 |     expect(filteredCount).toBeGreaterThan(0);
  149 |   }
  150 | 
  151 |   // 7. Detail Drawer Validation
  152 |   if (tableStatus.rowCount > 0) {
  153 |     console.log('--- Detail Drawer Validation ---');
  154 |     await effectiveTable.clickRow(0);
  155 |     await effectiveDetails.waitUntilOpen();
  156 |     const drawerStatus = await effectiveDetails.validateAll();
  157 |     console.log(`Drawer header: ${drawerStatus.headerName}`);
  158 |     await effectiveDetails.close();
  159 |     expect(await effectiveDetails.isOpen()).toBeFalsy();
  160 |   }
  161 | 
  162 |   expect(trackerPageObj.url()).toContain('app-tracker');
  163 | });
  164 | 
  165 | function defaultPaths() {
  166 |   const envPaths = [
  167 |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', '.env'),
  168 |     path.resolve(__dirname, '..', '..', '..', '.env'),
  169 |     path.resolve(__dirname, '..', '..', '..', 'app-tracker-automation', 'tests', '.env')
  170 |   ];
  171 | 
  172 |   for (const envPath of envPaths) {
  173 |     if (fs.existsSync(envPath)) {
  174 |       dotenv.config({ path: envPath });
  175 |       break;
  176 |     }
  177 |   }
  178 | }
  179 | 
```