import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Detail Drawer Component Utility
 * =================================
 * UI: Radix slide-out panel (right side) triggered by clicking a table row.
 */
export class DetailDrawer {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Primary Selectors ---
    static readonly DRAWER = "div[role='dialog'][data-state='open']";
    static readonly CLOSE_BTN = "button[aria-label='Close']";
    static readonly HEADER_NAME = "header span.block.text-base.font-semibold";
    static readonly ASIDE = "aside.w-60";
    static readonly STAGE_BTNS = "aside.w-60 ol li button";
    static readonly ACTIVE_STAGE = "aside.w-60 button[aria-current='step']";
    static readonly SUMMARY_BOX = "aside.w-60 div.p-6";
    static readonly MAIN_SECTION = "section.flex-1.overflow-y-auto";
    static readonly STAGE_HEADING = "section.flex-1 h2.text-xl.font-bold";
    static readonly STATUS_BADGE = "span.inline-flex.items-center.rounded.font-medium.whitespace-nowrap";
    static readonly LOCK_BADGE_SEL = "span.inline-flex.items-center.rounded.font-medium:has(span:text-is('Locked'))";
    static readonly COPY_LINK_BTN = "button.text-xs.text-purple-700";
    static readonly SHOW_MORE_BTN = "button.text-sm.text-purple-700";
    static readonly WORKFLOW_ROW = "div.flex.items-center.gap-3.py-2";

    // --- Multi-Locator Fallback Arrays ---
    static readonly DRAWER_SELECTORS = [
        "div[role='dialog'][data-state='open']",
        "div[role='dialog'][tabindex='-1']",
        "div.fixed.z-50[data-state='open']",
        "div.fixed.inset-y-0.right-0[role='dialog']",
    ];

    static readonly ASIDE_SELECTORS = [
        "aside.w-60",
        "aside.shrink-0.border-r",
        "aside.hidden.md\\:flex",
        "div[role='dialog'] aside",
    ];

    static readonly CLOSE_BTN_SELECTORS = [
        "button[aria-label='Close']",
        "header button[type='button']",
        "button:has(svg path[d*='205.66'])",
        "div[role='dialog'] header button",
    ];

    static readonly MAIN_SECTION_SELECTORS = [
        "section.flex-1.overflow-y-auto",
        "div.hidden.md\\:flex.flex-1 section",
        "div[role='dialog'] section",
    ];

