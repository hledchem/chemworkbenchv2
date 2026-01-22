# Developer Guide: Project Structure

This document explains the purpose of each folder in the repository.

## chemworkbench/

### core/
- pipeline executor
- canonical models
- processor registry
- routing logic

### utils/
- math functions
- IO utilities
- plotting helpers

### processors/
- technique-specific processors
- thin wrappers around math

### plotting/
- three-tier plotting engine

### config/
- schema
- defaults
- templates

### api/
- stable interface for UI, CLI, and LLM

### cli/
- command-line interface

## docs/
All documentation.

## tests/
Unit tests for math, processors, pipeline, and plotting.
