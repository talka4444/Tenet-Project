import { Component, OnInit } from '@angular/core';
import { ScanService } from '../services/scan.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-view-scans',
  imports: [CommonModule],
  templateUrl: './view-scans.html',
  styleUrl: './view-scans.css',
})
export class ViewScans implements OnInit {
  scans: { id: string; url: string; completed: string }[] = [];
  isLoading = true;

  constructor(private scanService: ScanService) {}

  ngOnInit(): void {
    this.scanService.getAllScans().subscribe({
      next: (data) => {
        this.scans = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to fetch scans', err);
        this.isLoading = false;
      },
    });
  }
}
