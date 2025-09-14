import { Component } from '@angular/core';
import { CreateScan } from './create-scan/create-scan';
import { ScanResults } from './scan-results/scan-results';
import { ScanStatus } from './scan-status/scan-status';
import { ScanResult } from './services/scan.service';
import { CommonModule } from '@angular/common';

interface ScanItem {
  scanId: string;
  results: ScanResult[];
  isCompleted: boolean;
}

@Component({
  selector: 'app-root',
  imports: [ScanResults, CreateScan, ScanStatus, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  scans: ScanItem[] = [];

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
