import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Policy List Table Component Utility
 * =====================================
 */
export class PolicyListTable {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Selectors ---
    static readonly TABLE_WRAPPER = "div.overflow-auto";
    static readonly TABLE = "div.overflow-auto table.w-full";
    static readonly THEAD = "div.overflow-auto table thead";
    static readonly TBODY = "div.overflow-auto table tbody";
    static readonly HEADER_CELLS = "div.overflow-auto table thead th";
    static readonly BODY_ROWS = "div.overflow-auto table tbody tr";

    // Column indices (1-based for CSS :nth-child)
    static readonly COL_APP_NO = 1;
    static readonly COL_PROPOSER = 2;
    static readonly COL_PLAN = 3;
    static readonly COL_APP_DATE = 4;
    static readonly COL_PREMIUM = 5;
    static readonly COL_POLICY_NO = 6;
    static readonly COL_STATUS = 7;
    static readonly COL_RA_DATE = 8;

    static readonly STATUS_BADGE_SEL = "span.inline-flex.items-center.rounded.font-medium";

    constructor(page: Page, timeout: number = 15000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    // ------------------------------------------------------------------ #
    //  Private helpers
    // ------------------------------------------------------------------ #

    private _table(): Locator {
        return this.page.locator(PolicyListTable.TABLE).first();
    }

    private async _rows(): Promise<Locator[]> {
        return await this.page.locator(PolicyListTable.BODY_ROWS).all();
    }

    private _row(index: number): Locator {
        return this.page.locator(PolicyListTable.BODY_ROWS).nth(index);
    }

    private async _cellText(row: Locator, colIndex: number): Promise<string> {
        try {
            const cell = row.locator(`td:nth-child(${colIndex})`).first();
            const span = cell.locator("span").first();
            return (await span.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            return "";
        }
    }

    // ------------------------------------------------------------------ #
    //  Visibility Checks
    // ------------------------------------------------------------------ #

    async isVisible(): Promise<boolean> {
        try {
            return await this._table().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async validateVisible(): Promise<boolean> {
        try {
            const wrapper = this.page.locator(PolicyListTable.TABLE_WRAPPER).first();
            await wrapper.waitFor({ state: "attached", timeout: this.timeout });
            await wrapper.waitFor({ state: "visible", timeout: this.timeout });
            const table = this._table();
            await table.waitFor({ state: "visible", timeout: this.timeout });
            this.logger.info("[OK] Policy List Table is visible");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Policy List Table not visible: ${e}`);
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Read Headers
    // ------------------------------------------------------------------ #

    async getHeaders(): Promise<string[]> {
        const headers: string[] = [];
        try {
            const cells = await this.page.locator(PolicyListTable.HEADER_CELLS).all();
            for (const cell of cells) {
                const span = cell.locator("span.inline-flex").first();
                let txt = "";
                try {
                    txt = await span.textContent({ timeout: 1000 }) || "";
                } catch (e) {
                    txt = await cell.textContent({ timeout: 1000 }) || "";
                }
                txt = txt.trim();
                if (txt) {
                    headers.push(txt);
                }
            }
            this.logger.info(`[OK] Table headers: ${headers}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read table headers: ${e}`);
        }
        return headers;
    }

    async validateHeaders(): Promise<boolean> {
        const expected = [
            "App. No.", "Proposer Name", "Plan Name", "App. Recv. On",
            "Modal Premium", "Policy No.", "Policy Status", "R&A Date"
        ];
        const headers = await this.getHeaders();
        const missing = expected.filter(h => !headers.some(hdr => hdr.includes(h)));
        if (missing.length > 0) {
            this.logger.warning(`[WARN] Missing expected columns: ${missing}`);
            return false;
        }
        this.logger.info("[OK] All expected columns present");
        return true;
    }

    // ------------------------------------------------------------------ #
    //  Read Rows
    // ------------------------------------------------------------------ #

    async getRowCount(): Promise<number> {
        try {
            const rows = await this._rows();
            const count = rows.length;
            this.logger.info(`[OK] Table row count: ${count}`);
            return count;
        } catch (e) {
            this.logger.warning(`[WARN] Could not count rows: ${e}`);
            return 0;
        }
    }

    async getRowData(index: number): Promise<any> {
        const data: any = {};
        try {
            const row = this._row(index);
            await row.waitFor({ state: "attached", timeout: this.timeout });
            data["app_no"] = await this._cellText(row, PolicyListTable.COL_APP_NO);
            data["proposer_name"] = await this._cellText(row, PolicyListTable.COL_PROPOSER);
            data["plan_name"] = await this._cellText(row, PolicyListTable.COL_PLAN);
            data["app_recv_on"] = await this._cellText(row, PolicyListTable.COL_APP_DATE);
            data["modal_premium"] = await this._cellText(row, PolicyListTable.COL_PREMIUM);
            data["policy_no"] = await this._cellText(row, PolicyListTable.COL_POLICY_NO);
            data["policy_status"] = await this.getPolicyStatusBadge(index);
            data["ra_date"] = await this._cellText(row, PolicyListTable.COL_RA_DATE);
            this.logger.info(`[OK] Row ${index} data: ${JSON.stringify(data)}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read row ${index} data: ${e}`);
        }
        return data;
    }

    async getAllRowsData(): Promise<any[]> {
        const allData: any[] = [];
        const count = await this.getRowCount();
        for (let i = 0; i < count; i++) {
            allData.push(await this.getRowData(i));
        }
        return allData;
    }

    async getPolicyStatusBadge(rowIndex: number): Promise<string> {
        try {
            const row = this._row(rowIndex);
            const statusCell = row.locator(`td:nth-child(${PolicyListTable.COL_STATUS})`).first();
            const badge = statusCell.locator(PolicyListTable.STATUS_BADGE_SEL).first();
            const txt = await badge.textContent({ timeout: 2000 }) || "";
            return txt.trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read status badge for row ${rowIndex}: ${e}`);
            return "";
        }
    }

    async getColumnValues(colIndex: number): Promise<string[]> {
        const values: string[] = [];
        try {
            const rows = await this._rows();
            for (const row of rows) {
                values.push(await this._cellText(row, colIndex));
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not read column ${colIndex}: ${e}`);
        }
        return values;
    }

    // ------------------------------------------------------------------ #
    //  Find / Search Rows
    // ------------------------------------------------------------------ #

    async findRowByAppNo(appNo: string): Promise<Locator | null> {
        try {
            const row = this.page.locator(
                `div.overflow-auto table tbody tr:has(span:text-is('${appNo}'))`
            ).first();
            if (await row.isVisible({ timeout: 3000 })) {
                this.logger.info(`[OK] Found row for App No: ${appNo}`);
                return row;
            }
        } catch (e) {}
        this.logger.warning(`[WARN] Row not found for App No: ${appNo}`);
        return null;
    }

    async findRowsByStatus(status: string): Promise<Locator[]> {
        const matched: Locator[] = [];
        try {
            const rows = await this._rows();
            for (const row of rows) {
                try {
                    const badge = row.locator(
                        `td:nth-child(${PolicyListTable.COL_STATUS}) ${PolicyListTable.STATUS_BADGE_SEL}`
                    ).first();
                    const txt = await badge.textContent({ timeout: 1000 }) || "";
                    if (txt.toLowerCase().includes(status.toLowerCase())) {
                        matched.push(row);
                    }
                } catch (e) {
                    continue;
                }
            }
            this.logger.info(`[OK] Found ${matched.length} rows with status '${status}'`);
        } catch (e) {
            this.logger.warning(`[WARN] Error finding rows by status: ${e}`);
        }
        return matched;
    }

    // ------------------------------------------------------------------ #
    //  Interactions
    // ------------------------------------------------------------------ #

    async clickRow(index: number): Promise<boolean> {
        try {
            const row = this._row(index);
            await row.waitFor({ state: "visible", timeout: this.timeout });
            await row.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Clicked row ${index}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click row ${index}: ${e}`);
            return false;
        }
    }

    async clickRowByAppNo(appNo: string): Promise<boolean> {
        const row = await this.findRowByAppNo(appNo);
        if (!row) {
            return false;
        }
        try {
            await row.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Clicked row for App No: ${appNo}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click row for App No '${appNo}': ${e}`);
            return false;
        }
    }

    async sortByColumn(columnHeader: string): Promise<boolean> {
        try {
            const header = this.page.locator(
                `div.overflow-auto thead th:has(span:has-text('${columnHeader}'))`
            ).first();
            await header.waitFor({ state: "visible", timeout: this.timeout });
            await header.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Sorted by column: ${columnHeader}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not sort by '${columnHeader}': ${e}`);
            return false;
        }
    }

    async getActiveSortColumn(): Promise<string | null> {
        try {
            const sortedTh = this.page.locator(
                "div.overflow-auto thead th[aria-sort]"
            ).first();
            if (await sortedTh.isVisible({ timeout: 3000 })) {
                const txt = await sortedTh.locator("span.inline-flex").first().textContent({ timeout: 2000 }) || "";
                const sortDir = await sortedTh.getAttribute("aria-sort", { timeout: 1000 });
                this.logger.info(`[OK] Active sort: '${txt.trim()}' (${sortDir})`);
                return txt.trim();
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not determine active sort column: ${e}`);
        }
        return null;
    }

    async getActiveSortDirection(): Promise<string | null> {
        try {
            const sortedTh = this.page.locator("div.overflow-auto thead th[aria-sort]").first();
            return await sortedTh.getAttribute("aria-sort", { timeout: 3000 });
        } catch (e) {
            return null;
        }
    }

    // ------------------------------------------------------------------ #
    //  Composite Validation
    // ------------------------------------------------------------------ #

    async validateAll(): Promise<any> {
        const result: any = {
            visible: false,
            headersValid: false,
            rowCount: 0,
            firstRow: {},
            activeSortColumn: null,
            sortDirection: null,
        };

        try {
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
        } catch (e) {}

        result.visible = await this.validateVisible();
        if (!result.visible) return result;

        result.headersValid = await this.validateHeaders();
        result.rowCount = await this.getRowCount();
        result.activeSortColumn = await this.getActiveSortColumn();
        result.sortDirection = await this.getActiveSortDirection();

        if (result.rowCount > 0) {
            result.firstRow = await this.getRowData(0);
        }

        this.logger.info(`[PolicyListTable] Validation result: ${JSON.stringify(result)}`);
        return result;
    }
}
