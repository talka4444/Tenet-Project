import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ScanService } from '../services/scan.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-scan',
  imports: [CommonModule, FormsModule],
  templateUrl: './create-scan.html',
  styleUrl: './create-scan.css',
})
export class CreateScan implements OnInit {
  suites: string[] = [];
  urls: string[] = ['https://tryme.tendry.net/chat'];

  url: string = '';
  suite: string = '';
  scanId: string = '';
  isLoading: boolean = false;

  @Output() scanStarted = new EventEmitter<string>();

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getAllSuites().subscribe({
      next: (names) => {
        this.suites = names;
      },
      error: (err) => {
        console.error('Error fetching suite names', err);
      },
    });
  }

  createScan() {
    this.isLoading = true;
    this.scanService
      .createScan({ url: this.url, suite: this.suite })
      .subscribe({
        next: (scanId) => {
          this.isLoading = false;
          this.scanStarted.emit(scanId);
        },
        error: (err) => {
          this.isLoading = false;
          console.error(err);
        },
      });
  }
}
