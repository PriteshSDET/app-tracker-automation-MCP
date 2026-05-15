# User Story 2: Unified Application Tracker Component Validation

## 📝 Story Description
**As an** Internal Sales Advisor (DSF/FLS) or Support Officer,
**I want** a unified, highly-functional Application Tracker dashboard,
**So that** I can efficiently manage my portfolio, perform granular searches, and track individual policy milestones without UI friction.

---

## ✅ Acceptance Criteria (AC)

### 1. Unified Navigation & Branding
- **AC 1.1**: The tracker must maintain a persistent header with "Aditya Birla Sun Life Insurance" branding.
- **AC 1.2**: Top-right navigation controls must include "Help", "Feedback", and "Logout" options.
- **AC 1.3**: The "MENU" button must be accessible at all times to allow cross-portal navigation.

### 2. Intelligent Search & Filtering
- **AC 2.1**: A search bar must allow filtering by **Application Number** or **Proposer Name** with sub-second response times.
- **AC 2.2**: Advanced filters (Date Range, Stage, Role) must trigger dynamic **Filter Chips** below the search bar.
- **AC 2.3**: Each filter chip must be removable via an 'X' icon, immediately updating the data grid.

### 3. Exhaustive Policy Data Grid
- **AC 3.1**: The "Policy List" table must display the following columns:
    - `App.No` (With link to journey)
    - `Proposer Name`
    - `Plan Name`
    - `Modal Premium` (With currency symbol ₹)
    - `Policy Status` (Color-coded: Pending, Issued, Rejected)
- **AC 3.2**: Sorting must be supported for "App.No" and "Modal Premium".

### 4. Granular Detail Drawer
- **AC 4.1**: Clicking any policy row must expand a side **Detail Drawer** or "Expanded View".
- **AC 4.2**: The drawer must show the vertical journey timeline (Lead -> Prospect -> R&A -> Medical -> Payment -> Issuance).
- **AC 4.3**: Each milestone must show a status (Completed, Pending, Skipped) with associated timestamps.

### 5. Pagination & State Management
- **AC 5.1**: The grid must support pagination at the footer (e.g., "1-10 of 250").
- **AC 5.2**: Navigation between pages must be smooth without full page reloads (SPA behavior).
- **AC 5.3**: Browser "Back" button should maintain the previous filter/search state.

---


