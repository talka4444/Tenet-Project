import { Component, Input, OnInit } from '@angular/core';
import { ScanResult, ScanService } from '../services/scan.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-scan-results',
  imports: [CommonModule],
  templateUrl: './scan-results.html',
  styleUrl: './scan-results.css',
})
export class ScanResults {
  @Input() results: ScanResult[] = [];
}
