import { Page, Locator, expect } from '@playwright/test';
import { Logger } from './logger';

/**
 * Top Navigation & Controls Component Utility
 * =============================================
 */
export class TopNavigationControls {
    private page: Page;
    private timeout: number;
    private logger: Logger;

    // --- Selectors ---
    static readonly LOGO_IMG = "img[alt='ABSLI']";
    static readonly PAGE_TITLE = "span.font-semibold.text-foreground.whitespace-nowrap";
    static readonly THEME_TOGGLE = "button[aria-label='Toggle theme']";
    static readonly ACCOUNT_BTN = "button[aria-label='Account menu']";
    static readonly USER_AVATAR = "span[role='img']";
    static readonly DOWNLOAD_BTN = "button:has-text('Download')";
    static readonly DOWNLOAD_ALT = [
        "button:has-text('Download')",
        "a:has-text('Download')",
        "[data-testid='download-btn']",
    ];
    static readonly NAV_CONTAINER = "div.flex.items-center.justify-between.w-full";

    constructor(page: Page, timeout: number = 15000) {
        this.page = page;
        this.timeout = timeout;
        this.logger = new Logger();
    }

    // ------------------------------------------------------------------ #
    //  Private helpers
    // ------------------------------------------------------------------ #

    private _nav(): Locator {
        return this.page.locator(TopNavigationControls.NAV_CONTAINER).first();
    }

    private async _downloadBtn(): Promise<Locator | null> {
        for (const sel of TopNavigationControls.DOWNLOAD_ALT) {
            try {
                const el = this.page.locator(sel).first();
                if (await el.isVisible({ timeout: 3000 })) {
                    return el;
                }
            } catch (e) {
                continue;
            }
        }
        return null;
    }

    // ------------------------------------------------------------------ #
    //  Visibility Checks
    // ------------------------------------------------------------------ #

