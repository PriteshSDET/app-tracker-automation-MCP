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
Error: expect(received).toBeTruthy()

Received: false
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - navigation "Application navigation" [ref=e4]:
    - generic [ref=e5]:
      - generic [ref=e6]:
        - img "ABSLI" [ref=e7]
        - generic [ref=e9]: App Tracker
      - generic [ref=e10]:
        - button "Toggle theme" [ref=e11] [cursor=pointer]:
          - img
        - button "Account menu" [active] [ref=e12] [cursor=pointer]:
          - img "AG" [ref=e13]:
            - generic [ref=e15]: AG
          - img [ref=e16]
  - main [ref=e18]:
    - generic [ref=e19]:
      - img [ref=e20]
      - paragraph [ref=e22]: Session Unavailable
      - paragraph [ref=e23]: Session token is unavailable. Please re-launch the application.
  - region "Notifications alt+T"
```

# Test source

```ts
  40  |   await menuBtn.click();
  41  | 
  42  |   await page.waitForTimeout(2000);
  43  | 
  44  |   const trackerMenuItem = locators.applicationTrackerItem.first();
  45  |   await trackerMenuItem.waitFor({ state: 'visible', timeout: 10000 });
  46  |   
  47  |   console.log('Navigating to Application Tracker...');
  48  |   // Attempt to handle both new tab and same-page navigation scenarios
  49  |   const pagePromise = page.context().waitForEvent('page', { timeout: 10000 }).catch(() => null);
  50  |   await trackerMenuItem.click({ force: true });
  51  |   
  52  |   const newPage = await pagePromise;
  53  |   let trackerPageObj = newPage || page;
  54  | 
  55  |   // If we are still on dashboard, something went wrong with the click
  56  |   if (trackerPageObj.url().includes('dashboard')) {
  57  |     console.log('Redirection check: Still on dashboard, retrying navigation...');
  58  |     await trackerMenuItem.click({ force: true });
  59  |     await trackerPageObj.waitForTimeout(3000);
  60  |     // If still on dashboard, try direct navigation as a fallback
  61  |     if (trackerPageObj.url().includes('dashboard')) {
  62  |         console.log('Direct navigation fallback...');
  63  |         await trackerPageObj.goto('https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications', { waitUntil: 'networkidle' });
  64  |     }
  65  |   }
  66  | 
  67  |   await trackerPageObj.waitForLoadState('networkidle', { timeout: 20000 });
  68  |   console.log(`Current Tracker URL: ${trackerPageObj.url()}`);
  69  |   
  70  |   const effectiveTopNav = new TopNavigationControls(trackerPageObj);
  71  |   const effectiveFilterChips = new ActiveFilterChips(trackerPageObj);
  72  |   const effectiveSearchBar = new FilterSearchBar(trackerPageObj);
  73  |   const effectivePagination = new PaginationFooter(trackerPageObj);
  74  |   const effectiveTable = new PolicyListTable(trackerPageObj);
  75  |   const effectiveDetails = new DetailDrawer(trackerPageObj);
  76  | 
  77  |   // 1. Top Navigation Interactions
  78  |   console.log('--- Top Navigation Interactions ---');
  79  |   await effectiveTopNav.toggleTheme();
  80  |   await trackerPageObj.waitForTimeout(1000);
  81  |   
  82  |   await effectiveTopNav.openAccountMenu();
  83  |   const initials = await effectiveTopNav.getUserInitials();
  84  |   console.log(`User initials found: ${initials}`);
  85  |   await effectiveTopNav.closeAccountMenu();
  86  | 
  87  |   // 2. Filter Chips Interactions
  88  |   console.log('--- Filter Chips Interactions ---');
  89  |   await effectiveFilterChips.validateChipsVisible();
  90  |   
  91  |   console.log('Opening filter dropdown...');
  92  |   const opened = await effectiveFilterChips.openDropdown();
  93  |   if (opened) {
  94  |     await trackerPageObj.waitForTimeout(2000);
  95  |     const availableStatuses = await effectiveFilterChips.getAvailableStatuses();
  96  |     console.log(`Available statuses: ${availableStatuses}`);
  97  |     
  98  |     if (availableStatuses.length > 0) {
  99  |       const statusToSelect = availableStatuses.find(s => s !== 'All' && s !== 'Others') || availableStatuses[0];
  100 |       
  101 |       console.log('Clearing all filters...');
  102 |       await effectiveFilterChips.clearAll();
  103 |       await trackerPageObj.waitForTimeout(2000);
  104 |       
  105 |       console.log(`Selecting "${statusToSelect}" status...`);
  106 |       await effectiveFilterChips.selectStatus(statusToSelect);
  107 |       await trackerPageObj.waitForTimeout(4000);
  108 |       
  109 |       const currentChips = await effectiveFilterChips.getActiveChipNames();
  110 |       console.log(`Active chips after selection: ${currentChips}`);
  111 |       
  112 |       console.log(`Verifying table status for row 0...`);
  113 |       const rowCount = await effectiveTable.getRowCount();
  114 |       if (rowCount > 0) {
  115 |         const firstRowStatus = await effectiveTable.getPolicyStatusBadge(0);
  116 |         console.log(`First row status: ${firstRowStatus}`);
  117 |       }
  118 |       
  119 |       console.log('Cleaning up filters...');
  120 |       await effectiveFilterChips.clearAll();
  121 |       await trackerPageObj.waitForTimeout(2000);
  122 |     }
  123 |     // Explicitly close the filter dropdown to ensure smooth flow
  124 |     await effectiveFilterChips.closeDropdown();
  125 |   }
  126 | 
  127 |   // 3. Search Bar Validation
  128 |   console.log('--- Search Bar Validation ---');
  129 |   await effectiveSearchBar.validateAll();
  130 |   // Ensure date filter or other popovers are closed
  131 |   await effectiveSearchBar.closeDateFilter();
  132 | 
  133 |   // 4. Pagination Validation
  134 |   console.log('--- Pagination Validation ---');
  135 |   await effectivePagination.validateAll();
  136 | 
  137 |   // 5. Policy Table Validation
  138 |   console.log('--- Policy Table Validation ---');
  139 |   const tableStatus = await effectiveTable.validateAll();
> 140 |   expect(tableStatus.visible).toBeTruthy();
      |                               ^ Error: expect(received).toBeTruthy()
  141 | 
  142 |   // 6. Search Interaction Validation
  143 |   if (tableStatus.rowCount > 0) {
  144 |     const firstAppNo = tableStatus.firstRow.app_no;
  145 |     console.log(`Searching for App No: ${firstAppNo}`);
  146 |     await effectiveSearchBar.search(firstAppNo);
  147 |     await trackerPageObj.waitForTimeout(3000);
  148 |     const filteredCount = await effectiveTable.getRowCount();
  149 |     console.log(`Filtered count: ${filteredCount}`);
  150 |   }
  151 | 
  152 |   // 7. Detail Drawer Validation
  153 |   if (tableStatus.rowCount > 0) {
  154 |     console.log('--- Detail Drawer Validation ---');
  155 |     await effectiveTable.clickRow(0);
  156 |     await effectiveDetails.waitUntilOpen();
  157 |     const drawerStatus = await effectiveDetails.validateAll();
  158 |     console.log(`Drawer header: ${drawerStatus.headerName}`);
  159 |     await effectiveDetails.close();
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