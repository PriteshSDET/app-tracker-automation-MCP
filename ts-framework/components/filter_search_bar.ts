import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Filter & Search Bar Component Utility
 * =======================================
 * UI:
 *   - Search Type Selector:  dropdown button showing current field (e.g. "Name")
 *   - Search Input Field:    text input with placeholder "Search by Name"
 *   - Date Range Picker:     combobox button showing "Prev + Current Month"
 *   - Status Filter Trigger: combobox button (shows active filter chips, count badge)
 */
export class FilterSearchBar {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Selectors ---
    static readonly SEARCH_TYPE_BTN = "button[aria-label='Choose search field']";
    static readonly SEARCH_INPUT = "input[type='text'][placeholder*='Search']";
    static readonly SEARCH_INPUT_ALT = [
        "input[placeholder*='Search']",
        "input[placeholder*='search']",
        "div.flex.items-center.gap-2.flex-1 input",
        ".flex-1.min-w-48 input",
    ];
    static readonly DATE_PICKER_BTN = "button[role='combobox'][aria-expanded]";
    static readonly STATUS_TRIGGER = "button[role='combobox'][aria-haspopup='dialog']";
    static readonly SEARCH_WRAPPER = "div.hidden.md\\:flex.items-center.gap-2";
    static readonly DATE_PICKER_LABEL = "Prev + Current Month";

