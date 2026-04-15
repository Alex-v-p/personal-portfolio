import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, shareReplay } from 'rxjs/operators';

import { API_BASE_URL } from '../../../core/config/api.config';

@Injectable({ providedIn: 'root' })
export class PublicHttpService {
  readonly http = inject(HttpClient);
  readonly apiBaseUrl = inject(API_BASE_URL);

  private readonly responseCache = new Map<string, Observable<unknown>>();

  cacheRequest<T>(cacheKey: string, requestFactory: () => Observable<T>): Observable<T> {
    const cachedResponse = this.responseCache.get(cacheKey);
    if (cachedResponse) {
      return cachedResponse as Observable<T>;
    }

    const request$ = requestFactory().pipe(
      catchError((error) => {
        this.responseCache.delete(cacheKey);
        return throwError(() => error);
      }),
      shareReplay({ bufferSize: 1, refCount: false })
    );

    this.responseCache.set(cacheKey, request$ as Observable<unknown>);

    return request$;
  }

  clearCachedRequest(cacheKey: string): void {
    this.responseCache.delete(cacheKey);
  }

  clearAllCachedRequests(): void {
    this.responseCache.clear();
  }
}
