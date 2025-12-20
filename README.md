# Allocation Table Processing Tool

This project was developed during my role as a Technical Clerk at BGEN to streamline the processing of allocation data sourced from multiple Excel spreadsheets.

One of my responsibilities involved preparing raw allocation data from 20 or more separate spreadsheets for input into a third-party workforce allocation system. The original workflow was time-consuming and error-prone due to inconsistent formatting, typographical errors, and manual data entry requirements.

This tool automates and simplifies that process and consists of two main components:

## Features

### 1. Spreadsheet Validation & Correction Tool
- A Python application built using Pygame
- Scans multiple spreadsheets for common data issues, including:
  - Inconsistent employee names
  - Incorrect or mismatched job titles
  - Invalid or missing hour allocations
- Highlights detected errors and provides a custom-built UI to correct them directly within the application, reducing the need for manual spreadsheet editing

### 2. Allocation Output Generator
- A standalone executable that processes the validated spreadsheets
- Consolidates the cleaned data into a single, standardised output table
- Produces a final format ready for copy-and-paste import into the allocation system

## Purpose

The tool significantly reduced manual data handling, improved accuracy, and sped up the allocation preparation workflow by automating repetitive checks and standardisation tasks.

## Technologies Used
- Python
- Pygame
- Openpyxl

## Limitations
- Designed for a specific spreadsheet structure used internally
- Not intended as a general-purpose ETL tool