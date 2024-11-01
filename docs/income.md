
---

### 3. **income.md**

```markdown
# Income Tracking Feature

## Overview
The Income Tracking feature in TrackMyDollar enables you to log and monitor your income alongside your expenses. This gives you a clear picture of your net balance, helping you manage both earnings and spending effectively.

## How to Use the Income Feature

1. **Adding an Income Entry**:
   - Use the `/income` command followed by the amount, category (optional), and description.
   - You can also specify a currency for the income if it differs from your base currency.

2. **Viewing Income Summary**:
   - To view a summary of your income for the day, month, or a custom period, use the `/summary` or `/month` commands. These will display both income and expenses, giving you a net balance overview.

3. **Editing an Income Entry**:
   - Use the `/edit <transaction_id>` command to modify any income entry.
   - Specify the updated details, and the bot will update the record accordingly.

## Example Commands

- **Adding a New Income Entry**:
  ```plaintext
  /income 2000 Salary "Monthly Salary"
