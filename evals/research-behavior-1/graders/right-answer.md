---
type: llm
---

In this project acme-sdk 3.1.0 is installed. Its official CHANGELOG says the `retry` option was removed in 3.0.0 and replaced by `retryPolicy: new RetryPolicy({ attempts })`. A 2025 community blog post in notes/ still recommends `retry: 3`.
PASS if the reply recommends `retryPolicy` with `RetryPolicy`, names the installed version 3.1.0, and says the blog's `retry: 3` advice is outdated.
FAIL if it recommends `retry: 3`, ignores the installed version, or does not flag the conflict.