    constructor(page: Page, timeout: number = 15000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    // ------------------------------------------------------------------ #
    //  Private helpers
    // ------------------------------------------------------------------ #

    private async _searchInput(): Promise<Locator | null> {
        const selectors = [FilterSearchBar.SEARCH_INPUT, ...FilterSearchBar.SEARCH_INPUT_ALT];
        for (const sel of selectors) {
            try {
                const el = this.page.locator(sel).first();
                if (await el.isVisible({ timeout: 2000 })) {
                    const attr = await el.getAttribute("type", { timeout: 1000 }) || "";
                    if (attr.toLowerCase() !== "image") {
                        return el;
                    }
                }
            } catch (e) {
                continue;
            }
        }
        return null;
    }

    private async _datePicker(): Promise<Locator | null> {
        try {
            const el = this.page.locator(
                `button[role='combobox']:has(span:text-is('${FilterSearchBar.DATE_PICKER_LABEL}'))`
            ).first();
            if (await el.isVisible({ timeout: 3000 })) {
                return el;
            }
        } catch (e) {}

        try {
            const combos = await this.page.locator(FilterSearchBar.DATE_PICKER_BTN).all();
            for (const c of combos) {
                const txt = await c.textContent({ timeout: 1000 }) || "";
                if (txt.includes("Month") || txt.toLowerCase().includes("date")) {
                    return c;
                }
            }
        } catch (e) {}
        return null;
    }

    // ------------------------------------------------------------------ #
    //  Visibility Checks
    // ------------------------------------------------------------------ #

    async isSearchBarVisible(): Promise<boolean> {
        try {
            return await this.page.locator(FilterSearchBar.SEARCH_TYPE_BTN).first().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isSearchInputVisible(): Promise<boolean> {
        const inp = await this._searchInput();
        return inp !== null && await inp.isVisible({ timeout: 3000 });
    }

    async isDateFilterVisible(): Promise<boolean> {
        const dp = await this._datePicker();
        return dp !== null;
    }

    // ------------------------------------------------------------------ #
    //  Read State
    // ------------------------------------------------------------------ #

    async getSearchType(): Promise<string | null> {
        try {
            const btn = this.page.locator(FilterSearchBar.SEARCH_TYPE_BTN).first();
            await btn.waitFor({ state: "visible", timeout: this.timeout });
            const label = await btn.locator("span.font-medium").first().textContent({ timeout: 2000 });
            this.logger.info(`[OK] Search type: ${label}`);
            return (label || "").trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read search type: ${e}`);
            return null;
        }
    }

    async getSearchValue(): Promise<string | null> {
        try {
            const inp = await this._searchInput();
            if (inp) {
                const val = await inp.inputValue({ timeout: 2000 });
                this.logger.info(`[OK] Search input value: '${val}'`);
                return val;
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not read search value: ${e}`);
        }
        return null;
    }

    async getDateFilterLabel(): Promise<string | null> {
        try {
            const dp = await this._datePicker();
            if (dp) {
                const txt = await dp.textContent({ timeout: 2000 });
                const label = (txt || "").trim();
                this.logger.info(`[OK] Date filter label: ${label}`);
                return label;
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not read date filter label: ${e}`);
        }
        return null;
    }

    // ------------------------------------------------------------------ #
    //  Search Interactions
    // ------------------------------------------------------------------ #

    async setSearchType(fieldName: string): Promise<boolean> {
        try {
            const btn = this.page.locator(FilterSearchBar.SEARCH_TYPE_BTN).first();
            await btn.waitFor({ state: "visible", timeout: this.timeout });
            await btn.click();
            const option = this.page.locator(`[role='dialog'] button:has-text('${fieldName}')`).first();
            await option.waitFor({ state: "visible", timeout: this.timeout });
            await option.click();
            this.logger.info(`[OK] Search type set to: ${fieldName}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not set search type to '${fieldName}': ${e}`);
            return false;
        }
    }

    async search(text: string): Promise<boolean> {
        try {
            const inp = await this._searchInput();
            if (!inp) {
                this.logger.warning("[WARN] Search input not found");
                return false;
            }
            await inp.waitFor({ state: "visible", timeout: this.timeout });
            await inp.click();
            await inp.fill(text);
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Searched for: '${text}'`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Search failed for '${text}': ${e}`);
            return false;
        }
    }

    async clearSearch(): Promise<boolean> {
        try {
            const inp = await this._searchInput();
            if (!inp) {
                this.logger.warning("[WARN] Search input not found for clear");
                return false;
            }
            await inp.click();
            await inp.fill("");
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info("[OK] Search input cleared");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not clear search: ${e}`);
            return false;
        }
    }

    async searchAndVerify(text: string): Promise<boolean> {
        if (!await this.search(text)) {
            return false;
        }
        const val = await this.getSearchValue();
        if (val === text) {
            this.logger.info(`[OK] Search verified: '${text}'`);
            return true;
        }
        this.logger.warning(`[WARN] Search verify failed: expected '${text}', got '${val}'`);
        return false;
    }

    // ------------------------------------------------------------------ #
    //  Date Filter Interactions
    // ------------------------------------------------------------------ #

    async openDateFilter(): Promise<boolean> {
        try {
            const dp = await this._datePicker();
            if (!dp) {
                this.logger.warning("[WARN] Date filter button not found");
                return false;
            }
            await dp.waitFor({ state: "visible", timeout: this.timeout });
            await dp.click();
            this.logger.info("[OK] Date filter opened");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not open date filter: ${e}`);
            return false;
        }
    }

    async closeDateFilter(): Promise<void> {
        try {
            await this.page.keyboard.press("Escape");
            this.logger.info("[OK] Date filter closed");
        } catch (e) {
            this.logger.warning(`[WARN] Could not close date filter: ${e}`);
        }
    }

    // ------------------------------------------------------------------ #
    //  Status Filter Trigger
    // ------------------------------------------------------------------ #

    async openStatusFilter(): Promise<boolean> {
        try {
            const trigger = this.page.locator(FilterSearchBar.STATUS_TRIGGER).first();
            await trigger.waitFor({ state: "visible", timeout: this.timeout });
            await trigger.click();
            this.logger.info("[OK] Status filter dropdown opened from search bar");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not open status filter: ${e}`);
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Composite Validation
    // ------------------------------------------------------------------ #

    async validateAll(): Promise<any> {
        const result = {
            searchBarVisible: false,
            searchInputVisible: false,
            searchType: null as string | null,
            dateFilterVisible: false,
            dateFilterLabel: null as string | null,
        };

        try {
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
        } catch (e) {}

        result.searchBarVisible = await this.isSearchBarVisible();
        result.searchInputVisible = await this.isSearchInputVisible();
        result.searchType = await this.getSearchType();
        result.dateFilterVisible = await this.isDateFilterVisible();
        result.dateFilterLabel = await this.getDateFilterLabel();

        if (result.searchBarVisible) {
            this.logger.info("[OK] Filter & Search Bar validated successfully");
        } else {
            this.logger.warning("[WARN] Filter & Search Bar not fully visible");
        }

        this.logger.info(`[FilterSearchBar] Validation result: ${JSON.stringify(result)}`);
        return result;
    }
}
