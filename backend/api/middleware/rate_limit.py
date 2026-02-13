"""
Rate limiting middleware using in-memory sliding window.
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import time
from typing import Dict, List, Tuple
import asyncio


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate limiting middleware with sliding window algorithm.

    Limits:
    - 20 requests per minute per IP address
    - Cleans up expired sessions every 5 minutes
    - Monitors memory usage
    """

    def __init__(self, app, requests_per_minute: int = 20):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60

        # In-memory storage: IP -> List of (timestamp, request_count)
        self.request_log: Dict[str, List[float]] = defaultdict(list)

        # Session cleanup tracking
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 5 minutes

        # Memory monitoring
        self.memory_warning_threshold = 10000  # entries

    async def dispatch(self, request: Request, call_next):
        """
        Process request with rate limiting check.
        """
        # Get client IP
        client_ip = self._get_client_ip(request)

        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)

        # Perform periodic cleanup
        await self._cleanup_sessions()

        # Check rate limit
        current_time = time.time()
        if not self._is_allowed(client_ip, current_time):
            retry_after = self._calculate_retry_after(client_ip, current_time)

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )

        # Log request
        self._log_request(client_ip, current_time)

        # Monitor memory usage
        self._check_memory_usage()

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        remaining = self._get_remaining_requests(client_ip, current_time)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time) + self.window_seconds)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP from request, checking X-Forwarded-For header.
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Take first IP from comma-separated list
            return forwarded.split(",")[0].strip()

        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"

    def _is_allowed(self, client_ip: str, current_time: float) -> bool:
        """
        Check if request is allowed under rate limit.

        Uses sliding window: only count requests within last 60 seconds.
        """
        # Get request log for this IP
        requests = self.request_log[client_ip]

        # Remove expired requests (outside sliding window)
        window_start = current_time - self.window_seconds
        valid_requests = [ts for ts in requests if ts > window_start]

        # Update log with only valid requests
        self.request_log[client_ip] = valid_requests

        # Check if under limit
        return len(valid_requests) < self.requests_per_minute

    def _log_request(self, client_ip: str, current_time: float):
        """
        Log a new request for the client IP.
        """
        self.request_log[client_ip].append(current_time)

    def _get_remaining_requests(self, client_ip: str, current_time: float) -> int:
        """
        Calculate remaining requests in current window.
        """
        requests = self.request_log.get(client_ip, [])
        window_start = current_time - self.window_seconds
        valid_requests = [ts for ts in requests if ts > window_start]

        remaining = self.requests_per_minute - len(valid_requests)
        return max(0, remaining)

    def _calculate_retry_after(self, client_ip: str, current_time: float) -> int:
        """
        Calculate retry-after seconds until rate limit resets.
        """
        requests = self.request_log.get(client_ip, [])
        if not requests:
            return 0

        # Find oldest request in current window
        window_start = current_time - self.window_seconds
        valid_requests = [ts for ts in requests if ts > window_start]

        if not valid_requests:
            return 0

        # Time until oldest request expires
        oldest_request = min(valid_requests)
        retry_after = int(oldest_request + self.window_seconds - current_time) + 1

        return max(1, retry_after)

    async def _cleanup_sessions(self):
        """
        Periodic cleanup of expired session data (T025A).

        Removes IPs with no requests in last 5 minutes.
        """
        current_time = time.time()

        # Only cleanup every 5 minutes
        if current_time - self.last_cleanup < self.cleanup_interval:
            return

        # Cleanup expired IPs
        expired_ips = []
        cleanup_threshold = current_time - self.cleanup_interval

        for ip, requests in self.request_log.items():
            # Remove expired requests
            valid_requests = [ts for ts in requests if ts > cleanup_threshold]

            if not valid_requests:
                # No recent requests, mark for removal
                expired_ips.append(ip)
            else:
                # Update with cleaned list
                self.request_log[ip] = valid_requests

        # Remove expired IPs
        for ip in expired_ips:
            del self.request_log[ip]

        self.last_cleanup = current_time

        # Log cleanup stats
        if expired_ips:
            print(f"[RateLimit] Cleaned up {len(expired_ips)} expired IP sessions")

    def _check_memory_usage(self):
        """
        Monitor memory usage and log warnings (T025B).

        Tracks total IPs and requests in memory.
        """
        total_ips = len(self.request_log)
        total_requests = sum(len(requests) for requests in self.request_log.values())

        # Log warning if exceeding threshold
        if total_ips > self.memory_warning_threshold:
            print(f"[RateLimit] WARNING: High memory usage - {total_ips} IPs, {total_requests} requests tracked")
            print(f"[RateLimit] Consider implementing Redis-based rate limiting for production")

        # Log stats every 1000 IPs
        if total_ips > 0 and total_ips % 1000 == 0:
            print(f"[RateLimit] Memory stats - {total_ips} IPs, {total_requests} requests")
