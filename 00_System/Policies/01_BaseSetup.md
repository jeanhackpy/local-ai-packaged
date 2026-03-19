# 🛠️ 01 - Base System Setup

**Part of:** [[SystemPolicy]]  
**Related:** [[README]]

## System Configuration Guidelines

This document outlines the base system setup guidelines for macOS Sequoia 15.7.3.

## Security Configuration

- FileVault enabled
- Firewall configured with blocked incoming connections
- SSH keys properly configured (see [[Development/VPS Hostinger & WordPress#SSH Config]])

## Development Environment

- Homebrew installed and configured (see [[SystemPolicy/02_DevEnv#Package Management]])
- Python managed by pyenv (see [[Development/IDE & Skills#Python Setup]])
- Node.js and npm installed (see [[SystemPolicy/02_DevEnv#Package Management]])
- Git configured with proper credentials (see [[SystemPolicy/02_DevEnv#Version Control]])

## Productivity Tools

- Raycast as primary launcher
- Warp terminal with voice input
- Stats for system monitoring
- Bitwarden for password management

## AI Agents Configuration

- [[Gemini CLI]] installed and configured
- [[Ollama]] with llama3.2 model
- [[Crawl4AI Datascraper]] for web scraping
- [[Superwhisper TTS]] for voice dictation
