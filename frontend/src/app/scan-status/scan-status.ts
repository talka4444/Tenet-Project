import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ScanResult, ScanService } from '../services/scan.service';
import { interval, Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-scan-status',
  imports: [CommonModule],
  templateUrl: './scan-status.html',
  styleUrl: './scan-status.css',
})
export class ScanStatus implements OnInit {
  @Input() scanId!: string;
  @Output() scanCompleted = new EventEmitter<ScanResult[]>();

  progress = '0%';
  private sub?: Subscription;

  constructor(private scanService: ScanService) {}

  ngOnInit() {
    this.sub = interval(2000).subscribe(() => {
      this.scanService.getStatus(this.scanId).subscribe({
        next: (completed) => {
          this.progress = completed;
          if (completed === '100.00%') {
            this.sub?.unsubscribe();
            this.scanService.getResults(this.scanId).subscribe({
              next: (res) => this.scanCompleted.emit(res.results),
              error: (err) => console.error(err),
            });
          }
        },
        error: (err) => {
          console.error(err);
          this.sub?.unsubscribe();
        },
      });
    });
  }
}
