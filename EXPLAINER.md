# Playto Engineering Challenge - Explainer

## The Tree: Handling Nested Comments Efficiently

To solve the **N+1 Nightmare** (fetching a post with 50 nested comments without 50 SQL queries), I implemented an **"adjacency list deserialization"** strategy.

### The Problem
A standard recursive serializer or lazy-loading approach would trigger a database query for the `replies` of every single comment, leading to O(N) queries where N is the number of comments.

### The Solution (O(1) Query for Comments)
Instead of recursion at the database level, I fetch **ALL** comments for a thread in a single optimized SQL query:

```python
# feed/views.py

# 1. Fetch ALL comments in one go (with author and like counts optimized)
all_comments = Comment.objects.filter(thread=instance).select_related('author').annotate(
    likes_count=Count('likes')
).order_by('created_at')
```

I then assemble the tree structure **in memory** (Python) using a hash map logic:
1.  Map all comments by ID (`comment_map = {c.id: c ...}`).
2.  Iterate through the list once.
3.  If a comment has a `parent_id`, append it directly to its parent's `prefetched_replies` list in memory.
4.  If it has no parent, it is a root comment.

This reduces the database load to exactly **1 query** for the comments, regardless of depth or count. The Serializer then simply serializes this pre-computed structure.

## The Math: Dynamic Leaderboard

To ensure the leaderboard purely reflects activity from the **last 24 hours** without storing state on the User model, I used Django's aggregation capabilities on the transaction log (`KarmaActivity` model).

**The Logic:**
Sum the `amount` of all `KarmaActivity` records created `>= now - 24h` for each user.

**The Code:**
```python
# feed/views.py

last_24h = timezone.now() - timedelta(hours=24)

leaderboard = KarmaActivity.objects.filter(
    created_at__gte=last_24h
).values('user__username').annotate(
    total_karma=Sum('amount')
).order_by('-total_karma')[:5]
```

## The AI Audit

**The Bug:**
During the implementation of the Like system, the AI generated a `ThreadViewSet` that attempted to count likes using `Count('kwargs')`.

**The Fix:**
This was obviously a hallucination or typo. I debugged the ViewSet and corrected it to `Count('likes')`. I also identified that the `is_liked` field in the serializer was originally causing 500 errors because the `GenericRelation` was missing from the models, preventing the reverse lookup. I manually added the `GenericRelation` to both `Thread` and `Comment` models to enable efficient querying.