    constructor(page: Page, timeout: number = 15000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    // ------------------------------------------------------------------ #
    //  Private helpers
    // ------------------------------------------------------------------ #

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

    private async _drawer(): Promise<Locator> {
        const resolved = await this._resolve(DetailDrawer.DRAWER_SELECTORS);
        if (resolved) {
            return resolved;
        }
        return this.page.locator(DetailDrawer.DRAWER).first();
    }

    private async _aside(): Promise<Locator> {
        const resolved = await this._resolve(DetailDrawer.ASIDE_SELECTORS);
        if (resolved) {
            return resolved;
        }
        return this.page.locator(DetailDrawer.ASIDE).first();
    }

    private async _main(): Promise<Locator> {
        const resolved = await this._resolve(DetailDrawer.MAIN_SECTION_SELECTORS);
        if (resolved) {
            return resolved;
        }
        return this.page.locator(DetailDrawer.MAIN_SECTION).first();
    }

    private _summaryBox(): Locator {
        return this.page.locator(DetailDrawer.SUMMARY_BOX).first();
    }

    private async _closeBtn(): Promise<Locator> {
        for (const sel of DetailDrawer.CLOSE_BTN_SELECTORS) {
            try {
                const el = this.page.locator(sel).first();
                if (await el.isVisible({ timeout: 2000 })) {
                    return el;
                }
            } catch (e) {
                continue;
            }
        }
        return this.page.locator(DetailDrawer.CLOSE_BTN).first();
    }

    // ------------------------------------------------------------------ #
    //  Open / Close / Visibility
    // ------------------------------------------------------------------ #

    async isOpen(): Promise<boolean> {
        try {
            const drawer = await this._drawer();
            return await drawer.isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async waitUntilOpen(): Promise<boolean> {
        try {
            let foundSel: string | null = null;
            for (const sel of DetailDrawer.DRAWER_SELECTORS) {
                try {
                    await this.page.locator(sel).waitFor({ state: 'attached', timeout: this.timeout });
                    foundSel = sel;
                    break;
                } catch (e) {
                    continue;
                }
            }
            if (!foundSel) {
                this.logger.warning("[WARN] Drawer not found via any selector (attached check)");
                return false;
            }
            await this.page.locator(foundSel).waitFor({ state: 'visible', timeout: this.timeout });
            this.logger.info(`[OK] Detail Drawer is open (selector: ${foundSel})`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Detail Drawer did not open: ${e}`);
            return false;
        }
    }

    async close(): Promise<boolean> {
        try {
            const btn = await this._closeBtn();
            await btn.waitFor({ state: 'visible', timeout: this.timeout });
            await btn.click();
            
            let dismissed = false;
            for (const sel of DetailDrawer.DRAWER_SELECTORS) {
                try {
                    await this.page.locator(sel).waitFor({ state: 'hidden', timeout: 5000 });
                    dismissed = true;
                    break;
                } catch (e) {
                    continue;
                }
            }
            if (!dismissed) {
                this.logger.warning("[WARN] Drawer may not have closed — hidden state not confirmed");
            }
            this.logger.info("[OK] Detail Drawer closed");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not close drawer: ${e}`);
            return false;
        }
    }

    async closeWithEscape(): Promise<void> {
        try {
            await this.page.keyboard.press("Escape");
            this.logger.info("[OK] Drawer closed via Escape");
        } catch (e) {
            this.logger.warning(`[WARN] Escape close failed: ${e}`);
        }
    }

    // ------------------------------------------------------------------ #
    //  Header
    // ------------------------------------------------------------------ #

    async getHeaderName(): Promise<string | null> {
        try {
            const drawer = await this._drawer();
            const el = drawer.locator(DetailDrawer.HEADER_NAME).first();
            await el.waitFor({ state: 'visible', timeout: this.timeout });
            const txt = await el.textContent({ timeout: 2000 }) || "";
            this.logger.info(`[OK] Drawer header name: '${txt.trim()}'`);
            return txt.trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read header name: ${e}`);
            return null;
        }
    }

    async getAriaTitle(): Promise<string | null> {
        try {
            const drawer = await this._drawer();
            const h2 = drawer.locator("h2.sr-only").first();
            return (await h2.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            return null;
        }
    }

    async getAriaDescription(): Promise<string | null> {
        try {
            const drawer = await this._drawer();
            const p = drawer.locator("p.sr-only").first();
            return (await p.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            return null;
        }
    }

    // ------------------------------------------------------------------ #
    //  Stepper / Stage Navigator
    // ------------------------------------------------------------------ #

    async getAllStages(): Promise<any[]> {
        const stages: any[] = [];
        try {
            const aside = await this._aside();
            const btns = await aside.locator("ol li button").all();
            for (const btn of btns) {
                const spans = await btn.locator("span.flex.flex-col span").all();
                const name = spans.length > 0 ? (await spans[0].textContent({ timeout: 1000 }) || "").trim() : "";
                const status = spans.length > 1 ? (await spans[1].textContent({ timeout: 1000 }) || "").trim() : "";
                if (name) {
                    stages.push({ name, status });
                }
            }
            this.logger.info(`[OK] Stages: ${JSON.stringify(stages)}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read stages: ${e}`);
        }
        return stages;
    }

    async getActiveStageName(): Promise<string | null> {
        try {
            const aside = await this._aside();
            const btn = aside.locator("button[aria-current='step']").first();
            const nameSpan = btn.locator("span.flex.flex-col span").first();
            const txt = await nameSpan.textContent({ timeout: 2000 }) || "";
            this.logger.info(`[OK] Active stage: '${txt.trim()}'`);
            return txt.trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read active stage: ${e}`);
            return null;
        }
    }

    async getStageStatus(stageName: string): Promise<string | null> {
        const stages = await this.getAllStages();
        for (const s of stages) {
            if (s.name.toLowerCase().includes(stageName.toLowerCase())) {
                return s.status;
            }
        }
        this.logger.warning(`[WARN] Stage '${stageName}' not found`);
        return null;
    }

    async clickStage(stageName: string): Promise<boolean> {
        try {
            const aside = await this._aside();
            let btn: Locator | null = null;
            const selectors = [
                `ol li button:has(span.flex.flex-col span:has-text('${stageName}'))`,
                `ol li button:has(span:has-text('${stageName}'))`,
                `aside button:has-text('${stageName}')`,
            ];

            for (const sel of selectors) {
                try {
                    const candidate = aside.locator(sel).first();
                    if (await candidate.isVisible({ timeout: 2000 })) {
                        btn = candidate;
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }

            if (!btn) {
                this.logger.warning(`[WARN] Stage button '${stageName}' not found`);
                return false;
            }
            
            await btn.waitFor({ state: 'visible', timeout: this.timeout });
            await btn.click({ force: true });
            
            try {
                await this.page.locator(`section.flex-1 h2.text-xl.font-bold:has-text('${stageName}')`).waitFor({ state: 'visible', timeout: this.timeout });
            } catch (e) {
                try {
                    await this.page.waitForLoadState("networkidle", { timeout: 5000 });
                } catch (ee) {}
            }
            
            this.logger.info(`[OK] Clicked stage: ${stageName}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click stage '${stageName}': ${e}`);
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Applicant Summary Box
    // ------------------------------------------------------------------ #

    async getAllSummaryFields(): Promise<Record<string, string>> {
        const data: Record<string, string> = {};
        try {
            const box = this._summaryBox();
            const rows = await box.locator("div.flex.flex-col.gap-0\\.5").all();
            for (const row of rows) {
                const spans = await row.locator("span").all();
                if (spans.length >= 2) {
                    const label = (await spans[0].textContent({ timeout: 1000 }) || "").trim();
                    const value = (await spans[1].textContent({ timeout: 1000 }) || "").trim();
                    if (label) {
                        data[label] = value;
                    }
                }
            }
            this.logger.info(`[OK] Summary fields: ${JSON.stringify(data)}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read summary fields: ${e}`);
        }
        return data;
    }

    async getSummaryField(label: string): Promise<string | null> {
        const fields = await this.getAllSummaryFields();
        for (const [key, val] of Object.entries(fields)) {
            if (key.toLowerCase().includes(label.toLowerCase())) {
                return val;
            }
        }
        this.logger.warning(`[WARN] Summary field '${label}' not found`);
        return null;
    }

    // ------------------------------------------------------------------ #
    //  Main Content
    // ------------------------------------------------------------------ #

    async getActiveStageHeading(): Promise<string | null> {
        try {
            const main = await this._main();
            const h2 = main.locator("h2.text-xl.font-bold").first();
            return (await h2.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read stage heading: ${e}`);
            return null;
        }
    }

    async getActiveStageBadgeStatus(): Promise<string | null> {
        try {
            const main = await this._main();
            const badgeArea = main.locator("div.flex.flex-wrap.items-center.gap-x-3").first();
            const badge = badgeArea.locator(DetailDrawer.STATUS_BADGE).first();
            return (await badge.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read stage badge status: ${e}`);
            return null;
        }
    }

    async getWorkflowSections(): Promise<string[]> {
        const sections: string[] = [];
        try {
            const main = await this._main();
            const headings = await main.locator("h3.text-sm.font-bold, h4.text-sm.font-bold").all();
            for (const h of headings) {
                const txt = (await h.textContent({ timeout: 1000 }) || "").trim();
                if (txt) sections.push(txt);
            }
            const topSpans = await main.locator("div.hidden.md\\:flex > span.text-sm.font-bold").all();
            for (const sp of topSpans) {
                const txt = (await sp.textContent({ timeout: 1000 }) || "").trim();
                if (txt && !sections.includes(txt)) {
                    sections.push(txt);
                }
            }
            this.logger.info(`[OK] Workflow sections: ${sections}`);
        } catch (e) {
            this.logger.warning(`[WARN] Could not read workflow sections: ${e}`);
        }
        return sections;
    }

    async getItemStatus(itemLabel: string): Promise<string | null> {
        try {
            const main = await this._main();
            const row = main.locator(`div.flex.items-center.gap-3:has(span:has-text('${itemLabel}'))`).first();
            const badge = row.locator(DetailDrawer.STATUS_BADGE).first();
            const txt = (await badge.textContent({ timeout: 2000 }) || "").trim();
            this.logger.info(`[OK] Item '${itemLabel}' status: ${txt}`);
            return txt;
        } catch (e) {
            this.logger.warning(`[WARN] Could not get status for '${itemLabel}': ${e}`);
            return null;
        }
    }

    async getAllItemStatuses(): Promise<any[]> {
        const items: any[] = [];
        try {
            const main = await this._main();
            const rows = await main.locator("div.flex.items-center.gap-3.py-2").all();
            for (const row of rows) {
                const labelSpans = await row.locator("span.text-sm.text-foreground.w-30").all();
                const label = labelSpans.length > 0 ? (await labelSpans[0].textContent({ timeout: 1000 }) || "").trim() : "";
                const badge = row.locator(DetailDrawer.STATUS_BADGE).first();
                let status = "";
                try {
                    status = (await badge.textContent({ timeout: 500 }) || "").trim();
                } catch (e) {}
                if (label) {
                    items.push({ label, status });
                }
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not read all item statuses: ${e}`);
        }
        return items;
    }

    async isItemLocked(itemLabel: string): Promise<boolean> {
        try {
            const main = await this._main();
            const section = main.locator(`div.hidden.md\\:flex:has(span:has-text('${itemLabel}'))`).first();
            const locked = section.locator(DetailDrawer.LOCK_BADGE_SEL).first();
            const result = await locked.isVisible({ timeout: 3000 });
            this.logger.info(`[OK] '${itemLabel}' locked: ${result}`);
            return result;
        } catch (e) {
            return false;
        }
    }

    async getLockMessage(itemLabel: string): Promise<string | null> {
        try {
            const main = await this._main();
            const section = main.locator(`div.hidden.md\\:flex:has(span:has-text('${itemLabel}'))`).first();
            const msg = section.locator("span.text-sm.text-muted-foreground").first();
            return (await msg.textContent({ timeout: 2000 }) || "").trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read lock message: ${e}`);
            return null;
        }
    }

    async clickCopyLink(itemLabel: string = "Mode of PIVC"): Promise<boolean> {
        try {
            const main = await this._main();
            const row = main.locator(`div.flex.items-center.gap-3:has(span:has-text('${itemLabel}'))`).first();
            const btn = row.locator(DetailDrawer.COPY_LINK_BTN).first();
            await btn.waitFor({ state: 'visible', timeout: this.timeout });
            await btn.click();
            this.logger.info(`[OK] Copy Link clicked for: ${itemLabel}`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click Copy Link for '${itemLabel}': ${e}`);
            return false;
        }
    }

    async clickShowMore(): Promise<boolean> {
        try {
            const main = await this._main();
            const btn = main.locator(DetailDrawer.SHOW_MORE_BTN).first();
            await btn.waitFor({ state: 'visible', timeout: this.timeout });
            const txt = await btn.textContent({ timeout: 1000 }) || "";
            await btn.click();
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
            this.logger.info(`[OK] Show More clicked: '${txt.trim()}'`);
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click Show More: ${e}`);
            return false;
        }
    }

    async getShowMoreText(): Promise<string | null> {
        try {
            const main = await this._main();
            const btn = main.locator(DetailDrawer.SHOW_MORE_BTN).first();
            if (await btn.isVisible({ timeout: 2000 })) {
                return (await btn.textContent({ timeout: 1000 }) || "").trim();
            }
        } catch (e) {}
        return null;
    }

    async validateAll(): Promise<any> {
        const result: any = {
            isOpen: false,
            headerName: null,
            ariaTitle: null,
            stages: [],
            activeStage: null,
            summaryFields: {},
            stageHeading: null,
            stageBadgeStatus: null,
            workflowSections: [],
            workflowItems: [],
            showMoreText: null,
        };

        result.isOpen = await this.waitUntilOpen();
        if (!result.isOpen) return result;

        try {
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
        } catch (e) {}

        result.headerName = await this.getHeaderName();
        result.ariaTitle = await this.getAriaTitle();
        result.stages = await this.getAllStages();
        result.activeStage = await this.getActiveStageName();
        result.summaryFields = await this.getAllSummaryFields();
        result.stageHeading = await this.getActiveStageHeading();
        result.stageBadgeStatus = await this.getActiveStageBadgeStatus();
        result.workflowSections = await this.getWorkflowSections();
        result.workflowItems = await this.getAllItemStatuses();
        result.showMoreText = await this.getShowMoreText();

        this.logger.info(`[DetailDrawer] Validation result: ${JSON.stringify(result)}`);
        return result;
    }
}
