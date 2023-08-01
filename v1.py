import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill_time = time.time()

    def refill(self):
        now = time.time()
        time_since_last_refill = now - self.last_refill_time
        new_tokens = time_since_last_refill * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = now

    def consume(self, tokens):
        if tokens <= self.tokens:
            self.tokens -= tokens
            return True
        return False

class APIRateLimiter:
    def __init__(self, capacity, refill_rate, max_requests_per_second):
        self.token_bucket = TokenBucket(capacity, refill_rate)
        self.max_requests_per_second = max_requests_per_second

    def allow_request(self):
        self.token_bucket.refill()
        return self.token_bucket.consume(self.max_requests_per_second)

# Usage Example:
rate_limiter = APIRateLimiter(capacity=100, refill_rate=10, max_requests_per_second=5)

def make_api_request():
    if rate_limiter.allow_request():
        # Perform your API request here
        print("API request successful.")
    else:
        # Handle the rate limit exceeded scenario
        print("API rate limit exceeded. Please wait and try again later.")

# Simulate 20 API requests
for i in range(20):
    make_api_request()
    time.sleep(0.2)  # Add a small delay to simulate a real-world scenario
