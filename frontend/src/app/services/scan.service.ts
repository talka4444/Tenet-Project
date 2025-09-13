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

@Injectable({
  providedIn: 'root',
})
export class ScanService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getSuites(): Observable<string[]> {
    return this.http.get<string[]>(this.apiUrl + '/suites');
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
