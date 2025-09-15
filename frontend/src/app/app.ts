import { Component } from '@angular/core';
import { CreateScan } from './create-scan/create-scan';
import { ScanResults } from './scan-results/scan-results';
import { ScanStatus } from './scan-status/scan-status';
import { ScanItem, ScanResult } from './services/scan.service';
import { CommonModule } from '@angular/common';
import { ViewScans } from './view-scans/view-scans';

@Component({
  selector: 'app-root',
  imports: [ScanResults, CreateScan, ScanStatus, ViewScans, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  scans: ScanItem[] = [];
  showAllScans = false;
  showCreateScan = true;

  addScan(scanId: string) {
    this.scans.push({ scanId, results: [], isCompleted: false });
  }

  updateScanResults(scanId: string, results: ScanResult[]) {
    const scan = this.scans.find((scan) => scan.scanId === scanId);
    if (scan) {
      scan.results = results;
      scan.isCompleted = true;
    }
  }
}
