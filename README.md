# 🛠 HolyC Compatibility Layer – Linux Binary Porting to TempleOS

## 🔍 Project Description

This project is a **lightweight compatibility layer** designed to enable execution of Linux-compiled binaries within **TempleOS**, using a custom-built **loader written in HolyC and x86_64 assembly**.

The loader intercepts system calls from external binaries and redirects them to equivalents implemented in HolyC, allowing controlled execution without altering the core of TempleOS.

---

## 💡 Objectives

- **Extend TempleOS's capabilities** while honoring its original design philosophy.
- Provide a method for interacting with external precompiled binaries inside a closed, minimal system.
- Bridge modern development tools and legacy sacred environments in a clean, deterministic way.

---

## 🧰 Features

- **Transpiler (Python)**  
  Converts standard C code to HolyC-compatible syntax:
  - Types: `int → I64`, `char → U8`, etc.
  - Functions: `printf → Print`, `malloc → MAlloc`, etc.
  - Control structures: `for`, `cast`, `#define`, and more.
  - Header handling: maps `<stdio.h>`, `<stdlib.h>` to `Sys/OS.h`.

- **Binary Loader (HolyC + x86_64 ASM)**  
  - Loads Linux ELF binaries directly into TempleOS memory.
  - Redirects syscalls to HolyC-defined equivalents.
  - Manages memory, environment (e.g., `argc`, `argv`), and process lifecycle.

- **Extensible System Call Interface**  
  - Users can define custom syscall mappings.
  - Designed for gradual expansion and integration of more complex runtime behaviors.

---

## 🔐 Philosophy

This project is not an attempt to modernize or override TempleOS.  
It is a **deliberate and respectful bridge**, built to preserve the system's spiritual and architectural identity while enabling selective, purposeful interaction with external software.

TempleOS is not just an operating system — it is a **philosophical construct**.  
This project treats it as such.


## 🙏 Credits

Inspired by the work and legacy of **Terry A. Davis**.  
With utmost respect for his vision and creation.
# TempleEntrance
⚠️ Non esiste alcuna giustificazione logica per questo progetto, ma funziona. Ed è bellissimo.
