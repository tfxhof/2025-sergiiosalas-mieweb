---
title: Mieweb
emoji: 📈
colorFrom: gray
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
short_description: Web app to calculate Mie extintion coeffitients
---

# MieWeb Project - Mie Calculation Interactive Tool

---

## Metadatos TfxHoF

- Autor: [Sergio Salas Sánchez]()
- Título: [Herramienta web para comparar la dispersión de luz por partículas esféricas de diferentes materiales mediante cálculos de Mie]()
- Fecha: Junio 2025

---

## Description

MieWeb is an interactive tool designed to compare the electromagnetic scattering response of different materials using Mie theory. It allows users to graphically visualize the absorption and scattering properties of optical materials, making it easier to compare their characteristics without requiring programming knowledge.


## Requirements

- python==3.12
- requirements.txt


## Installation Guide

### 1. Clone the Repository and navigate into mieWeb

First, clone this repository to your local machine:

```bash
git clone https://github.com/sergiiosalas/tfg.git
```

Then, navigate into the mieWeb directory where the application code is located:
```bash
cd tfg/mieWeb
```

### 2. Create and activate a virtual environment (optional but recommended)

It is recommended to use a virtual environment to manage dependencies. You can create and activate it using:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```


### 3. Install dependencies

Once you have cloned the repository, navigate into the mieWeb directory and install dependencies on your python environment:

```bash
pip install -r requirements.txt
```


### 4. Run the app

Once the dependencies are installed, you can run the application using:

```bash
python main.py
```