    async isLogoVisible(): Promise<boolean> {
        try {
            return await this.page.locator(TopNavigationControls.LOGO_IMG).first().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isPageTitleVisible(): Promise<boolean> {
        try {
            return await this.page.locator(TopNavigationControls.PAGE_TITLE).first().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isAccountMenuVisible(): Promise<boolean> {
        try {
            return await this.page.locator(TopNavigationControls.ACCOUNT_BTN).first().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    async isDownloadBtnVisible(): Promise<boolean> {
        const btn = await this._downloadBtn();
        return btn !== null;
    }

    async isThemeToggleVisible(): Promise<boolean> {
        try {
            return await this.page.locator(TopNavigationControls.THEME_TOGGLE).first().isVisible({ timeout: 3000 });
        } catch (e) {
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Read State
    // ------------------------------------------------------------------ #

    async getPageTitle(): Promise<string | null> {
        try {
            const el = this.page.locator(TopNavigationControls.PAGE_TITLE).first();
            await el.waitFor({ state: "visible", timeout: this.timeout });
            const txt = await el.textContent({ timeout: 2000 }) || "";
            this.logger.info(`[OK] Page title: '${txt.trim()}'`);
            return txt.trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read page title: ${e}`);
            return null;
        }
    }

    async getLogoSrc(): Promise<string | null> {
        try {
            const src = await this.page.locator(TopNavigationControls.LOGO_IMG).first().getAttribute("src", { timeout: 3000 });
            this.logger.info(`[OK] Logo src: ${src}`);
            return src;
        } catch (e) {
            this.logger.warning(`[WARN] Could not read logo src: ${e}`);
            return null;
        }
    }

    async getUserInitials(): Promise<string | null> {
        try {
            const avatar = this.page.locator(TopNavigationControls.USER_AVATAR).first();
            const label = await avatar.getAttribute("aria-label", { timeout: 3000 });
            if (label) {
                this.logger.info(`[OK] User initials: ${label}`);
                return label.trim();
            }
            const inner = avatar.locator("span[aria-hidden='true']").first();
            const txt = await inner.textContent({ timeout: 1000 }) || "";
            this.logger.info(`[OK] User initials (inner): ${txt.trim()}`);
            return txt.trim();
        } catch (e) {
            this.logger.warning(`[WARN] Could not read user initials: ${e}`);
            return null;
        }
    }

    async getDownloadButtonText(): Promise<string | null> {
        try {
            const btn = await this._downloadBtn();
            if (btn) {
                const txt = await btn.textContent({ timeout: 2000 }) || "";
                this.logger.info(`[OK] Download button text: '${txt.trim()}'`);
                return txt.trim();
            }
        } catch (e) {
            this.logger.warning(`[WARN] Could not read download button text: ${e}`);
        }
        return null;
    }

    async getDownloadRecordCount(): Promise<number | null> {
        const txt = await this.getDownloadButtonText();
        if (!txt) return null;
        const m = txt.match(/(\d+)/);
        if (m) {
            const count = parseInt(m[1]);
            this.logger.info(`[OK] Download record count: ${count}`);
            return count;
        }
        return null;
    }

    // ------------------------------------------------------------------ #
    //  Interactions
    // ------------------------------------------------------------------ #

    async toggleTheme(): Promise<boolean> {
        try {
            const btn = this.page.locator(TopNavigationControls.THEME_TOGGLE).first();
            await btn.waitFor({ state: "visible", timeout: this.timeout });
            await btn.click();
            this.logger.info("[OK] Theme toggled");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not toggle theme: ${e}`);
            return false;
        }
    }

    async openAccountMenu(): Promise<boolean> {
        try {
            const btn = this.page.locator(TopNavigationControls.ACCOUNT_BTN).first();
            await btn.waitFor({ state: "visible", timeout: this.timeout });
            await btn.click({ force: true });
            this.logger.info("[OK] Account menu opened");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not open account menu: ${e}`);
            return false;
        }
    }

    async closeAccountMenu(): Promise<void> {
        try {
            await this.page.keyboard.press("Escape");
            this.logger.info("[OK] Account menu closed");
        } catch (e) {
            this.logger.warning(`[WARN] Could not close account menu: ${e}`);
        }
    }

    async clickDownload(expectedCount?: number): Promise<boolean> {
        try {
            const btn = await this._downloadBtn();
            if (!btn) {
                this.logger.warning("[WARN] Download button not found");
                return false;
            }

            if (expectedCount !== undefined) {
                const actualCount = await this.getDownloadRecordCount();
                if (actualCount !== expectedCount) {
                    this.logger.warning(
                        `[WARN] Download count mismatch: expected ${expectedCount}, got ${actualCount}`
                    );
                }
            }

            await btn.waitFor({ state: "visible", timeout: this.timeout });
            await btn.click();
            this.logger.info("[OK] Download button clicked");
            return true;
        } catch (e) {
            this.logger.warning(`[WARN] Could not click download button: ${e}`);
            return false;
        }
    }

    // ------------------------------------------------------------------ #
    //  Composite Validation
    // ------------------------------------------------------------------ #

    async validateAll(): Promise<any> {
        const result: any = {
            logoVisible: false,
            pageTitle: null,
            userInitials: null,
            themeToggleVisible: false,
            downloadVisible: false,
            downloadText: null,
            downloadCount: null,
        };

        try {
            await this.page.waitForLoadState("networkidle", { timeout: this.timeout });
        } catch (e) {}

        result.logoVisible = await this.isLogoVisible();
        result.pageTitle = await this.getPageTitle();
        result.userInitials = await this.getUserInitials();
        result.themeToggleVisible = await this.isThemeToggleVisible();
        result.downloadVisible = await this.isDownloadBtnVisible();
        result.downloadText = await this.getDownloadButtonText();
        result.downloadCount = await this.getDownloadRecordCount();

        if (result.logoVisible && result.pageTitle === "App Tracker") {
            this.logger.info("[OK] Top Navigation & Controls validated successfully");
        } else {
            this.logger.warning("[WARN] Top Navigation validation partial - check results");
        }

        this.logger.info(`[TopNavigationControls] Validation result: ${JSON.stringify(result)}`);
        return result;
    }
}
