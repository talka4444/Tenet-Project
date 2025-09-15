import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';

export interface ScanResult {
  prompt: string;
  response: string;
  status: string;
}

export interface ResultsResponse {
  ScanId: string;
  results: ScanResult[];
}
export interface ScanItem {
  scanId: string;
  results: ScanResult[];
  isCompleted: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class ScanService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getAllSuites(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl + '/suites');
  }

  getAllScans(): Observable<{ id: string; url: string; completed: string }[]> {
    return this.http.get<{ id: string; url: string; completed: string }[]>(
      this.apiUrl + '/scans'
    );
  }

  createScan(data: { url: string; suite: string }): Observable<string> {
    return this.http
      .post<{ scanId: string }>(this.apiUrl + '/scan', data)
      .pipe(map((response) => response.scanId));
  }

  getStatus(scanId: string): Observable<string> {
    return this.http
      .get<{ completed: string }>(`${this.apiUrl}/status/${scanId}`)
      .pipe(map((response) => response.completed));
  }

  getResults(scanId: string): Observable<ResultsResponse> {
    return this.http.get<ResultsResponse>(`${this.apiUrl}/results/${scanId}`);
  }
}
