# Card comment format

Every employee posts exactly one comment per step on the card's issue, through:

```bash
python3 scripts/board.py comment <card> --step <strategist|analyst|engineer|inspector|manager> \
  --result <ok|failed|recovered|waiting> \
  --done "<what was done, one line, with links>" \
  --next "<what happens next, one line>" \
  --ask  "<only if Abhishek must decide: question? A) … B) … I recommend A because …>"
```

Result on GitHub:

> **Done:** Wrote the business brief: score 78, verdict GO (PR #12)
>
> **Next:** Your decision
>
> **Your call:** Strong demand, low cost. A) Approve build: merge PR #12 and move the card to Approved: build B) Refine pricing first C) Park. I recommend A because the cost to test is under a week.

The hidden marker `<!-- tt:step=… result=… -->` is added automatically; the manager uses it to detect
stuck work and count failures. Don't write it by hand.
