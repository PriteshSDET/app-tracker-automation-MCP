import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Pagination Footer Component Utility
 * =====================================
 */
export class PaginationFooter {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Selectors ---
    static readonly NAV_CONTAINER = "nav[role='navigation'][aria-label='Pagination']";
    static readonly PREV_BTN = "button[aria-label='Previous page']";
    static readonly NEXT_BTN = "button[aria-label='Next page']";
    static readonly ACTIVE_PAGE = "button[aria-current='page']";
    static readonly PAGE_NUM_LIST = "ul.hidden.sm\\:flex";
    static readonly MOBILE_COUNTER = "span.sm\\:hidden";

    constructor(page: Page, timeout: number = 10000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    // ------------------------------------------------------------------ #
    //  Private helpers
    // ------------------------------------------------------------------ #

    private _nav(): Locator {
        return this.page.locator(PaginationFooter.NAV_CONTAINER).first();
    }

    private _pageBtn(pageNum: number): Locator {
        return this.page.locator(`button[aria-label='Page ${pageNum}']`).first();
    }

    private _parsePageOfText(text: string): [number | null, number | null] {
        const match = text.match(/Page\s+(\d+)\s+of\s+(\d+)/i);
        if (match) {
            return [parseInt(match[1]), parseInt(match[2])];
        }
        return [null, null];
    }

    // ------------------------------------------------------------------ #
    //  Visibility Checks
    // ------------------------------------------------------------------ #

    async isVisible(): Promise<boolean> {
        try {
            return await this._nav().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async validateVisible(): Promise<boolean> {
        try {
            const nav = this._nav();
            await nav.waitFor({ state: "attached", timeout: this.timeout });
            await nav.waitFor({ state: "visible", timeout: this.timeout });
            this.logger.info("[OK] Pagination footer is visible");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Pagination footer not visible: ${e}`);
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Read State
    // ------------------------------------------------------------------ #

    async getCurrentPage(): Promise<number | null> {
        try {
            const active = this.page.locator(PaginationFooter.ACTIVE_PAGE).first();
            await active.waitFor({ state: "visible", timeout: this.timeout });
            const txt = await active.textContent({ timeout: 2000 }) || "";
            const pageNum = parseInt(txt.trim());
            this.logger.info(`[OK] Current page: ${pageNum}`);
            return pageNum;
        } catch (e) {
            try {
                const mobile = this.page.locator(PaginationFooter.MOBILE_COUNTER).first();
                const txt = await mobile.textContent({ timeout: 2000 }) || "";
                const [current] = this._parsePageOfText(txt);
                if (current !== null) {
                    this.logger.info(`[OK] Current page (mobile): ${current}`);
                    return current;
                }
            } catch (ee) {}
            this.logger.warning(`[WARN] Could not get current page: ${e}`);
            return null;
        }
    }

    async getTotalPages(): Promise<number | null> {
        try {
            const mobile = this.page.locator(PaginationFooter.MOBILE_COUNTER).first();
            if (await mobile.isVisible({ timeout: 2000 })) {
                const txt = await mobile.textContent({ timeout: 2000 }) || "";
                const [, total] = this._parsePageOfText(txt);
                if (total !== null) {
                    this.logger.info(`[OK] Total pages (mobile): ${total}`);
                    return total;
                }
            }
        } catch (e) {}

        try {
            const pageBtns = await this.page.locator("ul.hidden.sm\\:flex button[aria-label^='Page']").all();
            const nums: number[] = [];
            for (const btn of pageBtns) {
                const label = await btn.getAttribute("aria-label", { timeout: 1000 }) || "";
                const m = label.match(/Page\s+(\d+)/);
                if (m) {
                    nums.push(parseInt(m[1]));
                }
            }
            if (nums.length > 0) {
                const total = Math.max(...nums);
                this.logger.info(`[OK] Total pages (from buttons): ${total}`);
                return total;
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not determine total pages: ${e}`);
        }
        return null;
    }

    async getVisiblePageNumbers(): Promise<number[]> {
        const nums: number[] = [];
        try {
            const btns = await this.page.locator("ul.hidden.sm\\:flex button[aria-label^='Page']").all();
            for (const btn of btns) {
                const label = await btn.getAttribute("aria-label", { timeout: 1000 }) || "";
                const m = label.match(/Page\s+(\d+)/);
                if (m) {
                    nums.push(parseInt(m[1]));
                }
            }
            this.logger.info(`[OK] Visible page numbers: ${nums}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read page numbers: ${e}`);
        }
        return nums;
    }

    async isPreviousDisabled(): Promise<boolean> {
        try {
            const prev = this.page.locator(PaginationFooter.PREV_BTN).first();
            return await prev.isDisabled({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isNextDisabled(): Promise<boolean> {
        try {
            const nxt = this.page.locator(PaginationFooter.NEXT_BTN).first();
            return await nxt.isDisabled({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isOnFirstPage(): Promise<boolean> {
        return await this.isPreviousDisabled();
    }

    async isOnLastPage(): Promise<boolean> {
        return await this.isNextDisabled();
    }

    // ------------------------------------------------------------------ #
    //  Navigation Actions
    // ------------------------------------------------------------------ #

    async goToNext(): Promise<boolean> {
        try {
            if (await this.isNextDisabled()) {
                this.logger.warning("[WARN] Already on last page, cannot go next");
                return false;
            }
            const nxt = this.page.locator(PaginationFooter.NEXT_BTN).first();
            await nxt.waitFor({ state: "visible", timeout: this.timeout });
            await nxt.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info("[OK] Navigated to next page");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not go to next page: ${e}`);
            return false;
        }
    }

    async goToPrevious(): Promise<boolean> {
        try {
            if (await this.isPreviousDisabled()) {
                this.logger.warning("[WARN] Already on first page, cannot go previous");
                return false;
            }
            const prev = this.page.locator(PaginationFooter.PREV_BTN).first();
            await prev.waitFor({ state: "visible", timeout: this.timeout });
            await prev.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info("[OK] Navigated to previous page");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not go to previous page: ${e}`);
            return false;
        }
    }

    async goToPage(pageNum: number): Promise<boolean> {
        try {
            const btn = this._pageBtn(pageNum);
            await btn.waitFor({ state: "visible", timeout: this.timeout });
            await btn.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Navigated to page ${pageNum}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not go to page ${pageNum}: ${e}`);
            return false;
        }
    }

    async goToFirstPage(): Promise<boolean> {
        return await this.goToPage(1);
    }

    // ------------------------------------------------------------------ #
    //  Composite Validation
    // ------------------------------------------------------------------ #

    async validateAll(): Promise<any> {
        const result: any = {
            visible: false,
            currentPage: null,
            totalPages: null,
            prevDisabled: null,
            nextDisabled: null,
            pageNumbers: [],
        };

        result.visible = await this.validateVisible();
        if (!result.visible) {
            this.logger.info("[INFO] Pagination not visible - likely single page result");
            return result;
        }

        result.currentPage = await this.getCurrentPage();
        result.totalPages = await this.getTotalPages();
        result.prevDisabled = await this.isPreviousDisabled();
        result.nextDisabled = await this.isNextDisabled();
        result.pageNumbers = await this.getVisiblePageNumbers();

        this.logger.info(`[PaginationFooter] Validation result: ${JSON.stringify(result)}`);
        return result;
    }
}
