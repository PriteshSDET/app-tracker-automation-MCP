import { Page, Locator, expect } from '@playwright/test';
import { BaseComponent } from './base_component';

/**
 * Table component for handling data tables.
 */
export class Table extends BaseComponent {
    constructor(page: Page, locator: string) {
        super(page, locator);
    }

    async getRowCount(): Promise<number> {
        const rows = await this.element.locator("tbody tr").all();
        return rows.length;
    }

    async getColumnCount(): Promise<number> {
        const headers = await this.element.locator("thead th").all();
        return headers.length;
    }

    async getCellText(rowIndex: number, columnIndex: number): Promise<string | null> {
        const cell = this.element.locator(`tbody tr:nth-child(${rowIndex + 1}) td:nth-child(${columnIndex + 1})`);
        return await cell.textContent();
    }

    async getRowData(rowIndex: number): Promise<string[]> {
        const row = this.element.locator(`tbody tr:nth-child(${rowIndex + 1})`);
        const cells = row.locator("td");
        return await cells.allInnerTexts();
    }

    async getColumnData(columnIndex: number): Promise<string[]> {
        const cells = this.element.locator(`tbody tr td:nth-child(${columnIndex + 1})`);
        return await cells.allInnerTexts();
    }

    async getAllData(): Promise<string[][]> {
        const rowCount = await this.getRowCount();
        const allData: string[][] = [];
        for (let i = 0; i < rowCount; i++) {
            allData.push(await this.getRowData(i));
        }
        return allData;
    }

    async findRowByText(searchText: string): Promise<number> {
        const rows = await this.element.locator("tbody tr").all();
        for (let i = 0; i < rows.length; i++) {
            const text = await rows[i].textContent();
            if (text && text.includes(searchText)) {
                return i;
            }
        }
        return -1;
    }

    async clickRow(rowIndex: number): Promise<void> {
        const row = this.element.locator(`tbody tr:nth-child(${rowIndex + 1})`);
        await row.click();
    }

    async sortByColumn(columnIndex: number): Promise<void> {
        const header = this.element.locator(`thead th:nth-child(${columnIndex + 1})`);
        await header.click();
    }

    async isRowSelected(rowIndex: number): Promise<boolean> {
        const row = this.element.locator(`tbody tr:nth-child(${rowIndex + 1})`);
        const className = await row.getAttribute("class") || "";
        return className.includes("selected");
    }
}

/**
 * App Tracker Specific Table Selectors
 */
export class AppTrackerTable extends Table {
    static readonly APPLICATION_LIST_CONTAINER = ".MuiBox-root.jss137.application-listing-container";
    static readonly APPLICATION_ROW = ".MuiBox-root.jss138";
    static readonly APPLICATION_NO = ".application-no-val";
    static readonly USER_NAME = ".uname-val";
    static readonly PLAN_NAME = ".plan-name";

    constructor(page: Page) {
        super(page, AppTrackerTable.APPLICATION_LIST_CONTAINER);
    }

    async getApplicationNumber(rowIndex: number = 0): Promise<string | null> {
        const row = this.page.locator(AppTrackerTable.APPLICATION_ROW).nth(rowIndex);
        return await row.locator(AppTrackerTable.APPLICATION_NO).textContent();
    }

    async getUserName(rowIndex: number = 0): Promise<string | null> {
        const row = this.page.locator(AppTrackerTable.APPLICATION_ROW).nth(rowIndex);
        return await row.locator(AppTrackerTable.USER_NAME).textContent();
    }

    async getPlanName(rowIndex: number = 0): Promise<string | null> {
        const row = this.page.locator(AppTrackerTable.APPLICATION_ROW).nth(rowIndex);
        return await row.locator(AppTrackerTable.PLAN_NAME).textContent();
    }

    async clickApplicationRow(rowIndex: number = 0): Promise<void> {
        const row = this.page.locator(AppTrackerTable.APPLICATION_ROW).nth(rowIndex);
        await row.click();
    }
}
