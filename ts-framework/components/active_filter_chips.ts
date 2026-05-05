import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Active Filter Chips Component Utility
 * ======================================
 * UI: Radix-based popover dropdown with multi-select checkboxes.
 */
export class ActiveFilterChips {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Primary Selectors ---
    static readonly TRIGGER_BTN = "button[role='combobox']";
    static readonly CHIP_CONTAINER = "div.flex.items-center.gap-1.flex-nowrap";
    static readonly DROPDOWN_DIALOG = "[role='dialog'], [role='menu'], [data-radix-popper-content-wrapper]";
    static readonly CLEAR_ALL_BTN = "button:text('Clear All')";

    // --- Multi-Locator Fallback Arrays ---
    static readonly TRIGGER_SELECTORS = [
        "button[role='combobox']",
        "button[aria-haspopup='dialog']",
        "div.flex button[role='combobox']",
        "button:has(span.tabular-nums)",
    ];

    static readonly DIALOG_SELECTORS = [
        "[role='dialog'][data-state='open']",
        "div.fixed.z-50[data-state='open']",
        "[data-radix-popper-content-wrapper]",
        "div[role='dialog']",
        "div[role='menu']",
    ];

    constructor(page: Page, timeout: number = 15000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    private async _resolve(selectors: string[], timeout: number = 3000): Promise<Locator | null> {
        for (const sel of selectors) {
            try {
                const el = this.page.locator(sel).first();
                if (await el.isVisible({ timeout })) {
                    return el;
                }
            } catch (e) {
                continue;
            }
        }
        return null;
    }

    private async _trigger(): Promise<Locator> {
        const resolved = await this._resolve(ActiveFilterChips.TRIGGER_SELECTORS);
        if (resolved) return resolved;
        return this.page.locator(ActiveFilterChips.TRIGGER_BTN).first();
    }

    private async _dialog(): Promise<Locator> {
        for (const sel of ActiveFilterChips.DIALOG_SELECTORS) {
            const el = this.page.locator(sel).first();
            if (await el.isVisible({ timeout: 2000 })) {
                return el;
            }
        }
        return this.page.locator(ActiveFilterChips.DROPDOWN_DIALOG).first();
    }

    async isOpen(): Promise<boolean> {
        for (const sel of ActiveFilterChips.DIALOG_SELECTORS) {
            if (await this.page.locator(sel).first().isVisible({ timeout: 1000 })) {
                return true;
            }
        }
        return false;
    }

    async validateChipsVisible(): Promise<boolean> {
        try {
            const trigger = await this._trigger();
            await trigger.waitFor({ state: 'visible', timeout: this.timeout });
            this.logger.info("[OK] Active Filter Chips trigger is visible");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Active Filter Chips not visible: ${e}`);
            return false;
        }
    }

    async getActiveChipNames(): Promise<string[]> {
        const names: string[] = [];
        try {
            const removeBtns = await this.page.locator("button[aria-label^='Remove']").all();
            for (const btn of removeBtns) {
                const label = await btn.getAttribute("aria-label") || "";
                names.push(label.replace("Remove ", "").trim());
            }
            this.logger.info(`[OK] Active chips: ${names}`);
        } catch (e) {}
        return names;
    }

    async openDropdown(): Promise<boolean> {
        try {
            if (await this.isOpen()) {
                this.logger.info("[INFO] Dropdown already open");
                return true;
            }
            const trigger = await this._trigger();
            await trigger.click({ force: true });
            
            const orSelector = ActiveFilterChips.DIALOG_SELECTORS.join(", ");
            await this.page.locator(orSelector).first().waitFor({ state: 'visible', timeout: 8000 });
            
            this.logger.info("[OK] Filter chips dropdown opened");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not open filter chips dropdown: ${e}`);
            return false;
        }
    }

    async closeDropdown(): Promise<void> {
        try {
            if (!await this.isOpen()) return;
            await this.page.keyboard.press("Escape");
            await this.page.waitForTimeout(500);
            this.logger.info("[OK] Filter chips dropdown closed");
        } catch (e) {
            this.logger.warning(`[WARN] Could not close dropdown: ${e}`);
        }
    }

    async getAvailableStatuses(): Promise<string[]> {
        const statuses: string[] = [];
        try {
            const dialog = await this._dialog();
            const rows = await dialog.locator("button.relative span.truncate, [role='option'] span.truncate").all();
            for (const row of rows) {
                const txt = await row.textContent() || "";
                if (txt.trim()) statuses.push(txt.trim());
            }
            this.logger.info(`[OK] Available statuses: ${statuses}`);
        } catch (e) {}
        return statuses;
    }

    async selectStatus(statusName: string): Promise<boolean> {
        try {
            const dialog = await this._dialog();
            const row = dialog.locator(`button.relative:has-text("${statusName}"), [role='option']:has-text("${statusName}")`).first();
            await row.click({ force: true });
            this.logger.info(`[OK] Selected status: ${statusName}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not select status "${statusName}": ${e}`);
            return false;
        }
    }

    async clearAll(): Promise<boolean> {
        try {
            const dialog = await this._dialog();
            const clearBtn = dialog.locator("button:has-text('Clear All')").first();
            if (await clearBtn.isVisible({ timeout: 2000 })) {
                await clearBtn.click();
                this.logger.info("[OK] Clicked Clear All");
                return true;
            }
            this.logger.warning("[WARN] Clear All button not visible");
            return false;
        } catch (e) {
            return false;
        }
    }

    async validateAll(): Promise<any> {
        return {
            visible: await this.validateChipsVisible(),
            chipNames: await this.getActiveChipNames()
        };
    }
}
