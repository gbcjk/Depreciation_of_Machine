# Depreciation Calculator

A Python program to calculate asset depreciation using either straight-line or diminishing balance methods, with support for asset sales and profit/loss calculations.

## Features

- **Multiple Depreciation Methods**:
  - Straight-line method (fixed annual amount)
  - Diminishing balance method (percentage of remaining value)

- **Complete Asset Lifecycle Tracking**:
  - Purchase date and cost (including installation)
  - Annual depreciation calculations
  - Sale date and price recording
  - Automatic profit/loss calculation on disposal

- **Flexible Inputs**:
  - Custom accounting period end date
  - User-defined depreciation rate
  - Multiple assets management
  - Partial year depreciation calculations

## How to Use

1. **Input Parameters**:
   - Accounting year end date (DD-MM-YYYY format)
   - Depreciation rate (as percentage)
   - Depreciation method (straight-line or diminishing balance)

2. **For Each Asset**:
   - Purchase date and cost
   - Installation costs (if any)
   - Sale information (if sold) including date and price

3. **Output**:
   - Annual depreciation schedule for each asset
   - Book value at each accounting period end
   - Profit/loss calculation for sold assets
